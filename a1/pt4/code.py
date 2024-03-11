import gurobipy as gp

# Sets
Farms = ['Cowbell',
        'Creamy Acres',
        'Milky Way',
        'Happy Cows',
        'Udder Delight',
        'Fresh Pail']

Days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

F = range(len(Farms))
T = range(len(Days))

# Data
W_w = .9
W_l = .92
F_w = 4.0
F_l = 1.0
C_s = .05

# Change this if needed for different data
# Supply = [9600, 5300, 9300, 9200, 7100]
# Fat = [3.4, 3.6, 3.8, 3.6, 3.7]
Supply = [8700, 5400, 8800, 5400, 8900, 9300]
Fat = [3.3, 3.8, 3.6, 3.4, 3.5, 3.8]
Demand = [(13778, 3485), (27488, 6896), (68427, 17060), (13740, 3543), (27428, 6756), (27519, 6794), (82193, 20733)]

# Create a new model
m = gp.Model()

# Create variables
x = {(t, f): m.addVar(lb=0, ub=Supply[f], name=f"wholesale whole - {Farms[f]} {Days[t]}") for f in F for t in T}
y = {(t, f): m.addVar(lb=0, ub=Supply[f], name=f"wholesale low fat - {Farms[f]} {Days[t]}") for f in F for t in T}
z = {t: m.addVar(lb=0, name=f"whole storage - {Days[t]}") for t in T} 
w = {t: m.addVar(lb=0, name=f"low fat storage - {Days[t]}") for t in T} 
a = {t: m.addVar(lb=0, ub=Demand[t][0], name=f"whole milk sold on {Days[t]}") for t in T}
b = {t: m.addVar(lb=0, ub=Demand[t][1], name=f"low fat milk sold on {Days[t]}") for t in T}

# Set objective function
m.setObjective(gp.quicksum(W_w*a[t] + W_l*b[t] for t in T)
    - gp.quicksum(z[t]+w[t] for t in T) * C_s,
    gp.GRB.MAXIMIZE)

# Add constraints
for t in T:
    for f in F:
        m.addConstr(x[t,f] + y[t,f] <= Supply[f])
    m.addConstr(gp.quicksum(F_w*x[t,f] + F_l*y[t,f] for f in F) <= sum(Supply[f] * Fat[f] for f in F))
    
    # storage
    if t == 0:
        m.addConstr(z[t] == gp.quicksum(x[t,f] for f in F) - a[t])
        m.addConstr(w[t] == gp.quicksum(y[t,f] for f in F) - b[t])
        m.addConstr(a[t] <= gp.quicksum(x[t,f] for f in F))
        m.addConstr(b[t] <= gp.quicksum(y[t,f] for f in F))
    else:
        m.addConstr(z[t] == gp.quicksum(x[t,f] for f in F) + z[t-1] - a[t])
        m.addConstr(w[t] == gp.quicksum(y[t,f] for f in F) + w[t-1] - b[t])
        m.addConstr(a[t] <= gp.quicksum(x[t,f] for f in F) + z[t-1])
        m.addConstr(b[t] <= gp.quicksum(y[t,f] for f in F) + w[t-1])

# Solve it!
m.optimize()

# Print Gurobi solver status
if m.status == gp.GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print(f"Total income: {m.objVal}")
print("\nBreakdown:\nCatogory               Day      Sold(L) / Demand(L)\n-------------------------------------------------")
for t in T:
    print(f"Whole sold          on {Days[t]}      {m.getVarByName(f'whole milk sold on {Days[t]}').X} / {Demand[t][0]}")
    print(f"Low fat sold        on {Days[t]}      {m.getVarByName(f'low fat milk sold on {Days[t]}').X} / {Demand[t][1]}\n")

print("\nStorage:\nCatogory               Day      Amount(L)\n-------------------------------------------------")
for t in T:
    print(f"wholesale           on {Days[t]}      {m.getVarByName(f'whole storage - {Days[t]}').X}")
    print(f"low fat             on {Days[t]}      {m.getVarByName(f'low fat storage - {Days[t]}').X}\n")