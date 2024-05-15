
# SETS
names = ['Lily', 'Betty', 'Clover', 'Rosie']

cows = [
    [2.444, 0.0311, 0.00251],
    [2.454, 0.0376, 0.00255],
    [2.715, 0.0283, 0.00318],
    [2.628, 0.033, 0.00297]
]

# Ella
# cows = [
#     [2.411, 0.0378, 0.0033],
#     [2.454, 0.0376, 0.00255],
#     [2.489, 0.0389, 0.00312],
#     [2.734, 0.0302, 0.00254]
# ]

C = range(len(cows))
W = 52

# DATA
P   = 4.2   # selling price for each unit of milk 
L   = 5.0   # penalty cost per unit under 150
s_0 = 100   # starting units of grass
l_0 = (1,1,1,1)  # starting condition of cows
minGrass  = 150  # minimum units of grass before a penalty is applied 
PGood     = 0.5  # probability of having good weather in the region
dryFeed   = 3    # reduction in weekly feed per dry cow
milkUnits = 10   # maximum units of feed that can be converted into milk per cow
dryable   = 1    # number of cows that can be dried per week 

""" returns the units of grass below 150 """
def penalty_grass(x):
    x -= minGrass
    return 0 if x >= 0 else abs(x)

""" returns the units of grass required to feed the herd each week """
def dryenergy(t, l=(1,1,1,1)):
    if t < 18:
        y = sum(l[c]*(cows[c][0] + cows[c][1]*t) for c in C)
    else:
        y = sum(l[c]*(cows[c][0] + cows[c][1]*18) + cows[c][2]*(t-18)**2 for c in C)
    return round(y)

""" returns the units of grass available in the following week """
def pasture(p,weather):
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))

# """ returns the units of grass required to feed the herd each week """
# def required(t):
#     if t < 18:
#         y = 10.241 + 0.13*t
#     else:
#         y = 10.241 + 0.13*18 + 0.01121*(t-18)**2
#     return round(y)

_revenue = {}
def revenue(t,s,l):

    if s < dryenergy(t, l):
        return (-float('inf'), "Infeasible")
    
    if (t,s,l) not in _revenue:

        # determine how many units of feed can be converted to milk this week
        maxUnits = sum(l)*milkUnits

        # determine the current available grass units
        available = s-dryenergy(t, l)
        
        # determine how much grass is available at the end of the week for each weather scenario
        available_good = pasture(s,'Good')-dryenergy(t, l)
        available_poor = pasture(s,'Poor')-dryenergy(t, l)

        if t == 51 or sum(l) == 0:
                                    
            # calculate the maximum amount of profit given the penalty for each unit under 150 
            if sum(l) == 0:
                _revenue[t,s,l] = (PGood * (-L*penalty_grass(available_good))
                    + (1-PGood) * (-L*penalty_grass(available_poor)), (0, l))
            else:
                _revenue[t,s,l] = max((PGood * (P*a - L*penalty_grass(available_good-a))
                    + (1-PGood) * (P*a - L*penalty_grass(available_poor-a)), (a, l))
                for a in range(min(maxUnits+1, available+1)))
        else:
            _revenue[t,s,l] = max((PGood * (P*a + revenue(t+1, available_good-a, l)[0])
                + (1-PGood) * (P*a + revenue(t+1, available_poor-a, l)[0]),
                (a, l)) for a in range(min(maxUnits+1, available+1)))

            # add the option of drying a cow that's not yet dried
            dried = {}
            for i in C:
                if l[i]:
                new_l = list(l)
                new_l[i] = 0
                new_l = tuple(new_l)
                dried[l] = max((PGood * (P*a + revenue(t+1, available_good-a, new_l)[0])
                    + (1-PGood) * (P*a + revenue(t+1, available_poor-a, new_l)[0]),
                    (a, new_l)) for a in range(min(maxUnits+1, available+1)))

            _revenue[t,s,l] = max(max(dried.values()), _revenue[t,s,l])

    return _revenue[t,s,l]

def get_feed_amounts():
    s = s_0
    feed_amounts = [0] * 52

    for t in range(0,52):
        feed_amounts[t] = revenue(t,s)[1]
        s = PGood * pasture(s, 'Good') + (1 - PGood) * pasture(s, 'Bad') - revenue(t,s)[1]

    print(feed_amounts)

print(f"Total revenue from milk sold: {round(revenue(0, s_0, l_0)[0], 3)}")
#get_feed_amounts()
