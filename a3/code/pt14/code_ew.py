
# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))

# DATA
P   = 4.2
L   = 5.0
s_0 = 100
d_0 = 0
minGrass = 150
PGood    = 0.5


def penalty_grass(x):
    x -= minGrass

    if x >= 0:
        return 0
    else:
        return abs(x)

def pasture(p, weather):
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

# def required(t, n_dry):
#     if t < 18:
#         y = 10.088 + 0.1445 * t - 3 * n_dry
#     else:
#         y = 10.088 + 0.1445 * 18 + 0.01151 * (t - 18) ** 2 - 3 * n_dry
#     return round(y)

_revenue = {}
def revenue(t, s, n_dry):

    if s < required(t, n_dry):
        return (-5000, 0, 0, 0) # penalty for insufficient feed
    
    if (t, s, n_dry) not in _revenue:
        
        if t == 51:
            # determine how much grass is available 
            available_good = pasture(s, 'Good') - required(t, n_dry)
            available_poor = pasture(s, 'Poor') - required(t, n_dry)
            
            # calculate the maximum amount of profit given the penalty for each unit under 150 
            _revenue[t, s, n_dry] = max(
                (PGood * (P * a - L * penalty_grass(available_good - a))
                    + (1 - PGood) * (P * a - L * penalty_grass(available_poor - a)),
                    required(t, n_dry) + a, 0)
                for a in range(0, 41-10*n_dry))
        
        else:
            try:
                _revenue[t, s, n_dry] = max(
                    (PGood * (P * a + revenue(t + 1, pasture(s, 'Good') - required(t, n_dry) - a, n_dry)[0])
                        + (1 - PGood) * (P * a + revenue(t + 1, pasture(s, 'Poor') - required(t, n_dry) - a, n_dry)[0]),
                        required(t, n_dry) + a,
                        PGood * (P * a + revenue(t + 1, pasture(s, 'Good') - required(t, n_dry) - a, n_dry+1)[0])
                        + (1 - PGood) * (P * a + revenue(t + 1, pasture(s, 'Poor') - required(t, n_dry) - a, n_dry+1)[0]))
                    for a in range(0, 41-10*n_dry))
            except ValueError:
                _revenue[t, s, n_dry] = 0


    return _revenue[t,s, n_dry]

def get_feed_amounts():
    s = s_0
    feed_amounts = [0] * 52
    dry_cows = [0] * 52
    n_dry = 0

    for t in range(0, 52):
        feed_amounts[t] = revenue(t,s)[1]
        s = PGood * pasture(s, 'Good') + (1 - PGood) * pasture(s, 'Bad') - revenue(t,s)[1]

    print(feed_amounts)

# print(f"Total revenue from milk sold: {round(revenue(0, s_0, d_0)[0], 3)}")
# get_feed_amounts()

for i in range(51):
    print(required(i), required(i+1))
