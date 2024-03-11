from gurobipy import * 

### Sets
milk = ["Whole", 
        "Low Fat"
        ]

farms = ["Cowbell",
         "Creamy Acres",
         "Milky Way",
         "Happy Cows",
         "Udder Delight",
         "Fresh Pail"
         ]

days = ["Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
        ]

M = range(len(milk))
F = range(len(farms))
D = range(len(days))

# Data
""" $/L for whole and low fat milk respectively """
wholesale_price = [0.90, 0.92]
fat_product = [4, 1]

supply = [5200, 9900, 8800, 6900, 9500, 5900]
fat = [3.6, 3.5, 3.8, 3.9, 3.6, 3.4]
#supply = [8700, 5400, 8800, 5400, 8900, 9300]
#fat = [3.3, 3.8, 3.6, 3.4, 3.5, 3.8]

# Milk demand Mon-Sun
demand = [[13743, 27313, 68179, 13716, 27426, 27338, 81674],
          [3337, 7007, 17097, 3391, 6935, 6937, 20428]]
#demand = [[13778, 27488, 68427, 13740, 27428, 27519, 82193],
#          [3485, 6896, 17060, 3543, 6756, 6794, 20733]]

StoreCost = 0.05

### Create new model
model = Model("Teal Cow Dairy")


### Variables
X = {(m,d): model.addVar() for m in M for d in D}

Y = {(m,d): model.addVar() for m in M for d in D}

# WR[m, d] is the volume of whole milk m refined on day d
WS = {(f,d): model.addVar() for f in F for d in D }

# LR[m, d] is the volume of low fat milk supplied by farm f on day d
LS = {(f,d): model.addVar() for f in F for d in D }


# WR[m, d] is the volume of whole milk m refined on day d
WR = {(f,d): model.addVar() for f in F for d in D }

# LR[m, d] is the volume of low fat milk supplied by farm f on day d
LR = {(f,d): model.addVar() for f in F for d in D }

# S[s, d] is the volume of milk m stored on day d
S = {(m,d): model.addVar() for m in M for d in D }


### Objective
""" Maximise the sum of the income from each milk """
model.setObjective(quicksum(wholesale_price[m] * X[m, d] for m in M for d in D) -   # total profit
                   quicksum(StoreCost * S[m, d] for m in M for d in D),             # minus storage
                   GRB.MAXIMIZE)

### Constraints

# Total produced milk is equal to total whole and low fat from each of the farms 
for d in D:
    model.addConstr(X[0,d] == quicksum(WS[f,d] for f in F))
    model.addConstr(X[1,d] == quicksum(LS[f,d] for f in F))

for d in D:
    model.addConstr(Y[0,d] == quicksum(WR[f,d] for f in F))
    model.addConstr(Y[1,d] == quicksum(LR[f,d] for f in F))

# Supply from each farm cannot exceed demand
for d in D:
    for f in F:
        model.addConstr(WR[f,d] + LR[f,d] == supply[f])

for d in D:
    for m in M:
        if d > 0:
            model.addConstr(X[m,d] == Y[m,d] - (S[m,d] - S[m,d-1]))
        else:
            model.addConstr(X[m,d] == Y[m,d] - S[m,d])

# Demand for each day must not be exceeded
for m in M:
    for d in D:
        model.addConstr(X[m,d] <= demand[m][d])

# Every day, the fat content of the product must be <= the fat content of the supply
for d in D:
    model.addConstr(quicksum(Y[m,d] * fat_product[m] for m in M) <= # fat content of produced milk
                    quicksum(supply[f] * fat[f] for f in F))        # fat content of supply milk

# Storage
for m in M:
    if d > 0:
        model.addConstr(S[m,d] == S[m,d-1] + Y[m,d] - X[m,d])
    else:
        model.addConstr(S[m,d] == Y[m,d] - X[m,d])

""" the sum of all produced milk must equal the sum of supply """
#for d in D:
#    model.addConstr(quicksum(Y[m, d] for m in M) == quicksum(P[f,d] for f in F))

model.optimize()

print("\n")
print("-----------------------------------------------------------")
print("INCOME:", round(model.objVal, 2), "\n")
print("Total sold whole milk:", sum(round(X[m, d].x, 2) for m in M for d in D if m == 0))
print("Total sold low fat milk:", sum(round(X[m, d].x, 2) for m in M for d in D if m == 1))
print("\n")

print("--- Breakdown by day --------------------------------------")
for d in D:
    print(days[d])
    print("  Sold:")
    for m in M:
        print("    ", milk[m], ":", round(X[m, d].x, 2), " / ", demand[m][d])
    print("  Stored:")
    for m in M:
        print("    ", milk[m], ":", round(S[m, d].x, 2), " / ", demand[m][d])
    print("\n")

for m in M:
    print(milk[m])
    for d in D:
        print(days[d])
        print(Y[m,d].x, " ")

for f in F:
    print(farms[f], "\n")
    for d in D:
        print(days[d])
        print(WR[f,d].x, " lf: ", LR[f,d].x)
