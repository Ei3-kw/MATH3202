from gurobipy import *

# Sets
Farms = ['Cowbell', 'Creamy Acres', 'Milky Way', 'Happy Cows', 
         'Udder Delight', 'Fresh Pail', 'Cowabunga', 'Utopia', 
         'Moo Meadows', 'Bluebell', 'Harmony', 'Velvet Valley', 
         'Moonybrook', 'Cloven Hills', 'Midnight Moo', 'Willows Bend', 
         'Moosa Heads', 'Dreamy Dairies', 'Happy Hooves', 'Highlands']

Facilities = ['PF0', 'PF1', 'PF2']

Tankers = ['Tanker 1', 'Tanker 2', 'Tanker 3', 'Tanker 4', 'Tanker 5']

# Data
Milkruns = [
	[0, [0], 188, 470],
	[1, [0], 204, 510],
	[2, [0], 152, 380],
	[0, [1], 140, 350],
	[1, [1], 182, 455],
	[2, [1], 168, 420],
	[0, [2], 186, 465],
	[1, [2], 166, 415],
	[2, [2], 116, 290],
	[0, [3], 206, 515],
	[1, [3], 176, 440],
	[2, [3], 122, 305],
	[0, [4], 118, 295],
	[1, [4], 158, 395],
	[2, [4], 172, 430],
	[0, [5], 214, 535],
	[1, [5], 144, 360],
	[2, [5], 88, 220],
	[0, [6], 148, 370],
	[1, [6], 108, 270],
	[2, [6], 124, 310],
	[0, [7], 188, 470],
	[1, [7], 114, 285],
	[2, [7], 88, 220],
	[0, [8], 88, 220],
	[1, [8], 124, 310],
	[2, [8], 186, 465],
	[0, [9], 68, 170],
	[1, [9], 142, 355],
	[2, [9], 206, 515],
	[0, [10], 102, 255],
	[1, [10], 102, 255],
	[2, [10], 166, 415],
	[0, [11], 174, 435],
	[1, [11], 84, 210],
	[2, [11], 92, 230],
	[0, [12], 228, 570],
	[1, [12], 94, 235],
	[2, [12], 42, 105],
	[0, [13], 50, 125],
	[1, [13], 140, 350],
	[2, [13], 214, 535],
	[0, [14], 112, 280],
	[1, [14], 78, 195],
	[2, [14], 158, 395],
	[0, [15], 132, 330],
	[1, [15], 60, 150],
	[2, [15], 140, 350],
	[0, [16], 84, 210],
	[1, [16], 108, 270],
	[2, [16], 188, 470],
	[0, [17], 88, 220],
	[1, [17], 112, 280],
	[2, [17], 196, 490],
	[0, [18], 192, 480],
	[1, [18], 58, 145],
	[2, [18], 132, 330],
	[0, [19], 174, 435],
	[1, [19], 88, 220],
	[2, [19], 164, 410],
	[2, [0, 6], 188, 488],
	[2, [0, 7], 165, 419],
	[0, [8, 0], 194, 489],
	[0, [9, 0], 188, 461],
	[0, [10, 0], 208, 541],
	[2, [0, 11], 182, 470],
	[2, [0, 12], 156, 392],
	[0, [13, 0], 204, 505],
	[1, [14, 0], 234, 623],
	[1, [0, 15], 227, 605],
	[0, [16, 0], 233, 605],
	[0, [17, 0], 250, 652],
	[1, [0, 18], 260, 704],
	[1, [19, 0], 289, 785],
	[1, [14, 3], 209, 548],
	[1, [16, 3], 229, 593],
	[2, [6, 5], 139, 355],
	[1, [8, 5], 198, 501],
	[0, [9, 5], 215, 542],
	[2, [5, 12], 92, 232],
	[1, [14, 5], 180, 461],
	[1, [15, 5], 171, 443],
	[1, [16, 5], 200, 506],
	[1, [19, 5], 231, 611],
	[2, [6, 7], 126, 316],
	[1, [8, 6], 148, 351],
	[0, [9, 6], 150, 347],
	[1, [10, 6], 129, 304],
	[1, [6, 11], 113, 277],
	[2, [6, 12], 125, 313],
	[0, [13, 6], 150, 343],
	[1, [14, 6], 138, 335],
	[1, [15, 6], 130, 320],
	[1, [16, 6], 157, 377],
	[1, [17, 6], 174, 424],
	[1, [18, 6], 164, 426],
	[1, [19, 6], 192, 494],
	[1, [8, 7], 171, 420],
	[0, [9, 7], 190, 467],
	[1, [10, 7], 151, 370],
	[2, [11, 7], 106, 272],
	[2, [7, 12], 88, 220],
	[0, [13, 7], 189, 460],
	[1, [14, 7], 149, 368],
	[1, [15, 7], 140, 350],
	[1, [16, 7], 172, 422],
	[1, [17, 7], 186, 460],
	[1, [18, 7], 171, 447],
	[1, [19, 7], 200, 518],
	[0, [9, 8], 89, 164],
	[0, [8, 10], 106, 225],
	[1, [8, 11], 151, 360],
	[1, [8, 12], 182, 453],
	[0, [13, 8], 98, 187],
	[0, [8, 14], 143, 336],
	[1, [8, 15], 139, 324],
	[0, [16, 8], 130, 296],
	[0, [17, 8], 147, 343],
	[1, [8, 18], 177, 438],
	[1, [8, 19], 202, 513],
	[0, [9, 10], 106, 215],
	[1, [9, 11], 170, 407],
	[1, [9, 12], 201, 500],
	[0, [13, 9], 87, 154],
	[0, [9, 14], 135, 302],
	[0, [9, 15], 150, 347],
	[0, [9, 16], 120, 257],
	[0, [9, 17], 138, 311],
	[1, [9, 18], 188, 461],
	[1, [9, 19], 213, 536],
	[1, [10, 11], 130, 307],
	[1, [10, 12], 162, 403],
	[0, [13, 10], 104, 205],
	[1, [10, 14], 123, 286],
	[1, [10, 15], 118, 271],
	[0, [16, 10], 128, 290],
	[0, [17, 10], 146, 340],
	[1, [10, 18], 155, 382],
	[1, [10, 19], 181, 460],
	[2, [11, 12], 94, 236],
	[0, [13, 11], 175, 418],
	[1, [14, 11], 118, 275],
	[1, [15, 11], 109, 257],
	[1, [16, 11], 148, 350],
	[1, [17, 11], 155, 367],
	[1, [18, 11], 141, 357],
	[1, [19, 11], 170, 428],
	[1, [13, 12], 206, 511],
	[1, [14, 12], 149, 368],
	[1, [15, 12], 132, 326],
	[1, [16, 12], 179, 443],
	[1, [17, 12], 186, 460],
	[1, [18, 12], 151, 387],
	[1, [19, 12], 182, 464],
	[0, [13, 14], 113, 232],
	[0, [13, 15], 132, 289],
	[0, [13, 16], 86, 151],
	[0, [13, 17], 102, 199],
	[1, [13, 18], 171, 406],
	[0, [13, 19], 185, 448],
	[1, [14, 15], 79, 158],
	[1, [16, 14], 109, 233],
	[1, [17, 14], 115, 247],
	[1, [14, 18], 112, 257],
	[1, [19, 14], 136, 326],
	[1, [16, 15], 109, 233],
	[1, [17, 15], 114, 244],
	[1, [15, 18], 98, 224],
	[1, [19, 15], 124, 290],
	[0, [17, 16], 102, 208],
	[1, [16, 18], 138, 320],
	[1, [16, 19], 153, 365],
	[1, [17, 18], 138, 316],
	[1, [17, 19], 144, 334],
	[1, [19, 18], 89, 185],
	[1, [14, 8, 6], 168, 425],
	[0, [16, 6, 8], 167, 407],
	[1, [14, 6, 12], 173, 440],
	[1, [16, 6, 12], 192, 482],
	[1, [14, 16, 6], 158, 395],
	[1, [9, 8, 12], 202, 503],
	[0, [9, 8, 14], 144, 329],
	[1, [8, 9, 15], 153, 366],
	[0, [9, 8, 16], 131, 290],
	[1, [14, 8, 12], 202, 527],
	[1, [15, 8, 12], 197, 521],
	[1, [16, 8, 12], 218, 560],
	[1, [8, 14, 15], 145, 342],
	[0, [16, 14, 8], 145, 341],
	[0, [16, 15, 8], 158, 380],
	[1, [14, 9, 12], 214, 563],
	[1, [15, 9, 12], 210, 560],
	[1, [16, 9, 12], 228, 590],
	[0, [9, 15, 14], 150, 347],
	[0, [9, 14, 16], 137, 308],
	[0, [9, 15, 16], 151, 350],
	[1, [15, 14, 12], 150, 380],
	[1, [16, 14, 12], 180, 446],
	[1, [15, 16, 12], 180, 470],
	[1, [14, 16, 15], 110, 251],
	[1, [19, 16, 14], 154, 380],	
]

