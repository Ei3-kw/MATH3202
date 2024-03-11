from gurobipy import * 

# Sets
milk = ["Full Cream", 
        "Low Fat", 
        "Organic Full Cream", 
        "Organic Low Fat"]
farms = ["Barnwood", 
         "Thistlebrook", 
         "Rustic Ranch", 
         "Haven",
         "Silo Springs"]

M = range(len(milk))
F = range(len(farms))

# Data
income = [1.10, 1.12, 1.30, 1.32]
fat_product = [4, 1, 4, 1]

# supply = [9600, 5300, 9300, 9200, 7100]
# fat = [3.4, 3.6, 3.8, 3.6, 3.7]
supply = [5400, 7200, 7600, 5700, 7000]
fat = [3.8, 3.6, 3.3, 3.3, 3.7]

organic_product = ["Organic" in milk[m] for m in M]
organic_farm = [False, False, False, True, True]
low_fat = ["Low" in milk[m] for m in M]

MaxPercentLow = 0.25
MaxPercentOrganic = 0.15

# Create new model
model = Model("Teal Cow Dairy")

# Variables
""" X[m, f] is the volumne of milk m produced from supply from farm f """
X = {(m,f): model.addVar() for m in M for f in F }

# Objective
""" Maximise the sum of the income from each milk """
model.setObjective(quicksum(income[m] * X[m, f] for m in M for f in F), GRB.MAXIMIZE)

# Constraints
""" for every non-organic farm, the sum of organic milk produced there must be zero """ 
for f in F:
    if not organic_farm[f]:
        model.addConstr(quicksum(X[m, f] for m in M if organic_product[m]) == 0)

""" supply for each farm cannot be exceeded """
for f in F:
    model.addConstr(quicksum(X[m, f] for m in M) <= supply[f])

""" the sum of all produced milk must equal the sum of supply """
model.addConstr(quicksum(X[m, f] for m in M for f in F) == quicksum(supply[f] for f in F))

""" the percentage of fat in product is less than or equal to the percentage fat in supply """
# organic
model.addConstr(quicksum(X[m, f] * (fat_product[m] / 100) for m in M for f in F if organic_product[m]) 
                <= quicksum(supply[f]*(fat[f] / 100) for f in F if organic_farm[f]))
# non-organic
model.addConstr(quicksum(X[m, f] * (fat_product[m] / 100) for m in M for f in F if not organic_product[m])
                <= quicksum(supply[f]*(fat[f] / 100) for f in F))

""" low fat can be at most 25% of total milk production (for organic and non-organic) """
# organic
model.addConstr(quicksum(X[m, f] for f in F for m in M if (organic_product[m] and low_fat[m])) 
                <= MaxPercentLow * quicksum(X[m, f] for f in F for m in M if organic_product[m]))
# non-organic
model.addConstr(quicksum(X[m, f] for f in F for m in M if (not organic_product[m] and low_fat[m])) 
                <= MaxPercentLow * quicksum(X[m, f] for f in F for m in M if not organic_product[m]))

""" organic products can make up at most 15% of all milk sold """
model.addConstr(quicksum(X[m, f] for f in F for m in M if organic_product[m]) 
                <= MaxPercentOrganic * quicksum(X[m, f] for f in F for m in M))

model.optimize()

print("\n")
print("-----------------------------------------------------------")
print("INCOME:", round(model.objVal, 2), "\n")
print("Total full cream milk:", sum(round(X[m, f].x, 2) for m in M for f in F if m == 0))
print("Total low fat milk:", sum(round(X[m, f].x, 2) for m in M for f in F if m == 1))
print("Total organic full cream milk:", sum(round(X[m, f].x, 2) for m in M for f in F if m == 2))
print("Total organic low fat milk:", sum(round(X[m, f].x, 2) for m in M for f in F if m == 3))
print("\n")

print("--- Breakdown by milk variety -----------------------------")
for f in F:
    print(farms[f])
    for m in M:
        print("- ", milk[m], ":", round(X[m, f].x, 2))
    print("\n")

print("Total organic milk:", 
      sum(round(X[m, f].x, 2) for m in M for f in F if organic_product[m]))
print("Total non-organic milk:", 
      sum(round(X[m, f].x, 2) for m in M for f in F if not organic_product[m]))
print("Total organic low fat", 
      sum(round(X[m, f].x, 2) for f in F for m in M if (organic_product[m] and low_fat[m])))
print("Total non-organic low fat", 
      sum(round(X[m, f].x, 2) for f in F for m in M if (not organic_product[m] and low_fat[m])))
