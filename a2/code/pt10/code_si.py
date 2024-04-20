from gurobipy import *
from Milkruns2 import *

# SETS
Farms = ['Cowbell', 'Creamy Acres', 'Milky Way', 'Happy Cows', 'Udder Delight', 
         'Fresh Pail', 'Cowabunga', 'Utopia', 'Moo Meadows', 'Bluebell', 
         'Harmony', 'Velvet Valley', 'Moonybrook', 'Cloven Hills', 'Midnight Moo', 
         'Willows Bend', 'Moosa Heads', 'Dreamy Dairies', 'Happy Hooves', 'Highlands']

Facilities = ['PF0', 'PF1', 'PF2']

Tankers = ['Tanker 1', 'Tanker 2', 'Tanker 3', 'Tanker 4', 'Tanker 5']

MilkTypes = ['Non-Organic', 'Organic']  

F = range(len(Farms))
P = range(len(Facilities))
T = range(len(Tankers))
R = range(len(Milkruns))
K = range(len(MilkTypes))

# DATA
Supply = [5200, 9900, 8800, 6900, 9500, 5900, 3700, 4800, 3200, 3400, 
          4400, 4500, 3200, 4800, 3100, 3400, 3000, 4500, 4500, 3900]

PMin = [20000,24000,32000]  # maximum daily capacity (litres)
PMax = [45000,35000,36000]  # minimum daily processing (litres)

Maintenance = [500, 470, 440, 410, 380]  # cost of tanker maintenance for each tanker t in T ($/day)

MMax         = 600  # maximum number of minutes a tanker can be used for (min)
DeepClean    = 100  # cost of performing a deep clean between organic and non-organic runs ($)
BetweenFarms = 15   # delay between farms on a milk run (min)
BetweenRuns  = 60   # cleaning time between milk runs (min)

# constants for indexing the Milkruns array 
PF      = 0
FARMS   = 1
TIME    = 2
COST    = 3
ORGANIC = 4

# MODEL
m = Model('Comm 10')

# VARIABLES
U = {(p, t, k): m.addVar(vtype=GRB.BINARY, name=f"indicates whether a tanker is assigned organic or non-organic milk runs") for p in P for t in T for k in K}
V = {(p, t): m.addVar(vtype=GRB.BINARY, name=f"indicates whether a tanker does both organic and non-organic milk runs") for p in P for t in T}
W = {(p, t): m.addVar(vtype=GRB.BINARY, name=f"indicates whether a tanker in the fleet is operational") for p in P for t in T}
X = {(p, r, t): m.addVar(vtype=GRB.BINARY, name=f"route and tanker assignment per processing facility") for p in P for r in R for t in T}
Y = {(p, r, t): m.addVar(lb=0, vtype=GRB.INTEGER, name=f"total extra minutes between farms on a milk run") for p in P for r in R for t in T}
Z = {(p, t): m.addVar(lb=0, vtype=GRB.INTEGER, name=f"number of routes each tanker is assigned to") for p in P for t in T}

# OBJECTIVE
""" select tanker routes which minimise the cost of collections """
m.setObjective(quicksum(X[p,r,t] * Milkruns[r][COST] for p in P for r in R for t in T) +                    # cost for travel
               quicksum(W[p,t] * Maintenance[t] + V[p,t] * DeepClean for p in P for t in T), GRB.MINIMIZE)  # cost for maintenance and cleaning

