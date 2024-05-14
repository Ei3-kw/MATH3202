
# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))
W = 52

# DATA
P   = 4.2   # selling price for each unit of milk 
L   = 5.0   # penalty cost per unit under 150
s_0 = 100   # starting units of grass
minGrass  = 150  # minimum units of grass before a penalty is applied 
PGood     = 0.5  # probability of having good weather in the region
dryFeed   = 3    # reduction in weekly feed per dry cow
milkUnits = 10   # maximum units of feed that can be converted into milk per cow
dryable   = 1    # number of cows that can be dried per week 

""" returns the units of grass below 150 """
def penalty_grass(x):
    x -= 150
    return 0 if x >= 0 else abs(x)

""" returns the units of grass available in the following week """
def pasture(p,weather):
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))

""" returns the units of grass required to feed the herd each week """
def required(t):
    if t < 18:
        y = 10.241 + 0.13*t
    else:
        y = 10.241 + 0.13*18 + 0.01121*(t-18)**2
    return round(y)

_revenue = {}
def revenue(t,s,d):

    if s < required(t):
        return (-float('inf'), "Infeasible")
    
    if (t,s,d) not in _revenue:

        # determine how many units of feed can be converted to milk this week
        maxUnits = (4-d)*milkUnits

        # determine the current available grass units
        available = s-required(t-1)+dryFeed*d
        
        # determine how much grass is available at the end of the week for each weather scenario
        available_good = pasture(s,'Good')-required(t)+dryFeed*d
        available_poor = pasture(s,'Poor')-required(t)+dryFeed*d

        if t == 51 or d == 4:
                                    
            # calculate the maximum amount of profit given the penalty for each unit under 150 
            if d == 4:
                _revenue[t,s,d] = (PGood     * (-L*penalty_grass(available_good)) + 
                                   (1-PGood) * (-L*penalty_grass(available_poor)), (0,d))
            else:
                _revenue[t,s,d] = max((PGood     * (P*a - L*penalty_grass(available_good-a)) +
                                       (1-PGood) * (P*a - L*penalty_grass(available_poor-a)), (a,d)) 
                                      for a in range(min(maxUnits+1, available+1)))
        else:
            # add the option of drying a cow
            _revenue[t,s,d] = max((PGood     * (P*a + revenue(t+1, available_good-a, d+b)[0]) +
                                   (1-PGood) * (P*a + revenue(t+1, available_poor-a, d+b)[0]),
                                   (a,d+b)) for a in range(min(maxUnits+1, available+1)) for b in range(dryable+1))

    return _revenue[t,s,d]

def get_feed_amounts():
    s = s_0
    feed_amounts = [0] * 52

    for t in range(0,52):
        feed_amounts[t] = revenue(t,s)[1]
        s = PGood * pasture(s, 'Good') + (1 - PGood) * pasture(s, 'Bad') - revenue(t,s)[1]

    print(feed_amounts)

print(f"Total revenue from milk sold: {round(revenue(0, s_0, 0)[0], 3)}")
#get_feed_amounts()
