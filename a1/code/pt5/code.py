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
W_w = .9    # whole milk price
W_l = .92   # low fat milk price
F_w = 4.0   # whole milk fat content
F_l = 1.0   # low fat milk fat content
C_s = .05   # cost of storage per litre per day

# Change this if needed for different data

# Supply = [9600, 5300, 9300, 9200, 7100]
# Fat = [3.4, 3.6, 3.8, 3.6, 3.7]

Supply = [8700, 5400, 8800, 5400, 8900, 9300]
Fat = [3.3, 3.8, 3.6, 3.4, 3.5, 3.8]
Demand = [(13778, 3485), (27488, 6896), 
          (68427, 17060), (13740, 3543), 
          (27428, 6756), (27519, 6794), 
          (82193, 20733)]

# Create a new model 
m = gp.Model()

# Create variables
# Note: processed milk from each farm is bounded by the supply of each farm 
x = {(t, f): m.addVar(lb=0, ub=Supply[f], name=f"wholesale whole - {Farms[f]} {Days[t]}") for f in F for t in T}
y = {(t, f): m.addVar(lb=0, ub=Supply[f], name=f"wholesale low fat - {Farms[f]} {Days[t]}") for f in F for t in T}

# Note: there is no upper bound on the volume of stored milk
z = {t: m.addVar(lb=0, name=f"whole storage - {Days[t]}") for t in T} 
w = {t: m.addVar(lb=0, name=f"low fat storage - {Days[t]}") for t in T} 

# Note: milk sold each day is bounded by demand for the day 
# (this is sufficent for satisfying the implicit constraint on demand, i.e., daily demand cannot be exceeded)
a = {t: m.addVar(lb=0, ub=Demand[t][0], name=f"whole milk sold on {Days[t]}") for t in T}
b = {t: m.addVar(lb=0, ub=Demand[t][1], name=f"low fat milk sold on {Days[t]}") for t in T}

# Set objective function
m.setObjective(gp.quicksum(W_w * a[t] + W_l * b[t] for t in T) -    # income from whole milk and low fat milk sold
               gp.quicksum(z[t] + w[t] for t in T) * C_s,           # cost of storage
               gp.GRB.MAXIMIZE)

# Add constraints

C = {}      # constraints on supply
D_w = {}    # constraints on demand for whole milk 
D_l = {}    # constraints on demand for low fat milk
E = {}      # constraints on fat percentage 

for t in T:
    
    # each day, the volume of sold milk for each of the varieties cannot exceed demand for that variety
    D_w[t] = m.addConstr(a[t] <= Demand[t][0])
    D_l[t] = m.addConstr(b[t] <= Demand[t][1])

    # the total milk processed each day from each farm is less than or equal to the daily supply of that farm
    for f in F:
        C[(t,f)] = m.addConstr(x[t,f] + y[t,f] <= Supply[f])
    
    # each day cumulative fat content of processed milk is less than or equal to the fat content of supply
    # it is assumed that unused fat from previous days cannot be used later 
    E[t] = m.addConstr(gp.quicksum(F_w * x[t,f] + F_l * y[t,f] for f in F) <= 
                       gp.quicksum(Supply[f] * Fat[f] for f in F))
    
    if t == 0:
        # stored milk equals processed milk minus sold milk 
        m.addConstr(z[t] == gp.quicksum(x[t,f] for f in F) - a[t])
        m.addConstr(w[t] == gp.quicksum(y[t,f] for f in F) - b[t])

    else:
        # stored milk equals processed milk and stored milk from yesterday minus sold milk 
        m.addConstr(z[t] == gp.quicksum(x[t,f] for f in F) + z[t-1] - a[t])
        m.addConstr(w[t] == gp.quicksum(y[t,f] for f in F) + w[t-1] - b[t])

        # sold milk must be greater than or equal to milk stored from yesterday
        m.addConstr(a[t] >= z[t-1])
        m.addConstr(b[t] >= w[t-1])

   
# Solve it!
m.optimize()

# Print Gurobi solver status
if m.status == gp.GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print("\nTotals\n----------------------------------------------------")
print(f"Total income: {round(m.objVal, 2)}")
print(f"\nTotal whole milk sold:   {round(sum(m.getVarByName(f'whole milk sold on {Days[t]}').X for t in T), 2)}")
print(f"Total low fat milk sold: {round(sum(m.getVarByName(f'low fat milk sold on {Days[t]}').X for t in T), 2)}")

