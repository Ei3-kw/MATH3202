import gurobipy as gp
import numpy as np

# Sets
Farms = ['Barnwood',
        'Thistlebrook',
        'Rustic Ranch',
        'Haven',
        'Silo Springs']

F = range(len(Farms))

# Data
C_w = 1.10
C_l = 1.12
F_w = 4.0
F_l = 1.0

Supply = [9600, 5300, 9300, 9200, 7100]

Fat = [3.4, 3.6, 3.8, 3.6, 3.7]


# Create a new model
m = gp.Model()

# Create variables
x = {}
for f in F:
    x[f] = m.addVar(lb=0, ub=Supply[f], name=Farms[f]) 

# Set objective function
m.setObjective(gp.quicksum(C_w*x[f]+C_l*(Supply[f]-x[f]) for f in F), gp.GRB.MAXIMIZE)

# Add constraints
for f in F:
    m.addConstr(gp.quicksum(F_w*x[f]+F_l*(Supply[f]-x[f]) for f in F) == gp.quicksum(Supply[f]*Fat[f] for f in F))
    
# Solve it!
m.optimize()

print(f"Total income: {m.objVal}")
print("\nTotal:\n-------------------------------------------------")
print(f"Whole - {sum(m.getVarByName(Farms[f]).X for f in F)}\nLow fat - {sum(Supply[f]-m.getVarByName(Farms[f]).X for f in F)}\n")
print("\nBreakdown\n----------------------------------------------")
for f in F:
    print(f"{Farms[f]}: \nWhole - {m.getVarByName(Farms[f]).X}\nLow fat - {Supply[f]-m.getVarByName(Farms[f]).X}\n")



