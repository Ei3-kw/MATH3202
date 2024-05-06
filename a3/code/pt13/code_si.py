
# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))

# DATA
P   = 4.2
L   = 5.0
s_0 = 100
minGrass = 150
PGood    = 0.5

def penalty_grass(x):
    x -= 150

    if x >= 0:
        return 0
    else:
        return abs(x)

def pasture(p,weather):
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))

def required(t):
    if t < 18:
        y = 10.241 + 0.13*t
    else:
        y = 10.241 + 0.13*18 + 0.01121*(t-18)**2
    return round(y)

_revenue = {}
def revenue(t,s):

    if s < required(t):
        return (-5000, 0, 0)
    
    if (t,s) not in _revenue:
        
        if t == 51:
            # determine how much grass is available 
            available_good = pasture(s, 'Good') - required(t)
            available_poor = pasture(s, 'Poor') - required(t)
            
            # calculate the maximum amount of profit given the penalty for each unit under 150 
            _revenue[t,s] = max((PGood * (P * a - L * penalty_grass(available_good - a)) + 
                                 (1 - PGood) * (P * a - L * penalty_grass(available_poor - a)), 
                                 required(t) + a) for a in range(0, 41))
        
        else:
            _revenue[t,s] = max((PGood * (P * a + revenue(t + 1, pasture(s, 'Good') - required(t) - a)[0]) +
                                 (1 - PGood) * (P * a + revenue(t + 1, pasture(s, 'Poor') - required(t) - a)[0]),
                                 required(t) + a) for a in range(0, 41))

    return _revenue[t,s]

def get_feed_amounts():
    s = s_0
    feed_amounts = [0] * 52

    for t in range(0,52):
        feed_amounts[t] = revenue(t,s)[1]
        s = PGood * pasture(s, 'Good') + (1 - PGood) * pasture(s, 'Bad') - revenue(t,s)[1]

    print(feed_amounts)

print(f"Total revenue from milk sold: {round(revenue(0, s_0)[0], 3)}")
get_feed_amounts()
