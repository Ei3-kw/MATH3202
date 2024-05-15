
# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))
W = 52

# DATA
P   = 4.2       # selling price for each unit of milk 
L   = 5.0       # penalty cost per unit under 150
s_0 = 100       # starting units of grass
minGrass = 150  # minimum units of grass before a penalty is applied 
maxUnits = 40   # maximum units of feed that can be converted into milk across the herd

""" returns the units of grass below 150 """
def penalty_grass(x):
    x -= 150
    return 0 if x >= 0 else abs(x)

""" returns the units of grass available in the following week """
def pasture(p):
    return round(p + 0.61*p*(1-p/300))

""" returns the units of grass required to feed the herd each week """
def required(t):
    if t < 18:
        y = 10.241 + 0.13*t
    else:
        y = 10.241 + 0.13*18 + 0.01121*(t-18)**2
    return round(y)

_revenue = {}
def revenue(t,s):
    
    # there is not enough grass to feed the herd, the solution is infeasible 
    if s < required(t):
        return (-float('inf'), "Infeasible")

    if (t,s) not in _revenue:

        # determine the current available grass units
        available = s-required(t)
        
        # determine how much grass is available at the end of the week
        available_next = pasture(s)-required(t)

        if t == 51:          
            # calculate the maximum amount of profit given the penalty for each unit under 150 
            _revenue[t,s] = max((P*a - L*penalty_grass(available_next-a), a) 
                                for a in range(min(maxUnits+1, available+1)))

        else:
            _revenue[t,s] = max((P*a + revenue(t+1, available_next-a)[0], a) 
                                for a in range(min(maxUnits+1, available+1)))

    return _revenue[t,s]

""" returns the number of units of feed given to the herd each week """
def get_feed_amounts():
    feed_amounts = [0] * W
    s = s_0
    total = 0

    for t in range(W):
        feed_amounts[t] = revenue(t,s)[1]+required(t)
        total += P*revenue(t,s)[1]
        s = pasture(s)-revenue(t,s)[1]-required(t)
    
    print(f"Total revenue calculated using feed amounts: {round(total, 3)}")
    print(f"\nBREAKDOWN BY WEEK:")
    print(f"{'-'*65}\n| {'Week':<6} {'Feed':<6} | {'Week':<6} {'Feed':<6} | ", end='')
    print(f"{'Week':<6} {'Feed':<6} | {'Week':<6} {'Feed':<6} |\n|{'-'*63}|")
    for n in range(13):
        print(f"| {n:<6} {feed_amounts[n]:<6} | {13+n:<6} {feed_amounts[13+n]:<6} | ", end='')
        print(f"{26+n:<6} {feed_amounts[26+n]:<6} | {39+n:<6} {feed_amounts[39+n]:<6} |")
    print(f"{'-'*65}\n")

print(f"\nTOTALS:\n{'-'*65}")
print(f"Total revenue from milk sold: {round(revenue(0, s_0)[0], 3)}")
get_feed_amounts()
