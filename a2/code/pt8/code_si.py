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

F = range(len(Farms))
P = range(len(Facilities))
T = range(len(Tankers))
R = range(len(Milkruns))

# DATA
Supply = [5200, 9900, 8800, 6900, 
          9500, 5900, 3700, 4800, 
          3200, 3400, 4400, 4500, 
          3200, 4800, 3100, 3400, 
          3000, 4500, 4500, 3900]


PMin = [20000,24000,32000]  # maximum daily capacity (litres)
PMax = [45000,35000,36000]  # minimum daily processing (litres)

Maintenance = [500, 470, 440, 410, 380]     # cost of tanker maintenance for each tanker t in T ($/day)

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
W = {(p, t): m.addVar(vtype=GRB.BINARY, name=f"binary variable for whether a tanker in the fleet is operational") for p in P for t in T}
X = {(p, r, t): m.addVar(vtype=GRB.BINARY, name=f"route and tanker assignment per processing facility") for p in P for r in R for t in T}

# OBJECTIVE
""" select tanker routes which minimise the total cost of collections """
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

        for r in R:
            # for each processing facility p, if the Milkrun does not originate from p the tanker cannot be assigned to this route
            if Milkruns[r][PF] != p:
                m.addConstr(X[p,r,t] == 0)

            # if a tanker is used, set the binary variable to indicate this
            m.addConstr(W[p,t] >= X[p,r,t])

        if t > 0:
            # tankers must be used in order (this way the cheaper maintenance fees are not automatically applied)
            m.addConstr(W[p,t] <= W[p,t-1])

for f in F:
    # every farm needs to be visited on one of the assigned routes 
    m.addConstr(quicksum(X[p,r,t] for p in P for r in R for t in T if f in Milkruns[r][FARMS]) == 1)

m.optimize()

if m.status == GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print(f"\n{'TOTALS'}\n{'-'*55}")
print(f"{'Total cost of collections:': <20} ${int(m.objVal)}\n")

print(f"{'-'*55}\n{'Facility': <11} {'Travel ($)': <13} {'Maintenance ($)': <18} {'Total ($)': <16}\n{'-'*55}")

for p in P:
    print(f"{Facilities[p]: <11} {int(quicksum(X[p,r,t].x * Milkruns[r][COST] for r in R for t in T).getValue()): <13}", end='')
    print(f" {int(quicksum(W[p,t] * Maintenance[t] for t in T).getValue()): <18}", end='')
    print(f" {int(quicksum(X[p,r,t].x * Milkruns[r][COST] for r in R for t in T).getValue() + quicksum(W[p,t] * Maintenance[t] for t in T).getValue())}")
print(f"{'-'*55}\n")

for p in P:
    supply = 0
    print(f"PROCESSING FACILITY {p}")
    print(f"{'-'*78}\n{'Run': <6} {'Farms': <18} {'Time (min)': <13} {'Cost ($)': <11} {'Tanker': <11} {'Supply (L)': <16}\n{'-'*78}")
    for r in R:
        for t in T:
            if X[p,r,t].x:
                for i in range(len(Milkruns[r][FARMS])):
                    if i == 0:
                        print(f"{r: <6} {Farms[Milkruns[r][FARMS][i]]: <18} {Milkruns[r][TIME]: <13} {Milkruns[r][COST]: <11} {Tankers[t]: <11} {Supply[Milkruns[r][FARMS][i]]: <16}")
                    else:
                        print(f"{' '*6} {Farms[Milkruns[r][FARMS][i]]: <18} {' '*13} {' '*11} {' '*11} {Supply[Milkruns[r][FARMS][i]]: <16}")
                    supply += Supply[Milkruns[r][FARMS][i]]
    print(f"{'-'*78}")
    print(f"{' '*6} {' '*18} {' '*13} {' '*11} {' '*11} {supply} / {PMax[p]}\n")

