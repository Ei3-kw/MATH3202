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

#supply = [5200, 9900, 8800, 6900, 9500, 5900]
#fat = [3.6, 3.5, 3.8, 3.9, 3.6, 3.4]
supply = [8700, 5400, 8800, 5400, 8900, 9300]
fat = [3.3, 3.8, 3.6, 3.4, 3.5, 3.8]

# Milk demand Mon-Sun
#demand = [[13743, 27313, 68179, 13716, 27426, 27338, 81674],
#          [3337, 7007, 17097, 3391, 6935, 6937, 20428]]
demand = [[13778, 27488, 68427, 13740, 27428, 27519, 82193],
          [3485, 6896, 17060, 3543, 6756, 6794, 20733]]

StoreCost = 0.05

### Create new model
model = Model("Teal Cow Dairy")


### Variables

# milk m produced on day d
X = {(m,d): model.addVar() for m in M for d in D }

# milk m sold from product of day d 
Y = {(m,d): model.addVar() for m in M for d in D }

# milk m stored from product of day d
Z = {(m,d): model.addVar() for m in M for d in D }

# total milk m stored cumulatively
S = {(m,d): model.addVar() for m in M for d in D }

# total milk m sold on day d
T = {(m,d): model.addVar() for m in M for d in D }


### Objective
model.setObjective(quicksum(wholesale_price[m] * T[m, d] for m in M for d in D) -   # total profit
                   quicksum(StoreCost * S[m, d] for m in M for d in D),             # minus storage
                   GRB.MAXIMIZE)

### Constraints

# sold and stored of day d must equal the produced milk of day d
for d in D:
    for m in M:
        model.addConstr(X[m,d] == Y[m,d] + S[m,d])

# produced milk must be less than or equal to supply
for d in D:
    model.addConstr(quicksum(X[m,d] for m in M) <= quicksum(supply[f] for f in F))

# demand for each day must not be exceeded
for m in M:
    for d in D:
        model.addConstr(T[m,d] <= demand[m][d])

for d in D:
    for m in M:
        if d > 0:
            """ milk sold today equals milk from today's product plus milk stored from yesterday """
            model.addConstr(T[m,d] == Y[m,d] + (S[m,d-1]))

        else:    
            """ milk sold cumulatively equals milk sold today """
            model.addConstr(T[m,d] == Y[m,d])
            

# Every day, the fat content of the product must be <= the fat content of the supply
for d in D:
    model.addConstr(quicksum(X[m,d] * fat_product[m] for m in M) <=     # fat content of produced milk
                    quicksum(supply[f] * fat[f] for f in F))            # fat content of supply milk

model.optimize()

print("\n")
print("-----------------------------------------------------------")
print("INCOME:", round(model.objVal, 2), "\n")
print("Total sold whole milk:", sum(round(T[m, d].x, 2) for m in M for d in D if m == 0))
print("Total sold low fat milk:", sum(round(T[m, d].x, 2) for m in M for d in D if m == 1))
print("\n")

print("--- Breakdown by day --------------------------------------")
for d in D:
    print("----- ", days[d], " -----")
    print("   Sold: ", milk[0], ": ", T[0,d].x, " / ", demand[0][d])
    print("         ", milk[1], ": ", T[1,d].x, " / ", demand[1][d])
    print(" Stored: ", milk[0], ": ", S[0,d].x)
    print("         ", milk[1], ": ", S[1,d].x)

    print("\n")

print("--- Further Breakdown --------------------------------------")
for d in D:
    print("----- ", days[d], " -----\n")
    
    print(" Today produced:    ", milk[0], ": ", round(X[0,d].x, 2))
    print("                    ", milk[1], ": ", round(X[1,d].x, 2))
    print(" Today sold:        ", milk[0], ": ", round(Y[0,d].x, 2))
    print("                    ", milk[1], ": ", round(Y[1,d].x, 2))
    print(" Today stored:      ", milk[0], ": ", round(S[0,d].x, 2))
    print("                    ", milk[1], ": ", round(S[1,d].x, 2))

    if d == 0:
        print(" Sold from storage: ", milk[0], ": 0")
        print("                    ", milk[1], ": 0")

    else:
        print(" Sold from storage: ", milk[0], ": ", (T[0,d].x - Y[0,d].x))
        print("                    ", milk[1], ": ", (T[1,d].x - Y[1,d].x))

    print("\n")




