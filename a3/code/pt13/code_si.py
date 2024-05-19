import matplotlib.pyplot as plt
from numpy import arange, array

# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))

# DATA
W = 52          # number of weeks
P = 4.2         # selling price for each unit of milk 
L = 5.0         # penalty cost per unit under 150
s_0 = 100       # starting units of grass
minGrass = 150  # minimum units of grass before a penalty is applied 
maxUnits = 40   # maximum units of feed that can be converted into milk across the herd
PGood = 0.5     # probability of having good weather in the region

def penalty_grass(x):
    """ calculate units of grass below 150 """
    x -= minGrass
    return 0 if x >= 0 else abs(x)

def pasture(p,weather):
    """ calculate units of grass available next week given the current weather """
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))
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
        return (-float('inf'), "Infeasible")
    
    if (t,s) not in _revenue:

        # determine the available grass units once the herd has been fed
        available = s - required(t)

        # determine how much grass is available at the end of the week for each weather scenario
        available_good = pasture(s,'Good') - required(t)
        available_poor = pasture(s,'Poor') - required(t)

        if t == 51: 
            # calculate the maximum amount of profit given the penalty for each unit under 150 
            _revenue[t,s] = max((PGood * (P*a - L*penalty_grass(available_good-a)) 
                                 + (1-PGood) * (P*a - L*penalty_grass(available_poor-a)), a) 
                                for a in range(min(maxUnits+1, available+1)))
        
        else:
            _revenue[t,s] = max((PGood * (P*a + revenue(t+1, available_good-a)[0]) 
                                 + (1-PGood) * (P*a + revenue(t+1, available_poor-a)[0]), a) 
                                for a in range(min(maxUnits+1, available+1)))

    return _revenue[t,s]

print(f"\nTOTALS:\n{'-'*69}")
print(f"Total revenue from milk sold: {round(revenue(0,s_0)[0], 2)}\n")

# determine the units of grass required at the beginning of week t so that 40 additional 
# units can be given
feed_dict = {}
for t in range(W):
    for p in range(0, 300):
        rev = revenue(t, p)

        if rev[1] != "Infeasible" and rev[1] >= 30:
            feed_dict[t] = p
            break 

print(f"\nREQUIRED PASTURE FOR OPTIMAL STRATEGY:")
print(f"{'-'*69}\n| {'Week':<6} {'Pasture':<6} | {'Week':<6} {'Pasture':<6} | ", end='')
print(f"{'Week':<6} {'Pasture':<6} | {'Week':<6} {'Pasture':<6} |\n|{'-'*67}|")
for t in range(13):
    for i in range(4):
        print(f"| {t+13*i:<6} ", end='')
        if i == 3:
            print(f"{feed_dict[t+13*i]:<6}  |")
        else:
            print(f"{feed_dict[t+13*i]:<6}  ", end='')
print(f"{'-'*69}\n")

# store the required feed each week in a list 
req = []
for t in range(52):
    req.append(required(t))

# sort the dictionary of feed amounts by week before plotting 
feed = []
for x in range(52):
    feed.append(feed_dict[x])

# edit settings 
plt.figure(facecolor = 'black') 
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams.update({'text.color'       : 'white',
                     'axes.labelcolor'  : 'white',
                     'xtick.color'      : 'white',
                     'ytick.color'      : 'white',
                     'axes.grid' : True, 'grid.color' : '#161616'
                     })

# plot the optimal feed strategy 
x = arange(0,52)
y = array(feed)
plt.subplot(2, 1, 1)
plt.plot(x, y, color='#008080')
plt.xticks(arange(min(x), max(x), 2.0))
plt.yticks(arange(140, 175, 5))
plt.xlabel ('Week')
plt.ylabel ('Initial Units of Grass')
plt.tight_layout()

# plot required feed per week
x = arange(0,52)
y = array(req)
plt.subplot(2, 1, 2)
plt.plot(x, y, color='#008080')
plt.xticks(arange(min(x), max(x), 2.0))
plt.xlabel ('Week')
plt.ylabel ('Feed')
plt.tight_layout()

plt.show()
