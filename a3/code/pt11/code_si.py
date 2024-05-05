
# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))

# DATA
P   = 4.2
s_0 = 100

def pasture(p):
    return round(p + 0.61*p*(1-p/300))

def required(t):
    if t < 18:
        y = 10.241 + 0.13*t
    else:
        y = 10.241 + 0.13*18 + 0.01121*(t-18)**2
    return round(y)


_revenue = {}
def revenue(t,s):

    if s - required(t) < 0:
        return (0, "Insufficient Supply")

    if (t,s) not in _revenue:
        if t == 51:
            
            # determine how much grass is available 
            available = s - required(t-1)
            extra = 0

            if available >= 40:
                extra = 40
            else:
                extra = available

            _revenue[t,s] = (P * extra, required(t) + extra)

        else:
            _revenue[t,s] = max((P * a + revenue(t+1, pasture(s) - required(t) - a)[0], required(t) + a) for a in range(0, 41))

    return _revenue[t,s]

def get_feed_amounts():
    s = s_0
    feed_amounts = [0] * 52

    for t in range(0,52):
        feed_amounts[t] = revenue(t, s)[1]
        s = pasture(s) - revenue(t,s)[1]

    print(feed_amounts)

print(f"Total revenue from milk sold: {round(revenue(0, s_0)[0], 3)}")
get_feed_amounts()
