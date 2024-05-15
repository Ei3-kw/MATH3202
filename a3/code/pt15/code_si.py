
# SETS
names = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(names))

cows = [
    [2.444, 0.0311, 0.00251],
    [2.454, 0.0376, 0.00255],
    [2.715, 0.0283, 0.00318],
    [2.628, 0.033, 0.00297]
]

# DATA
W = 52           # number of weeks
P = 4.2          # selling price for each unit of milk 
L = 5.0          # penalty cost per unit under 150
s_0 = 100        # starting units of grass
l_0 = (1,1,1,1)  # starting condition of cows 
minGrass = 150   # minimum units of grass before a penalty is applied 
maxUnitsCow = 10 # maximum units of feed that can be converted into milk per cow
PGood = 0.5      # probability of having good weather in the region
dryFeed = 3      # reduction in weekly feed per dry cow
dryable = 1      # maximum number of cows that can be dried off each week 

def penalty_grass(x):
    """ calculate units of grass below 150 """
    x -= minGrass
    return 0 if x >= 0 else abs(x)

def dry(l,b):
    """ update the list of dried cows """
    lst = list(l)
    lst[b] = 0
    return tuple(lst)

def pasture(p,weather):
    """ calculate units of grass available next week given the current weather """
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))
    return round(p + 0.61*p*(1-p/300))

def dryenergy(t, l):
    """ calculate units of grass required to feed the herd in week t based on dried cows """
    if t < 18:
        y = sum(l[c]*(cows[c][0] + cows[c][1]*t) for c in C)
    else:
        y = sum(l[c]*(cows[c][0] + cows[c][1]*18) + cows[c][2]*(t-18)**2 for c in C)
    return round(y)

_revenue = {}
def revenue(t,s,l):

    # if there is not enough grass to feed the herd, the solution is infeasible
    if s < dryenergy(t,l):
        return (-float('inf'), ("Infeasible", "Infeasible"))
    
    if (t,s,l) not in _revenue:

        # get the number of cows able to produce milk 
        d = sum(l)

        # determine units of feed that can be converted into milk based on the number of non-dry cows
        maxUnits = d * maxUnitsCow

        # determine the available grass units once the herd has been fed
        available = s - dryenergy(t,l)
        
        if t == 51 or d == 0:
            
            # determine how much grass is available at the end of the week for each weather scenario
            available_good = pasture(s,'Good') - dryenergy(t,l)
            available_poor = pasture(s,'Poor') - dryenergy(t,l)

            if d == 0:
                _revenue[t,s,l] = (PGood * (-L*penalty_grass(available_good)) 
                                   + (1-PGood) * (-L*penalty_grass(available_poor)), (0, l))
            else:
                _revenue[t,s,l] = max((PGood * (P*a - L*penalty_grass(available_good-a)) 
                                       + (1-PGood) * (P*a - L*penalty_grass(available_poor-a)), (a, l)) 
                                      for a in range(min(maxUnits+1, available+1)))
        else:
            # determine maximum profit if a cow is dried
            dryCows = max((PGood * (P*a + revenue(t+1, pasture(s,'Good')-dryenergy(t,l)-a, dry(l,b))[0]) 
                           + (1-PGood) * (P*a + revenue(t+1, pasture(s,'Poor')-dryenergy(t,l)-a, dry(l,b))[0]), (a,dry(l,b))) 
                          for a in range(min(maxUnits+1, available+1)) for b in C if l[b])

            # determine maximum profit if no cows are dried 
            notDryCows = max((PGood * (P*a + revenue(t+1, pasture(s,'Good')-dryenergy(t,l)-a, l)[0]) 
                              + (1-PGood) * (P*a + revenue(t+1, pasture(s,'Poor')-dryenergy(t,l)-a, l)[0]), (a,l)) 
                             for a in range(min(maxUnits+1, available+1)))

            _revenue[t,s,l] = max(dryCows, notDryCows)

    return _revenue[t,s,l]

print(f"Total revenue from milk sold: {round(revenue(0, s_0, l_0)[0], 2)}")

feed_dict = {}
l = l_0
for t in range(52):
    for p in range(0, 300):
        rev = revenue(t, p, l)
        if rev[1][0] == maxUnitsCow * sum(l):
            feed_dict[t] = tuple((p, l))
            if rev[1][1] != "Infeasible" and sum(rev[1][1]) < sum(l):
                l = rev[1][1]
            break 

print(feed_dict)