# CONSTRAINTS
for p in P:
    # maximum daily capacity is not exceeded for each processing facility
    m.addConstr(quicksum(X[p,r,t] * Supply[f] for r in R for t in T for f in F if f in Milkruns[r][FARMS]) <= PMax[p])

    # minimum processing requirement is met for each processing facility
    m.addConstr(quicksum(X[p,r,t] * Supply[f] for r in R for t in T for f in F if f in Milkruns[r][FARMS]) >= PMin[p])

    for t in T:
        # tankers are operational (including breaks) for at most 10 hours (600 minutes)
        m.addConstr(quicksum(X[p,r,t] * Milkruns[r][TIME] + Y[p,r,t] for r in R) + (Z[p,t] - W[p,t]) * BetweenRuns <= MMax)

        # number of routes a tanker is assigned to equals the sum of route assignments to that tanker and processing facility
        m.addConstr(Z[p,t] == quicksum(X[p,r,t] for r in R))
        
        # if a tanker has both organic and non-organic milk runs, set the binary variable to indicate this
        m.addConstr(V[p,t] == (quicksum(U[p,t,k] for k in K) - W[p,t]))

        for r in R:
            if Milkruns[r][ORGANIC]:
                # if a run is used and is organic, set the binary variable to indicate this
                m.addConstr(U[p,t,1] >= X[p,r,t])

            else:
                # if a run is used and is non-organic, set the binary variable to indicate this
                m.addConstr(U[p,t,0] >= X[p,r,t])

            # for processing facility p, if the Milkrun does not originate from p the tanker cannot be assigned to this route
            if Milkruns[r][PF] != p:
                m.addConstr(X[p,r,t] == 0)

            # if a tanker is used, set the binary variable to indicate this
            m.addConstr(W[p,t] >= X[p,r,t])

            if len(Milkruns[r][FARMS]) > 0:
                # for each used milk run that visits multiple farms, record the required number of minutes for breaks 
                m.addConstr(Y[p,r,t] == X[p,r,t] * (len(Milkruns[r][FARMS]) - 1) * BetweenFarms)

            else:
                # if there is only one farm on the route, there is no need for breaks 
                m.addConstr(Y[p,r,t] == 0)

        # tankers must be used in order (this way the cheaper maintenance fees are not automatically applied)
        if t > 0:
            m.addConstr(W[p,t] <= W[p,t-1])

for f in F:
    # every farm needs to be visited on one of the routes 
    m.addConstr(quicksum(X[p,r,t] for p in P for r in R for t in T if f in Milkruns[r][FARMS]) == 1)

m.optimize()

if m.status == GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print(f"\n{'TOTALS'}\n{'-'*52}")
print(f"{'Total cost of collections:': <20} ${int(m.objVal)}\n")

print(f"{'-'*52}\n{'Facility': <10} {'Travel ($)': <12} {'Maintenance ($)': <17} {'Total ($)': <15}\n{'-'*52}")
for p in P:
    print(f"{Facilities[p]: <10} {int(quicksum(X[p,r,t].x * Milkruns[r][COST] for r in R for t in T).getValue()): <12}", end='')
    print(f" {int(quicksum(W[p,t] * Maintenance[t] for t in T).getValue()): <17}", end='')
    print(f" {int(quicksum(X[p,r,t].x * Milkruns[r][COST] for r in R for t in T).getValue() + quicksum(W[p,t] * Maintenance[t] for t in T).getValue())}")
print(f"{'-'*52}\n")

for p in P:
    supply = 0
    time = 0
    cost = 0
    breaks = 0
    cleaning = 0

    # calculate total cleaning time between runs for each processing facility 
    for t in T:
        cleaning += (Z[p,t].x - W[p,t].x) * BetweenRuns

    print(f"PROCESSING FACILITY {p}")
    print(f"{'-'*110}\n{'Run': <6} {'Farms': <16} {'Milktype': <15} {'Travel (min)': <15} {'Breaks (min)': <15} {'Cost ($)': <11} {'Tanker': <11} {'Supply (L)': <15}\n{'-'*110}")
    for r in R:
        for t in T:
            if X[p,r,t].x:
                for i in range(len(Milkruns[r][FARMS])):
                    if i == 0:
                        print(f"{r: <6} {Farms[Milkruns[r][FARMS][i]]: <16} {MilkTypes[Milkruns[r][ORGANIC]]: <15} {Milkruns[r][TIME]: <15} {Y[p,r,t].x: <15.0f} {Milkruns[r][COST]: <11} {Tankers[t]: <11} {Supply[Milkruns[r][FARMS][i]]: <15}")
                        time += Milkruns[r][TIME]
                        cost += Milkruns[r][COST]
                        breaks += Y[p,r,t].x
                    else:
                        print(f"{' '*6} {Farms[Milkruns[r][FARMS][i]]: <16} {' '*15} {' '*15} {' '*15} {' '*11} {' '*11} {Supply[Milkruns[r][FARMS][i]]: <15}")
                    supply += Supply[Milkruns[r][FARMS][i]]
    print(f"{'-'*110}")
    print(f"{' '*6} {' '*16} {' '*15} {time: <15} {breaks: <2.0f} {'(+'} {cleaning: <3.0f}{')': <6} {cost: <11} {' '*11} {supply} / {PMax[p]}\n")

