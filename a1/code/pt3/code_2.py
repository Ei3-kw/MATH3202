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

Supply = [9600, 5300, 9300, 9200, 7100]
Fat = [3.4, 3.6, 3.8, 3.6, 3.7]
Organic = [False, False, False, True, True]

# Create a new model
m = gp.Model("Comm3")

# Create variables
w = {}
x = {}
y = {}
z = {}
for f in F:
    w[f] = m.addVar(lb=0, ub=Supply[f], name=f"whole organic - {Farms[f]}")
    x[f] = m.addVar(lb=0, ub=Supply[f], name=f"low fat organic - {Farms[f]}") 
    y[f] = m.addVar(lb=0, ub=Supply[f], name=f"whole normal - {Farms[f]}")
    z[f] = m.addVar(lb=0, ub=Supply[f], name=f"low fat normal - {Farms[f]}")

# Set objective function
m.setObjective(gp.quicksum(O_w * w[f] + O_l * x[f] + 
                           C_w * y[f] + C_l * z[f] 
                           for f in F), gp.GRB.MAXIMIZE)

# Add constraints
for f in F:
    # the sum of all milk produced from each farm must equal supply
    m.addConstr(w[f] + x[f] + y[f] + z[f] == Supply[f])
    
    # if a farm is not organic, no organic milk can be produced from the supply
    if not Organic[f]:
        m.addConstr(w[f] == 0)
        m.addConstr(x[f] == 0)

# total fat content of products is less than or equal to fat content of supply
m.addConstr(gp.quicksum(F_w * (w[f] + y[f]) + F_l * (x[f] + z[f]) for f in F) <= 
            gp.quicksum(Supply[f] * Fat[f] for f in F))

# fat content of organic products is less than or equal to fat content of supply
m.addConstr(gp.quicksum(F_w * w[f] + F_l * x[f] for f in F) <= 
            gp.quicksum(Supply[f] * Fat[f] for f in F if Organic[f]))

# low fat milk is 25% of the total for each of organic and normal products
m.addConstr(0.25 * gp.quicksum(w[f] + x[f] for f in F) >= gp.quicksum(x[f] for f in F))
m.addConstr(0.25 * gp.quicksum(y[f] + z[f] for f in F) >= gp.quicksum(z[f] for f in F))
    
# organic products is at most 15% of all milk 
m.addConstr(.15 * gp.quicksum(Supply[f] for f in F) - gp.quicksum(w[f] + x[f] for f in F) >= 0)

# Solve it!
m.optimize()

print(f"Total income: {m.objVal}")
print("\nTotal:\n-------------------------------------------------")
print(f"\
        Whole organic - {sum(m.getVarByName(f'whole organic - {Farms[f]}').X for f in F)}\n\
        Low fat organic - {sum(m.getVarByName(f'low fat organic - {Farms[f]}').X for f in F)}\n\
        Whole - {sum(m.getVarByName(f'whole normal - {Farms[f]}').X for f in F)}\n\
        Low fat - {sum(m.getVarByName(f'low fat normal - {Farms[f]}').X for f in F)}\n")

print("\nBreakdown\n----------------------------------------------")
for f in F:
    print(f"{Farms[f]}: \n\
        Whole organic - {m.getVarByName(f'whole organic - {Farms[f]}').X}\n\
        Low fat organic - {m.getVarByName(f'low fat organic - {Farms[f]}').X}\n\
        Whole - {m.getVarByName(f'whole normal - {Farms[f]}').X}\n\
        Low fat - {m.getVarByName(f'low fat normal - {Farms[f]}').X}\n")
