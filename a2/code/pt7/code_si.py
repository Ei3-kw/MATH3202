from gurobipy import *

# SETS
Farms = ['Cowbell', 'Creamy Acres', 'Milky Way', 'Happy Cows', 
         'Udder Delight', 'Fresh Pail', 'Cowabunga', 'Utopia', 
         'Moo Meadows', 'Bluebell', 'Harmony', 'Velvet Valley', 
         'Moonybrook', 'Cloven Hills', 'Midnight Moo', 'Willows Bend', 
         'Moosa Heads', 'Dreamy Dairies', 'Happy Hooves', 'Highlands']

Facilities = ['PF0', 'PF1', 'PF2']

Tankers = ['Tanker 1', 'Tanker 2', 'Tanker 3', 'Tanker 4', 'Tanker 5']

F = range(len(Farms))
P = range(len(Facilities))
T = range(len(Tankers))

# DATA
Supply = [5200, 9900, 8800, 6900, 
          9500, 5900, 3700, 4800, 
          3200, 3400, 4400, 4500, 
          3200, 4800, 3100, 3400, 
          3000, 4500, 4500, 3900]

Distance = [
	[94,102,76],    # Cowbell
	[70,91,84],     # Creamy Acres
	[93,83,58],     # Milky Way 
	[103,88,61],    # Happy Cows 
	[59,79,86],     # Udder Delight
	[107,72,44],    # Fresh Pail
	[74,54,62],     # Cowabunga
	[94,57,44],     # Utopia
	[44,62,93],     # Moo Meadows 
	[34,71,103],    # Bluebell
	[51,51,83],     # Harmony
	[87,42,46],     # Velvet Valley
	[114,47,21],    # Moonybrook
	[25,70,107],    # Cloven Hills
	[56,39,79],     # Midnight Moo
	[66,30,70],     # Willows Bend
	[42,54,94],     # Moosa Heads
	[44,56,98],     # Dreamy Dairies
	[96,29,66],     # Happy Hooves
	[87,44,82]      # Highlands
]

PMin = [20000,24000,32000]  # maximum daily capacity (litres)
PMax = [45000,35000,36000]  # minimum daily processing (litres)

Maintenance = [500, 470, 440, 410, 380]     # cost of tanker maintenance ($/day)

TEmpty  = 2     # travel cost with empty tanker ($/km)
TFull   = 3     # travel cost with milk on board ($/km)
TRound  = 5     # travel cost for a round trip ($/km)

HMax = 10       # maximum number of hours a tanker can be used for 
DMax = 600      # maximum number of kilometers a tanker can be used for (assuming average speed of 60km/h)

# MODEL
m = Model('Comm 7')

# VARIABLES
W = {(p,t): m.addVar(vtype=GRB.BINARY, name=f"whether a tanker in the fleet is operational") for p in P for t in T}
X = {(p,f,t): m.addVar(vtype=GRB.BINARY, name=f"farm and tanker assignment per processing facility") for p in P for f in F for t in T}

# OBJECTIVE
""" minimise the cost of travel to all of the farms """
m.setObjective(quicksum(X[p,f,t] * Distance[f][p] * TRound for p in P for f in F for t in T) +     # cost for travel
               quicksum(W[p,t] * Maintenance[t] for p in P for t in T), GRB.MINIMIZE)   # cost for maintenance

# CONSTRAINTS
for p in P:
    # maximum daily capacity is not exceeded for each processing facility
    m.addConstr(quicksum(X[p,f,t] * Supply[f] for f in F for t in T) <= PMax[p])

    # minimum processing requirement is met for each processing facility
    m.addConstr(quicksum(X[p,f,t] * Supply[f] for f in F for t in T) >= PMin[p])

    for t in T:
        # tankers are operational for at most 10 hours (or 600 km) (we multiply by 2 to account for both directions of travel)
        m.addConstr(quicksum(X[p,f,t] * Distance[f][p] for f in F) * 2 <= DMax)

        # if a tanker is used, we set the binary variable to indicate this
        for f in F:
            m.addConstr((X[p,f,t] == 1) >> (W[p,t] == 1))

        # tankers must be used in order (this way the cheaper maintenance fees are not automatically applied)
        if t > 0:
            m.addConstr((W[p,t] == 1) >> (W[p,t-1] == 1))

for f in F:
    # each farm is assigned to one processing plant and one tanker
    m.addConstr(quicksum(X[p,f,t] for p in P for t in T) == 1)

m.optimize()

# Print gurobi solver status
if m.status == GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print(f"\n{'Totals'}\n{'-'*65}")
print(f"{'Total cost of travel:': <20} ${int(m.objVal)}\n")

print(f"{'-'*65}\n{'Facility': <13} {'Collection ($)': <18} {'Maintenance ($)': <18} {'Total ($)': <15}\n{'-'*65}")

for p in P:
    print(f"{Facilities[p]: <13} {int(quicksum(X[p,f,t].x * Distance[f][p] * TRound for f in F for t in T).getValue()): <18}", end='')
    print(f" {int(quicksum(W[p,t] * Maintenance[t] for t in T).getValue()): <18}", end='')
    print(f" {int(quicksum(X[p,f,t].x * Distance[f][p] * TRound for f in F for t in T).getValue() + quicksum(W[p,t] * Maintenance[t] for t in T).getValue())}")

print(f"{'-'*65}\n")


for p in P:
    print(f"PROCESSING FACILITY {p}")
    print(f"{'-'*80}\n{'Farms': <18} {'Dist. (km)': <15} {'Cost ($)': <15} {'Supply (L)': <15} {'Tanker': <15}\n{'-'*80}")
    for f in F:
        for t in T:
            if X[p,f,t].x:
                print(f"{Farms[f]: <18} {Distance[f][p]: <15} {Distance[f][p] * TRound: <15} {Supply[f]: <15} {Tankers[t]: <15}")
    print(f"{'-'*80}")
    print(f"{' '*18} {int(quicksum(X[p,f,t].x * Distance[f][p] for f in F for t in T).getValue()): <15}", end='')
    print(f" {int(quicksum(X[p,f,t].x * Distance[f][p] * TRound for f in F for t in T).getValue()): <15}", end='')
    print(f" {int(quicksum(X[p,f,t].x * Supply[f] for f in F for t in T).getValue())} / {PMax[0]}\n")

