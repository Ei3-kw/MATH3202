from gurobipy import * 

# Sets
milk = ["Low Fat", "Full Cream"]
farms = ['Barnwood', 'Thistlebrook', 'Rustic Ranch', 'Haven', 'Silo Springs']

M = range(len(milk))
F = range(len(farms))

# Data
income = [1.10, 1.12]
fat_product = [4, 1]

supply = [5400, 7200, 7600, 5700, 7000]
fat = [3.8, 3.6, 3.3, 3.3, 3.7]

model = Model("Teal Cow Dairy")

X = {}
for m in M:
    X[m] = model.addVar(vtype=GRB.CONTINUOUS)

# Objective
model.setObjective(quicksum(income[m]*X[m] for m in M), GRB.MAXIMIZE)

# Constraints
model.addConstr(quicksum(X[m] for m in M) == quicksum(supply[f] for f in F))
model.addConstr(quicksum(X[m]*(fat_product[m] / 100) for m in M) 
            == quicksum(supply[f]*(fat[f] / 100) for f in F))

model.optimize()

print("Income is", model.objVal)
for m in M:
    print("Produce", X[m].x, milk[m])
