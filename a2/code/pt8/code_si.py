from gurobipy import *
from Milkruns import *

# SETS
Farms = ['Cowbell', 'Creamy Acres', 'Milky Way', 'Happy Cows', 
         'Udder Delight', 'Fresh Pail', 'Cowabunga', 'Utopia', 
         'Moo Meadows', 'Bluebell', 'Harmony', 'Velvet Valley', 
         'Moonybrook', 'Cloven Hills', 'Midnight Moo', 'Willows Bend', 
         'Moosa Heads', 'Dreamy Dairies', 'Happy Hooves', 'Highlands']

Facilities = ['PF0', 'PF1', 'PF2']

Tankers = ['Tanker 1', 'Tanker 2', 'Tanker 3', 'Tanker 4', 'Tanker 5']

# DATA
Supply = [5200, 9900, 8800, 6900, 
          9500, 5900, 3700, 4800, 
          3200, 3400, 4400, 4500, 
          3200, 4800, 3100, 3400, 
          3000, 4500, 4500, 3900]

F = range(len(Farms))
P = range(len(Facilities))
T = range(len(Tankers))
R = range(len(Milkruns))

PMin = [20000,24000,32000]  # maximum daily capacity (litres)
PMax = [45000,35000,36000]  # minimum daily processing (litres)

Maintenance = [500, 470, 440, 410, 380]     # cost of tanker maintenance ($/day)

HMax = 10       # maximum number of hours a tanker can be used for (h)
MMax = 600      # maximum number of minutes a tanker can be used for (min)

# constants for indexing the Milkruns array 
PF    = 0
FARMS = 1
TIME  = 2
COST  = 3

# MODEL
m = Model('Comm 8')

# VARIABLES
W = {(p, t): m.addVar(vtype=GRB.BINARY, name=f"whether a tanker in the fleet is operational") for p in P for t in T}
X = {(p, r, t): m.addVar(vtype=GRB.BINARY, name=f"route and tanker assignment per processing facility") for p in P for r in R for t in T}

# OBJECTIVE
""" select tanker routes which minimise the cost of travel to all of the farms """
m.setObjective(quicksum(X[p,r,t] * Milkruns[r][COST] for p in P for r in R for t in T) +    # cost for travel
               quicksum(W[p,t] * Maintenance[t] for p in P for t in T), GRB.MINIMIZE)       # cost for maintenance

# CONSTRAINTS
for p in P:
    # maximum daily capacity is not exceeded for each processing facility
    m.addConstr(quicksum(X[p,r,t] * Supply[f] for r in R for t in T for f in F if f in Milkruns[r][FARMS]) <= PMax[p])

    # minimum processing requirement is met for each processing facility
    m.addConstr(quicksum(X[p,r,t] * Supply[f] for r in R for t in T for f in F if f in Milkruns[r][FARMS]) >= PMin[p])

    for t in T:
        # tankers are operational for at most 10 hours (600 minutes)
        m.addConstr(quicksum(X[p,r,t] * Milkruns[r][TIME] for r in R) <= MMax)

        # if a tanker is used, set the binary variable to indicate this
        for r in R:
            m.addConstr((X[p,r,t] == 1) >> (W[p,t] == 1))

        # tankers must be used in order (this way the cheaper maintenance fees are not automatically applied)
        if t > 0:
            m.addConstr((W[p,t] == 1) >> (W[p,t-1] == 1))

    for t in T:
        for r in R:
            # for processing facility p, if the Milkrun does not originate from p the tanker cannot be assigned to this route
            if Milkruns[r][PF] != p:
                m.addConstr(X[p,r,t] == 0)

for f in F:
    # every farm needs to be visited on one of the routes 
    m.addConstr(quicksum(X[p,r,t] for p in P for r in R for t in T if f in Milkruns[r][FARMS]) == 1)

m.optimize()

if m.status == GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print(f"\n{'-'*52}")
print(f"{'Total cost of travel:': <20} ${int(m.objVal)}\n")

print(f"{'-'*52}\n{'Facility': <10} {'Travel ($)': <12} {'Maintenance ($)': <17} {'Total ($)': <15}\n{'-'*52}")

for p in P:
    print(f"{Facilities[p]: <10} {int(quicksum(X[p,r,t].x * Milkruns[r][COST] for r in R for t in T).getValue()): <12}", end='')
    print(f" {int(quicksum(W[p,t] * Maintenance[t] for t in T).getValue()): <17}", end='')
    print(f" {int(quicksum(X[p,r,t].x * Milkruns[r][COST] for r in R for t in T).getValue() + quicksum(W[p,t] * Maintenance[t] for t in T).getValue())}")
print(f"{'-'*52}\n")

for p in P:
    supply = 0
    print(f"PROCESSING FACILITY {p}")
    print(f"{'-'*72}\n{'Run': <5} {'Farms': <15} {'Time (min)': <12} {'Cost ($)': <10} {'Tanker': <10} {'Supply (L)': <15}\n{'-'*72}")
    for r in R:
        for t in T:
            if X[p,r,t].x:
                for i in range(len(Milkruns[r][FARMS])):
                    if i == 0:
                        print(f"{r: <5} {Farms[Milkruns[r][FARMS][i]]: <15} {Milkruns[r][TIME]: <12} {Milkruns[r][COST]: <10} {Tankers[t]: <10} {Supply[Milkruns[r][FARMS][i]]: <15}")
                    else:
                        print(f"{' '*5} {Farms[Milkruns[r][FARMS][i]]: <15} {' '*12} {' '*10} {' '*10} {Supply[Milkruns[r][FARMS][i]]: <15}")
                    supply += Supply[Milkruns[r][FARMS][i]]
    print(f"{'-'*72}")
    print(f"{' '*5} {' '*15} {' '*12} {' '*10} {' '*10} {supply} / {PMax[p]}\n")