Supply = [5200, 9900, 8800, 6900, 
          9500, 5900, 3700, 4800, 
          3200, 3400, 4400, 4500, 
          3200, 4800, 3100, 3400, 
          3000, 4500, 4500, 3900]

Distance = [
	[94,102,76],    # Cowbell
	[70,91,84],     # Creamy Acres
	[93,83,58],     # Milky Way 
	[103,88,61],    # Happy Cows 
	[59,79,86],     # Udder Delight
	[107,72,44],    # Fresh Pail
	[74,54,62],     # Cowabunga
	[94,57,44],     # Utopia
	[44,62,93],     # Moo Meadows 
	[34,71,103],    # Bluebell
	[51,51,83],     # Harmony
	[87,42,46],     # Velvet Valley
	[114,47,21],    # Moonybrook
	[25,70,107],    # Cloven Hills
	[56,39,79],     # Midnight Moo
	[66,30,70],     # Willows Bend
	[42,54,94],     # Moosa Heads
	[44,56,98],     # Dreamy Dairies
	[96,29,66],     # Happy Hooves
	[87,44,82]      # Highlands
]

F = range(len(Farms))
P = range(len(Facilities))
T = range(len(Tankers))
R = range(len(Milkruns))

PMin = [20000,24000,32000]  # maximum daily capacity (litres)
PMax = [45000,35000,36000]  # minimum daily processing (litres)

