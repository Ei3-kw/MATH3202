from gurobipy import *

# SETS
Farms = ['Cowbell', 'Creamy Acres', 'Milky Way', 'Happy Cows', 
         'Udder Delight', 'Fresh Pail', 'Cowabunga', 'Utopia', 
         'Moo Meadows', 'Bluebell', 'Harmony', 'Velvet Valley', 
         'Moonybrook', 'Cloven Hills', 'Midnight Moo', 'Willows Bend', 
         'Moosa Heads', 'Dreamy Dairies', 'Happy Hooves', 'Highlands']

Facilities = ['PF0', 'PF1', 'PF2']

F = range(len(Farms))
P = range(len(Facilities))

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

PMin = [20000,24000,32000]  # minimum daily processing (litres)
PMax = [45000,35000,36000]  # maximum daily processing capacity (litres)

TEmpty  = 2     # travel cost with empty tanker ($/km)
TFull   = 3     # travel cost with milk on board ($/km)
TRound  = 5     # travel cost for a round trip ($/km)

# MODEL
m = Model('Comm 6')

# VARIABLES
""" boolean variables to tell us which of the processing plants the farms are assigned to """
X = {(f, p): m.addVar(lb=0, vtype=GRB.BINARY, name=f"farm assignment") for f in F for p in P}

# OBJECTIVE
""" minimise the cost of travel to all of the farms """
m.setObjective(quicksum(X[f, p] * Distance[f][p] * TRound for f in F for p in P), GRB.MINIMIZE)

# CONSTRAINTS

# processing facility daily limits
for p in P:
    # maximum daily capacity is not exceeded for each processing facility
    m.addConstr(quicksum(X[f,p] * Supply[f] for f in F) <= PMax[p])

    # minimum processing requirement is met for each processing facility
    m.addConstr(quicksum(X[f,p] * Supply[f] for f in F) >= PMin[p])

for f in F:
    # each farm must only be assigned to one processing plant
    m.addConstr(quicksum(X[f,p] for p in P) == 1)

m.optimize()

# Print Gurobi solver status
if m.status == GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print(f"\n{'Totals'}\n{'-'*65}")
print(f"{'Total cost of travel:': <20} ${int(m.objVal)}\n")
for p in P:
    print(f"{'Total travel for'} {Facilities[p]}: ${int(quicksum(X[f,p].x * Distance[f][p] * TRound for f in F).getValue()): <20}")
print("\n")

for p in P:
    print(f"PROCESSING FACILITY {P[p]}")
    print(f"{'-'*65}\n{'Farms': <18} {'Dist. (km)': <15} {'Cost ($)': <15} {'Supply (L)': <15}\n{'-'*65}")
    for f in F:
        if X[f,p].x:
            print(f"{Farms[f]: <18} {Distance[f][p]: <15} {Distance[f][p]*TRound: <15} {Supply[f]: <15}")
    print(f"{'-'*65}")

    print(f"{' '*18} {int(quicksum(X[f,p].x * Distance[f][p] for f in F).getValue()): <15}" , end='')
    print(f" {int(quicksum(X[f,p].x * Distance[f][p] * TRound for f in F).getValue()): <15} {int(quicksum(X[f,p].x * Supply[f] for f in F).getValue())} / {PMax[p]}\n")
