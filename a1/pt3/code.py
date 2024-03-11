import gurobipy as gp

# Sets
Farms = ['Barnwood',
        'Thistlebrook',
        'Rustic Ranch',
        'Haven',
        'Silo Springs']

F = range(len(Farms))

# Data
O_w = 1.30
O_l = 1.32
C_w = 1.10
C_l = 1.12
F_w = 4.0
F_l = 1.0

# Change this if needed for different data
Supply = [9600, 5300, 9300, 9200, 7100]
Fat = [3.4, 3.6, 3.8, 3.6, 3.7]
# Supply = [5400, 7200, 7600, 5700, 7000]
# Fat = [3.8, 3.6, 3.3, 3.3, 3.7]
Organic = [0, 0, 0, 1, 1]

# Create a new model
m = gp.Model()

# Create variables
x = {}
y = {}
z = {}
for f in F:
    z[f] = m.addVar(lb=0, ub=Supply[f]*Organic[f], name=f"low fat organic - {Farms[f]}") 
    y[f] = m.addVar(lb=0, ub=Supply[f]*Organic[f], name=f"whole organic - {Farms[f]}")
    x[f] = m.addVar(lb=0, ub=Supply[f], name=f"whole normal - {Farms[f]}") 

# Set objective function
m.setObjective(gp.quicksum(O_w*y[f]+O_l*z[f]+C_w*x[f]+C_l*(Supply[f]-y[f]-z[f]-x[f]) for f in F), gp.GRB.MAXIMIZE)

# Add constraints
for f in F:
    m.addConstr(gp.quicksum(F_w*(x[f]+y[f])+F_l*(Supply[f]-x[f]-y[f]) for f in F) <= gp.quicksum(Supply[f]*Fat[f] for f in F))
    m.addConstr(gp.quicksum(F_w*y[f]+F_l*z[f] for f in F) <= gp.quicksum(Supply[f]*Fat[f]*Organic[f] for f in F))
    m.addConstr(y[f] <= Supply[f]*Organic[f]-z[f])
    m.addConstr(x[f] <= Supply[f]-y[f]-z[f])
    # pt3
    m.addConstr(gp.quicksum(y[f] for f in F) >= 3 * gp.quicksum(z[f] for f in F))
    m.addConstr(gp.quicksum(x[f] for f in F) >= 3 * gp.quicksum(Supply[f]-x[f]-y[f]-z[f] for f in F))
    m.addConstr(.15 * sum(Supply)- gp.quicksum(z[f] + y[f] for f in F) >= 0)

# Solve it!
m.optimize()

print(f"Total income: {m.objVal}")
print("\nTotal:\n-------------------------------------------------")
print(f"\
        Whole organic - {sum(m.getVarByName(f'whole organic - {Farms[f]}').X for f in F)}\n\
        Low fat organic - {sum(m.getVarByName(f'low fat organic - {Farms[f]}').X for f in F)}\n\
        Whole - {sum(m.getVarByName(f'whole normal - {Farms[f]}').X for f in F)}\n\
        Low fat - {sum(Supply[f] - m.getVarByName(f'whole normal - {Farms[f]}').X - m.getVarByName(f'low fat organic - {Farms[f]}').X - m.getVarByName(f'whole organic - {Farms[f]}').X for f in F)}\n")

print("\nBreakdown\n----------------------------------------------")
for f in F:
    print(f"{Farms[f]}: \n\
        Whole organic - {m.getVarByName(f'whole organic - {Farms[f]}').X}\n\
        Low fat organic - {m.getVarByName(f'low fat organic - {Farms[f]}').X}\n\
        Whole - {m.getVarByName(f'whole normal - {Farms[f]}').X}\n\
        Low fat - {Supply[f] - m.getVarByName(f'whole normal - {Farms[f]}').X - m.getVarByName(f'low fat organic - {Farms[f]}').X - m.getVarByName(f'whole organic - {Farms[f]}').X}\n")