Maintenance = [500, 470, 440, 410, 380]

TEmpty  = 2     # travel cost with empty tanker ($/km)
TFull   = 3     # travel cost with milk on board ($/km)
TRound  = 5     # travel cost for a round trip ($/km)

HMax = 10       # maximum number of hours a tanker can be used for 
DMax = 600      # maximum number of minutes a tanker can be used for 

# Model
m = Model('Comm 6')

# Variables 

W = {(p, t): m.addVar(vtype=GRB.BINARY, name=f"whether a tanker in the fleet is operational") for p in P for t in T}

""" boolean variables to tell us which of the processing plants the farms are assigned to """
X = {(f, t, r): m.addVar(vtype=GRB.BINARY, name=f"farm and tanker assignment for PF0") for f in F for t in T for r in R}
Y = {(f, t, r): m.addVar(vtype=GRB.BINARY, name=f"farm and tanker assignment for PF1") for f in F for t in T for r in R}
Z = {(f, t, r): m.addVar(vtype=GRB.BINARY, name=f"farm and tanker assignment for PF2") for f in F for t in T for r in R}


# Objective
""" minimise the cost of travel to all of the farms """
m.setObjective(quicksum((X[f,t,r] * Milkruns[r][3] + 
                         Y[f,t,r] * Milkruns[r][3] + 
                         Z[f,t,r] * Milkruns[r][3]) for f in F for t in T for r in R) +     # cost for travel
               quicksum(W[p,t] * Maintenance[t] for p in P for t in T), GRB.MINIMIZE)       # cost for maintenance

