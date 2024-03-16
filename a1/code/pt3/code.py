import sys
import gurobipy as gp

# Sets
Farms = ['Barnwood',
         'Thistlebrook',
         'Rustic Ranch',
         'Haven',
         'Silo Springs']

F = range(len(Farms))

# Data
O_w = 1.30      # organic whole milk ($/L)
O_l = 1.32      # organic low fat milk ($/L)
C_w = 1.10      # non-organic whole milk ($/L)
C_l = 1.12      # non-organic low fat milk ($/L)
F_w = 4.0       # fat content of processed whole milk (%)
F_l = 1.0       # fat content of processed low fat milk (%)
MaxLow = 0.25   # max percentage of product that can be low fat (%)
MaxOrg = 50     # max percentage of product that can be organic (%)

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
m.setObjective(gp.quicksum(O_w * w[f] + O_l * x[f] + C_w * y[f] + C_l * z[f] for f in F), gp.GRB.MAXIMIZE)

C = {}

# Add constraints
for f in F:
    # for each farm, the sum of milk processed from that farm must equal supply
    C[f"Supply - {Farms[f]}"] = m.addConstr(w[f] + x[f] + y[f] + z[f] == Supply[f])
    
    # if a farm is not organic, no organic milk can be produced from the supply
    if not Organic[f]:
        m.addConstr(w[f] == 0)
        m.addConstr(x[f] == 0)

# the total fat content of processed milk is less than or equal to the fat content of the input
C["Total fat"] = m.addConstr(gp.quicksum(F_w * (w[f] + y[f]) + F_l * (x[f] + z[f]) for f in F) <=
                             gp.quicksum((w[f] + x[f] + y[f] + z[f]) * Fat[f] for f in F))
    
# fat content of organic products is less than or equal to fat content of its input
C["Organic fat"] = m.addConstr(gp.quicksum(F_w * w[f] + F_l * x[f] for f in F) <= 
                               gp.quicksum((w[f] + x[f]) * Fat[f] for f in F))

# low fat milk is 25% of the total for each of organic and normal products
m.addConstr(MaxLow * gp.quicksum(w[f] + x[f] for f in F) >= gp.quicksum(x[f] for f in F))
m.addConstr(MaxLow * gp.quicksum(y[f] + z[f] for f in F) >= gp.quicksum(z[f] for f in F))
    
# organic products is at most 15% of all milk 
C["Organic proportion"] =  m.addConstr(100 * gp.quicksum(w[f] + x[f] for f in F)/ sum(Supply[f] for f in F) <= MaxOrg)

# Solve it!
m.optimize()

print(f"\nTotal income: {m.objVal}")

print("\nTotal\n-------------------------------------------------")
print(f"\
        Whole organic     {sum(m.getVarByName(f'whole organic - {Farms[f]}').X for f in F):8.2f}\n\
        Low fat organic   {sum(m.getVarByName(f'low fat organic - {Farms[f]}').X for f in F):8.2f}\n\
        Whole             {sum(m.getVarByName(f'whole normal - {Farms[f]}').X for f in F):8.2f}\n\
        Low fat           {sum(m.getVarByName(f'low fat normal - {Farms[f]}').X for f in F):8.2f}\n")

print("\nBreakdown\n-------------------------------------------------")
for f in F:
    print(f"{Farms[f]}: \n\
        Whole organic     {m.getVarByName(f'whole organic - {Farms[f]}').X:8.2f}\n\
        Low fat organic   {m.getVarByName(f'low fat organic - {Farms[f]}').X:8.2f}\n\
        Whole             {m.getVarByName(f'whole normal - {Farms[f]}').X:8.2f}\n\
        Low fat           {m.getVarByName(f'low fat normal - {Farms[f]}').X:8.2f}\n")


print("\nConstraint Analysis\n--------------------------------------------------------------------")
print(f"Category                  Dual       Slack         Low          Up\n--------------------------------------------------------------------")
for f in F:
    print(f"\n{Farms[f]}:")
    print(f"Supply            \
    {round(C[f'Supply - {Farms[f]}'].Pi, 4):8.2f}\
    {round(C[f'Supply - {Farms[f]}'].Slack, 4):8.2f}\
    {round(C[f'Supply - {Farms[f]}'].SARHSLow, 4):8.2f}\
    {round(C[f'Supply - {Farms[f]}'].SARHSUp, 4):8.2f}")
    print(f"Organic Supply    \
    {round(Organic[f]*C[f'Supply - {Farms[f]}'].Pi, 4):8.2f}\
    {round(Organic[f]*C[f'Supply - {Farms[f]}'].Slack, 4):8.2f}\
    {round(Organic[f]*C[f'Supply - {Farms[f]}'].SARHSLow, 4):8.2f}")

print(f"\nTotal fat         \
    {round(C['Total fat'].Pi, 4):8.2f}\
    {round(C['Total fat'].Slack, 4):8.2f}\
    {round(C['Total fat'].SARHSLow, 4):8.2f}\
   {round(C['Total fat'].SARHSUp, 4):8.2f}")
print(f"Organic fat       \
    {round(C['Organic fat'].Pi, 4):8.2f}\
    {round(C['Organic fat'].Slack, 4):8.2f}\
    {round(C['Organic fat'].SARHSLow, 4):8.2f}\
    {round(C['Organic fat'].SARHSUp, 4):8.2f}")
print(f"Organic proportion\
    {round(C['Organic proportion'].Pi, 4):8.2f}\
    {round(C['Organic proportion'].Slack, 4):8.2f}\
    {round(C['Organic proportion'].SARHSLow, 4):8.2f}\
    {round(C['Organic proportion'].SARHSUp, 4):8.2f}")


print("\n\nVariable Analysis\n--------------------------------------------------------------------")
print(f"Category                   RC        Low       Obj       Up\n--------------------------------------------------------------------")
for f in F:
    print(f"{Farms[f]}:")
    print(f"Whole organic             {round(w[f].RC, 4):5.2f}     {round(w[f].SAObjLow, 4):5.2f}     {round(w[f].Obj, 4):5.2f}     {round(w[f].SAObjUp, 4):5.2f}")
    print(f"Low fat organic           {round(x[f].RC, 4):5.2f}     {round(x[f].SAObjLow, 4):5.2f}     {round(x[f].Obj, 4):5.2f}     {round(x[f].SAObjUp, 4):5.2f}")
    print(f"Whole normal              {round(y[f].RC, 4):5.2f}     {round(y[f].SAObjLow, 4):5.2f}     {round(y[f].Obj, 4):5.2f}     {round(y[f].SAObjUp, 4):5.2f}")
    print(f"Low fat normal            {round(z[f].RC, 4):5.2f}     {round(z[f].SAObjLow, 4):5.2f}     {round(z[f].Obj, 4):5.2f}     {round(z[f].SAObjUp, 4):5.2f}\n")

