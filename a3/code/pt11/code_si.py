import matplotlib.pyplot as plt
from numpy import arange, array

# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))

# DATA
W = 52        # number of weeks
P = 4.2       # selling price for each unit of milk 
s_0 = 100     # starting units of grass
maxUnits = 40 # maximum units of feed that can be converted into milk across the herd

def pasture(p):
    """ calculate units of grass available next week """
    return round(p + 0.61*p*(1-p/300))

def required(t):
    """ calculate units of grass required to feed the herd in week t """
    if t < 18:
        y = 10.241 + 0.13*t
    else:
        y = 10.241 + 0.13*18 + 0.01121*(t-18)**2
    return round(y)

_revenue = {}
def revenue(t,s):

    # if there is not enough grass to feed the herd, the solution is infeasible 
    if s < required(t):
        return (0, "Infeasible")
    
    if (t,s) not in _revenue:
        
        # determine the available grass units once the herd has been fed
        available = s - required(t)
        
        # determine how much grass is available at the end of the week
        available_next = pasture(s)-required(t)

        if t == 51:
            _revenue[t,s] = max((P*a, a) for a in range(min(maxUnits+1, available+1)))

        else:
            _revenue[t,s] = max((P*a + revenue(t+1, available_next-a)[0], a) 
                                for a in range(min(maxUnits+1, available+1)))

    return _revenue[t,s]

def get_feed_amounts():
    """ determine the number of units of feed given to the herd each week """
    feed_amounts = [0] * W
    extra_feed = [0] * W
    required_feed = [0] * W
    s = s_0
    total = 0

    for t in range(W):
        feed_amounts[t] = revenue(t,s)[1] + required(t)
        extra_feed[t] = revenue(t,s)[1]
        required_feed[t] = required(t)
        total += P * revenue(t,s)[1]
        s = pasture(s) - revenue(t,s)[1] - required(t)
    
    print(f"Total revenue calculated using feed amounts: {round(total, 3)}")
    print(f"\nTOTAL FEED PER WEEK:")
    print(f"{'-'*65}\n| {'Week':<6} {'Feed':<6} | {'Week':<6} {'Feed':<6} | ", end='')
    print(f"{'Week':<6} {'Feed':<6} | {'Week':<6} {'Feed':<6} |\n|{'-'*63}|")
    for n in range(13):
        print(f"| {n:<6} {feed_amounts[n]:<6} | {13+n:<6} {feed_amounts[13+n]:<6} | ", end='')
        print(f"{26+n:<6} {feed_amounts[26+n]:<6} | {39+n:<6} {feed_amounts[39+n]:<6} |")
    print(f"{'-'*65}\n")

    print(f"\nEXTRA FEED GIVEN FOR PROFIT:")
    print(f"{'-'*65}\n| {'Week':<6} {'Feed':<6} | {'Week':<6} {'Feed':<6} | ", end='')
    print(f"{'Week':<6} {'Feed':<6} | {'Week':<6} {'Feed':<6} |\n|{'-'*63}|")
    for n in range(13):
        print(f"| {n:<6} {extra_feed[n]:<6} | {13+n:<6} {extra_feed[13+n]:<6} | ", end='')
        print(f"{26+n:<6} {extra_feed[26+n]:<6} | {39+n:<6} {extra_feed[39+n]:<6} |")
    print(f"{'-'*65}\n")

    return feed_amounts, extra_feed, required_feed

print(f"\nTOTALS:\n{'-'*65}")
print(f"Total revenue from milk sold: {round(revenue(0, s_0)[0], 3)}")
feed, extra, req = get_feed_amounts()

total_feed = 0
total_feed_end = 0
week_count = 0
week_count_end = 0
for t in range(W):
    if feed[t] > 40 and feed[t] <= 50:
        week_count += 1
        total_feed += feed[t]
    if feed[t] > 50:
        week_count_end += 1
        total_feed_end += feed[t]

print(f"Average weekly feed in the middle of the year ({week_count} weeks): {round(total_feed / week_count, 2)}")
print(f"Average weekly feed at the end of the year ({week_count_end} weeks): {round(total_feed_end / week_count_end, 2)}")

# edit settings 
plt.figure(facecolor = '#008080') 
plt.rcParams['axes.facecolor'] = '#008080'
plt.rcParams.update({'text.color'       : 'white',
                     'axes.labelcolor'  : 'white',
                     'xtick.color'      : 'white',
                     'ytick.color'      : 'white'
                     })

ax = plt.gca()
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('#008080')
ax.spines['right'].set_color('#008080')
ax.yaxis.grid = True

# plot the optimal feed strategy 
x = arange(0,52)
y = array(feed)
plt.xticks(arange(min(x), max(x), 2.0))
plt.bar(x, y, color='white')
plt.xlabel ('Week')
plt.ylabel ('Feed')
plt.tight_layout()

plt.show()

# edit settings 
plt.figure(facecolor = 'black') 
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams.update({'text.color'       : 'white',
                     'axes.labelcolor'  : 'white',
                     'xtick.color'      : 'white',
                     'ytick.color'      : 'white'
                     })

ax = plt.gca()
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('black')
ax.spines['right'].set_color('black')

# plot a breakdown of the optimal feed strategy 
x = arange(0,52)
plt.xticks(arange(min(x), max(x), 2.0))
plt.plot(x, extra, color='#00A08F', label='extra')
plt.plot(x, feed, color='#124653', label='total')
plt.plot(x, req, color='#FEE074', label='required')
plt.xlabel ('Week')
plt.ylabel ('Feed')
plt.tight_layout()
plt.legend(loc='best')

plt.show()