# Constraints

# maximum daily capacity is not exceeded for each processing facility
m.addConstr(quicksum(X[f,t,r] * Supply[f] for f in F for t in T for r in R) <= PMax[0])
m.addConstr(quicksum(Y[f,t,r] * Supply[f] for f in F for t in T for r in R) <= PMax[1])
m.addConstr(quicksum(Z[f,t,r] * Supply[f] for f in F for t in T for r in R) <= PMax[2])

# minimum processing requirement is met for each processing facility
m.addConstr(quicksum(X[f,t,r] * Supply[f] for f in F for t in T for r in R) >= PMin[0])
m.addConstr(quicksum(Y[f,t,r] * Supply[f] for f in F for t in T for r in R) >= PMin[1])
m.addConstr(quicksum(Z[f,t,r] * Supply[f] for f in F for t in T for r in R) >= PMin[2])

for f in F:
    # each farm is assigned to one processing plant, one tanker and one milkrun
    m.addConstr(quicksum(X[f,t,r] + Y[f,t,r] + Z[f,t,r] for t in T for r in R) == 1)

for r in R:
    m.addConstr(quicksum(X[f,t,r] + Y[f,t,r] + Z[f,t,r] for f in F for t in T) <= 1)

#for f in F:
#    for t in T:
#        for r in R:
#            m.addConstr((X[f,t,r] == 1) >> (X[f,t,r] == 1 for i in F if i in Milkruns[r][2])) 
#            m.addConstr((Y[f,t,r] == 1) >> (Y[f,t,r] == 1 for i in F if i in Milkruns[r][2])) 
#            m.addConstr((Z[f,t,r] == 1) >> (Z[f,t,r] == 1 for i in F if i in Milkruns[r][2])) 

for f in F:
    for t in T:
        for r in R:
        # If it is the first processing facility
            if Milkruns[r][0] == 0:
                m.addConstr(Y[f,t,r] == 0)
                m.addConstr(Z[f,t,r] == 0)
            elif Milkruns[r][0] == 1:
                m.addConstr(X[f,t,r] == 0)
                m.addConstr(Z[f,t,r] == 0)
            elif Milkruns[r][0] == 1:
                m.addConstr(X[f,t,r] == 0)
                m.addConstr(Y[f,t,r] == 0)

# tankers are operational for at most 10 hours
for t in T:
    m.addConstr(quicksum(X[f,t,r] * Milkruns[r][2] for f in F for r in R) <= DMax)
    m.addConstr(quicksum(Y[f,t,r] * Milkruns[r][2] for f in F for r in R) <= DMax)
    m.addConstr(quicksum(Z[f,t,r] * Milkruns[r][2] for f in F for r in R) <= DMax)

for t in T:
    for f in F:
        for r in R:
            m.addConstr((X[f,t,r] == 1) >> (W[0,t] == 1))
            m.addConstr((Y[f,t,r] == 1) >> (W[1,t] == 1))
            m.addConstr((Z[f,t,r] == 1) >> (W[2,t] == 1))

for p in P:
    for t in T:
        if t > 0:
            m.addConstr((W[p,t] == 1) >> (W[p,t-1] == 1))

m.optimize()

if m.status == GRB.INFEASIBLE:
    print("The model is infeasible.")  
    exit()

print(f"\n{'Totals'}\n{'-'*65}")
print(f"{'Total cost of travel:': <20} ${int(m.objVal)}\n")

print(f"{'-'*65}\n{'Facility': <13} {'Collection ($)': <18} {'Maintenance ($)': <18} {'Total ($)': <15}\n{'-'*65}")

print(f"{'PF0': <13} {int(quicksum(X[f,t,r].x * Milkruns[r][3] for f in F for t in T for r in R).getValue()): <18}", end='')
print(f" {int(quicksum(W[0,t] * Maintenance[t] for t in T).getValue()): <18}", end='')
print(f" {int(quicksum(X[f,t,r].x * Milkruns[r][3] for f in F for t in T for r in R).getValue() + quicksum(W[0,t] * Maintenance[t] for t in T).getValue())}")