print("\nWeekly breakdown\n----------------------------------------------------")
print("\nSales:\nCategory               Day      Sold(L) / Demand(L)\n----------------------------------------------------")
for t in T:
    print(f"Whole sold          on {Days[t]}      {round(m.getVarByName(f'whole milk sold on {Days[t]}').X, 2)} / {round(Demand[t][0], 2)}")
    print(f"Low fat sold        on {Days[t]}      {round(m.getVarByName(f'low fat milk sold on {Days[t]}').X, 2)} / {round(Demand[t][1], 2)}\n")

print("\nStorage:\nCategory               Day      Amount(L)\n----------------------------------------------------")
for t in T:
    print(f"Whole               on {Days[t]}      {round(m.getVarByName(f'whole storage - {Days[t]}').X, 2)}")
    print(f"Low fat             on {Days[t]}      {round(m.getVarByName(f'low fat storage - {Days[t]}').X, 2)}\n")

print("\nBreakdown by Farms\n----------------------------------------------------")
for f in F:
    print(f"\n{Farms[f]}\nCategory               Day      Produced(L)\n----------------------------------------------------")
    for t in T:
        print(f"Whole produced      on {Days[t]}      {round(m.getVarByName(f'wholesale whole - {Farms[f]} {Days[t]}').X, 2)}")
        print(f"Low fat produced    on {Days[t]}      {round(m.getVarByName(f'wholesale low fat - {Farms[f]} {Days[t]}').X, 2)}\n")



print("\nConstraint Analysis\n----------------------------------------------------------------------")
for f in F:
    print(f"\n{Farms[f]}")
    print(f"Category             Day     Dual     Slack      RHS      Low          Up\n----------------------------------------------------------------------")
    for t in T:
        print(f"Supply            on {Days[t]} {round(C[(t,f)].Pi, 4):8.2f}  {round(C[(t,f)].Slack, 4):8.2f}   {round(C[(t,f)].RHS, 4):8.2f}     {round(C[(t,f)].SARHSLow, 4):8.2f}     {round(C[(t,f)].SARHSUp, 4):8.2f}")


print(f"\nCategory             Day     Dual     Slack          RHS         Low          Up\n----------------------------------------------------------------------")
for t in T:
        print(f"Demand - Whole    on {Days[t]}{round(D_w[t].Pi, 4):9.2f}  {round(D_w[t].RHS, 4):9.2f}   {round(D_w[t].Slack, 4):9.2f}   {round(D_w[t].SARHSLow, 4):9.2f}   {round(D_w[t].SARHSUp, 4):9.2f}")
        print(f"Demand - Low fat  on {Days[t]}{round(D_l[t].Pi, 4):9.2f}  {round(D_l[t].RHS, 4):9.2f}   {round(D_l[t].Slack, 4):9.2f}   {round(D_l[t].SARHSLow, 4):9.2f}   {round(D_l[t].SARHSUp, 4):9.2f}")
        print(f"Fat Percentage    on {Days[t]}{round(E[t].Pi, 4):9.2f}  {round(D_l[t].RHS, 4):9.2f}   {round(E[t].Slack, 4):9.2f}   {round(E[t].SARHSLow, 4):9.2f}   {round(E[t].SARHSUp, 4):9.2f}\n")


print("\nVariable Analysis\n--------------------------------------------------------------------")
print(f"Category              Day      RC        Low       Obj       Up\n--------------------------------------------------------------------")
for t in T:
    #print(f"\n{Days[t]}\n----------------------------------------------------------------")
    print(f"Whole sold         on {Days[t]}     {round(a[t].RC, 4):5.2f}     {round(a[t].SAObjLow, 4):5.2f}     {round(a[t].Obj, 4):5.2f}     {round(a[t].SAObjUp, 4):5.2f}")
    print(f"Low fat sold       on {Days[t]}     {round(b[t].RC, 4):5.2f}     {round(b[t].SAObjLow, 4):5.2f}     {round(b[t].Obj, 4):5.2f}     {round(b[t].SAObjUp, 4):5.2f}")
    print(f"Whole stored       on {Days[t]}     {round(z[t].RC, 4):5.2f}     {round(z[t].SAObjLow, 4):5.2f}     {round(z[t].Obj, 4):5.2f}     {round(z[t].SAObjUp, 4):5.2f}")
    print(f"Low fat stored     on {Days[t]}     {round(w[t].RC, 4):5.2f}     {round(w[t].SAObjLow, 4):5.2f}     {round(w[t].Obj, 4):5.2f}     {round(w[t].SAObjUp, 4):5.2f}\n")

