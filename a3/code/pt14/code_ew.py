import matplotlib.pyplot as plt
from numpy import arange, array
import math

# SETS
cows = ['Lily', 'Betty', 'Clover', 'Rosie']

C = range(len(cows))

# DATA
W = 52           # number of weeks
P = 4.2          # selling price for each unit of milk
L = 5.0          # penalty cost per unit under 150
s_0 = 100        # starting units of grass
minGrass = 150   # minimum units of grass before a penalty is applied
maxUnitsCow = 10 # maximum units of feed that can be converted into milk per cow
PGood = 0.5      # probability of having good weather in the region
dryFeed = 3      # reduction in weekly feed per dry cow
dryable = 1      # maximum number of cows that can be dried off each week

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
def revenue(t,s,d):

    # if there is not enough grass to feed the herd, the solution is infeasible
    if s < required(t) - dryFeed*d:
        return (-float('inf'), ("Infeasible", "Infeasible"))

    if (t,s,d) not in _revenue:

        # determine units of feed that can be converted into milk based on the number of non-dry cows
        maxUnits = (4-d) * maxUnitsCow

        # determine the available grass units once the herd has been fed
        available = s - required(t) + dryFeed*d

        # determine how much grass is available at the end of the week for each weather scenario
        available_good = pasture(s,'Good') - required(t) + dryFeed*d
        available_poor = pasture(s,'Poor') - required(t) + dryFeed*d

        # base case - end of season, apply penalty if required
        if t == 51:
            # all cows dried
            if d == 4:
                _revenue[t,s,d] = (PGood * (-L*penalty_grass(available_good))
                    + (1-PGood) * (-L*penalty_grass(available_poor)), (0, d))
            else:
                _revenue[t,s,d] = max(
                    (PGood * (P*a - L*penalty_grass(available_good-a))
                    + (1-PGood) * (P*a - L*penalty_grass(available_poor-a)), (a, d))
                    for a in range(min(maxUnits+1, available+1)))
        else: # general case
            # all cows dried
            if d == 4:
                _revenue[t,s,d] = (PGood * revenue(t+1, available_good, d)[0]\
                    + (1-PGood) * revenue(t+1, available_poor, d)[0], (0, d))
            else:
                _revenue[t,s,d] = max(
                    (PGood * (P*a + revenue(t+1, available_good-a, d+b)[0])
                        + (1-PGood) * (P*a + revenue(t+1, available_poor-a, d+b)[0]), (a, d+b))
                    for a in range(min(maxUnits+1, available+1)) for b in range(dryable+1))

    return _revenue[t,s,d]

print(f"\nTOTALS:\n{'-'*65}")
print(f"Total revenue from milk sold: {round(revenue(0, s_0, 0)[0], 3)}")

# determine the units of grass required at the beginning of week t so that 40 additional
# units can be given
feed_dict = {}
dryCows = 0
for t in range(52):
    for p in range(0, 300):
        rev = revenue(t, p, dryCows)
        if rev[1][0] == maxUnitsCow * (4-dryCows):
            feed_dict[t] = tuple((p, dryCows))
            if rev[1][1] != "Infeasible" and rev[1][1] > dryCows:
                dryCows += 1
            break

print(f"\nREQUIRED PASTURE FOR OPTIMAL STRATEGY:")
print(f"{'-'*113}\n| {'Week':<6} {'Pasture':<9} {'Dry Cows':<8} | {'Week':<6} {'Pasture':<9} {'Dry Cows':<8} | ", end='')
print(f"{'Week':<6} {'Pasture':<9} {'Dry Cows':<8} | {'Week':<6} {'Pasture':<9} {'Dry Cows':<8} |\n|{'-'*111}|")

# print optimal feed each week and number of dried cows
for t in range(13):
    for i in range(4):
        if i == 3:
            print(f"| {t+13*i:<6} {feed_dict[t+13*i][0]:<9} {feed_dict[t+13*i][1]:<8} |")
        else:
            print(f"| {t+13*i:<6} {feed_dict[t+13*i][0]:<9} {feed_dict[t+13*i][1]:<8} ", end='')

print(f"{'-'*113}\n")

feed0, feed1, feed2, feed3, feed4 = ([] for i in range(5))
x0, x1, x2, x3, x4 = ([] for i in range(5))
for t in range(52):
    x = feed_dict[t]
    if x[1] == 0:
        feed0.append(x[0])
        x0.append(t)
    elif x[1] == 1:
        if len(x1) == 0:
            feed0.append(x[0])
            x0.append(t)
        feed1.append(x[0])
        x1.append(t)
    elif x[1] == 2:
        if len(x2) == 0:
            feed1.append(x[0])
            x1.append(t)
        feed2.append(x[0])
        x2.append(t)
    elif x[1] == 3:
        if len(x3) == 0:
            feed2.append(x[0])
            x2.append(t)
        feed3.append(x[0])
        x3.append(t)
    elif x[1] == 4:
        if len(x4) == 0:
            feed3.append(x[0])
            x3.append(t)
        feed4.append(x[0])
        x4.append(t)
    t += 1

plt.figure(facecolor = 'black')
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams.update({'text.color'       : 'white',
                     'axes.labelcolor'  : 'white',
                     'xtick.color'      : 'white',
                     'ytick.color'      : 'white',
                     'axes.grid' : True, 'grid.color' : '#161616'
                     })

# plot the optimal feed strategy
plt.plot(array(x0), array(feed0), color='#00A08F', label='dry cows = 0')
plt.plot(array(x1), array(feed1), color='#124653', label='dry cows = 1')
plt.plot(array(x2), array(feed2), color='#FEE074', label='dry cows = 2')
plt.plot(array(x3), array(feed3), color='#FF9469', label='dry cows = 3')
plt.plot(array(x4), array(feed4), color='#D5D5D8', label='dry cows = 4')
plt.xticks(arange(0, 52, 2.0))
plt.legend(loc='best')

plt.xlabel ('Week')
plt.ylabel ('Feed')

plt.show()