print(f"{'PF1': <13} {int(quicksum(X[f,t,r].x * Milkruns[r][3] for f in F for t in T for r in R).getValue()): <18}", end='')
print(f" {int(quicksum(W[1,t] * Maintenance[t] for t in T).getValue()): <18}", end='')
print(f" {int(quicksum(X[f,t,r].x * Milkruns[r][3] for f in F for t in T for r in R).getValue() + quicksum(W[1,t] * Maintenance[t] for t in T).getValue())}")

print(f"{'PF3': <13} {int(quicksum(X[f,t,r].x * Milkruns[r][3] for f in F for t in T for r in R).getValue()): <18}", end='')
print(f" {int(quicksum(W[2,t] * Maintenance[t] for t in T).getValue()): <18}", end='')
print(f" {int(quicksum(X[f,t,r].x * Milkruns[r][3] for f in F for t in T for r in R).getValue() + quicksum(W[2,t] * Maintenance[t] for t in T).getValue())}")

print(f"{'-'*65}\n")

"""
print(f"PROCESSING FACILITY 0")
print(f"{'-'*80}\n{'Farms': <18} {'Dist. (km)': <15} {'Cost ($)': <15} {'Supply (L)': <15} {'Tanker': <15}\n{'-'*80}")
for f in F:
    for t in T:
        if X[f,t].x:
            print(f"{Farms[f]: <18} {Distance[f][0]: <15} {Distance[f][0]*TRound: <15} {Supply[f]: <15} {Tankers[t]: <15}")
print(f"{'-'*80}")

print(f"{' '*18} {int(quicksum(X[f,t].x * Distance[f][0] for f in F for t in T).getValue()): <15}", end='')
print(f" {int(quicksum(X[f,t].x * Distance[f][0] * TRound for f in F for t in T).getValue()): <15}", end='')
print(f" {int(quicksum(X[f,t].x * Supply[f] for f in F for t in T).getValue())} / {PMax[0]}\n")


print(f"PROCESSING FACILITY 1")
print(f"{'-'*80}\n{'Farms': <18} {'Dist. (km)': <15} {'Cost ($)': <15} {'Supply (L)': <15} {'Tanker': <15}\n{'-'*80}")
for f in F:
    for t in T:
        if X[f,t].x:
            print(f"{Farms[f]: <18} {Distance[f][1]: <15} {Distance[f][1]*TRound: <15} {Supply[f]: <15} {Tankers[t]: <15}")
print(f"{'-'*80}")

print(f"{' '*18} {int(quicksum(Y[f,t].x * Distance[f][1] for f in F for t in T).getValue()): <15}", end='')
print(f" {int(quicksum(Y[f,t].x * Distance[f][1] * TRound for f in F for t in T).getValue()): <15}", end='')
print(f" {int(quicksum(Y[f,t].x * Supply[f] for f in F for t in T).getValue())} / {PMax[1]}\n")


print(f"PROCESSING FACILITY 2")
print(f"{'-'*80}\n{'Farms': <18} {'Dist. (km)': <15} {'Cost ($)': <15} {'Supply (L)': <15} {'Tanker': <15}\n{'-'*80}")
for f in F:
    for t in T:
        if X[f,t].x:
            print(f"{Farms[f]: <18} {Distance[f][0]: <15} {Distance[f][0]*TRound: <15} {Supply[f]: <15} {Tankers[t]: <15}")
print(f"{'-'*80}")

print(f"{' '*18} {int(quicksum(Z[f,t].x * Distance[f][2] for f in F for t in T).getValue()): <15}", end='')
print(f" {int(quicksum(Z[f,t].x * Distance[f][2] * TRound for f in F for t in T).getValue()): <15}", end='')
print(f" {int(quicksum(Z[f,t].x * Supply[f] for f in F for t in T).getValue())} / {PMax[2]}\n")
"""
