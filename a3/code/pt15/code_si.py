
# SETS
names = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(names))

cows = [
    [2.444, 0.0311, 0.00251],
    [2.454, 0.0376, 0.00255],
    [2.715, 0.0283, 0.00318],
    [2.628, 0.033, 0.00297]
]

W = 52

# DATA
P   = 4.2        # selling price for each unit of milk 
L   = 5.0        # penalty cost per unit under 150
s_0 = 100        # starting units of grass
l_0 = (1,1,1,1)  # starting condition of cows 
minGrass  = 150  # minimum units of grass before a penalty is applied 
PGood     = 0.5  # probability of having good weather in the region
dryFeed   = 3    # reduction in weekly feed per dry cow
milkUnits = 10   # maximum units of feed that can be converted into milk per cow
dryable   = 1    # number of cows that can be dried per week 

""" returns the units of grass below 150 """
def penalty_grass(x):
    x -= 150
    return 0 if x >= 0 else abs(x)

""" updates the list of dried cows """
def dry(l,b):
    lst = list(l)
    lst[b] = 0
    return tuple(lst)

""" returns the units of grass available in the following week """
def pasture(p,weather):
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))

""" returns the units of grass required to feed the herd each week """
def dryenergy(t, l):
    if t < 18:
        y = sum(l[c]*(cows[c][0] + cows[c][1]*t) for c in C)
    else:
        y = sum(l[c]*(cows[c][0] + cows[c][1]*18) + cows[c][2]*(t-18)**2 for c in C)
    return round(y)

_revenue = {}
def revenue(t,s,l):

    if s < dryenergy(t,l):
        return (-float('inf'), "Infeasible")
    
    if (t,s,l) not in _revenue:

        # get the number of cows able to produce milk 
        temp = [x for x in l]
        d = sum(temp)

        # determine how many units of feed can be converted to milk this week
        maxUnits = d*milkUnits

        # determine the current available grass units
        available = s-dryenergy(t,l)
        
        if t == 51 or d == 0:
            
            # determine how much grass is available at the end of the week for each weather scenario
            available_good = pasture(s,'Good')-dryenergy(t,l)
            available_poor = pasture(s,'Poor')-dryenergy(t,l)

            if d == 0:
                _revenue[t,s,l] = (PGood     * (-L*penalty_grass(available_good)) + 
                                   (1-PGood) * (-L*penalty_grass(available_poor)), (0,l))
            else:
                _revenue[t,s,l] = max((PGood     * (P*a - L*penalty_grass(available_good-a)) +
                                       (1-PGood) * (P*a - L*penalty_grass(available_poor-a)), (a,l)) 
                                      for a in range(min(maxUnits+1, available+1)))
        else:
            # add the option of drying a cow
            dryCows = max((PGood     * (P*a + revenue(t+1, pasture(s,'Good')-dryenergy(t,dry(l,b))-a, dry(l,b))[0]) +
                           (1-PGood) * (P*a + revenue(t+1, pasture(s,'Poor')-dryenergy(t,dry(l,b))-a, dry(l,b))[0]),
                           (a,dry(l,b))) for a in range(min(maxUnits+1, available+1)) for b in C if l[b])

            notDryCows = max((PGood     * (P*a + revenue(t+1, pasture(s,'Good')-dryenergy(t,l)-a, l)[0]) +
                              (1-PGood) * (P*a + revenue(t+1, pasture(s,'Poor')-dryenergy(t,l)-a, l)[0]),
                              (a,l)) for a in range(min(maxUnits+1, available+1)))

            _revenue[t,s,l] = max(dryCows, notDryCows)


    return _revenue[t,s,l]

print(f"Total revenue from milk sold: {round(revenue(0, s_0, l_0)[0], 3)}")
