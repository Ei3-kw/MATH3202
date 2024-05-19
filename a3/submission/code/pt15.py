import matplotlib.pyplot as plt
from numpy import arange, array

# SETS
names = ['Lily', 'Betty', 'Clover', 'Rosie']

cows = [
    [2.444, 0.0311, 0.00251],
    [2.454, 0.0376, 0.00255],
    [2.715, 0.0283, 0.00318],
    [2.628, 0.033, 0.00297]
]

C = range(len(cows))
W = 52

# DATA
P   = 4.2               # selling price for each unit of milk
L   = 5.0               # penalty cost per unit under 150
s_0 = 100               # starting units of grass
l_0 = (1,1,1,1)         # starting condition of cows
minGrass  = 150         # minimum units of grass before a penalty is applied
PGood     = 0.5         # probability of having good weather in the region
maxMilkUnits = 10       # maximum units of feed that can be converted into milk per cow

""" returns the units of grass below 150 """
def penalty_grass(x):
    x -= minGrass
    return 0 if x >= 0 else abs(x)

""" returns the required feed for each cow each week in units of grass """
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

_revenue = {}
def revenue(t,s,l):

    # insufficient units of pasture to meet the feeding requirement
    if s < dryenergy(t, l):
        return (-float('inf'), "Infeasible")
    
    if (t,s,l) not in _revenue:

        # determine how many units of feed can be converted to milk this week
        maxUnits = sum(l)*maxMilkUnits

        # determine the current available grass units
        available = s-dryenergy(t, l)
        
        # determine how much grass is available at the end of the week for each weather scenario
        available_good = pasture(s,'Good')-dryenergy(t, l)
        available_poor = pasture(s,'Poor')-dryenergy(t, l)

        # base case - end of season, apply penalty for each unit under 150
        if t == 51:
            # all cows dried
            if sum(l) == 0:
                _revenue[t,s,l] = (PGood * (-L*penalty_grass(available_good))
                    + (1-PGood) * (-L*penalty_grass(available_poor)), (0, l))
            else:
                _revenue[t,s,l] = max((PGood * (P*a - L*penalty_grass(available_good-a))
                    + (1-PGood) * (P*a - L*penalty_grass(available_poor-a)), (a, l))
                for a in range(min(maxUnits+1, available+1)))
        else: # general case
            # all cows dried
            if sum(l) == 0:
                # no profit can be made if all cows are dry so there are no actions to consider
                _revenue[t,s,l] = (PGood * revenue(t+1, available_good, l)[0]
                    + (1-PGood) * revenue(t+1, available_poor, l)[0], (0, l))
            else: # explore (drying cow c or not) X (diff extra feed)
                _revenue[t,s,l] = max((PGood * (P*a + revenue(t+1, available_good-a, l)[0])
                    + (1-PGood) * (P*a + revenue(t+1, available_poor-a, l)[0]), (a, l))
                for a in range(min(maxUnits+1, available+1)))

                # add the option of drying a cow that's not yet dried
                dried = {}
                for i in C:
                    if l[i]:
                        new_l = list(l)
                        new_l[i] = 0
                        new_l = tuple(new_l)
                        dried[new_l] = max((PGood * (P*a + revenue(t+1, available_good-a, new_l)[0])
                            + (1-PGood) * (P*a + revenue(t+1, available_poor-a, new_l)[0]),
                            (a, new_l)) for a in range(min(maxUnits+1, available+1)))

                _revenue[t,s,l] = max(max(dried.values()), _revenue[t,s,l])

    return _revenue[t,s,l]


if __name__ == '__main__':
    print(f"Total revenue from milk sold: {round(revenue(0, s_0, l_0)[0], 2)}")

    feed_dict = {}
    l = l_0
    for t in range(52):
        for p in range(0, 300):
            rev = revenue(t, p, l)
            if rev[1][0] != 'Infeasible' and rev[1][0] == maxMilkUnits * sum(l):
                feed_dict[t] = tuple((p, l))
                if rev[1][1] != "Infeasible" and sum(rev[1][1]) < sum(l):
                    for i in range(4):
                        if rev[1][1][i] < l[i]:
                            print(names[i])
                    l = rev[1][1]
                break

    print(f"\nREQUIRED PASTURE FOR OPTIMAL STRATEGY:")
    print(f"{'-'*113}\n| {'Week':<6} {'Pasture':<9} {'Dry Cows':<8} | {'Week':<6} {'Pasture':<9} {'Dry Cows':<8} | ", end='')
    print(f"{'Week':<6} {'Pasture':<9} {'Dry Cows':<8} | {'Week':<6} {'Pasture':<9} {'Dry Cows':<8} |\n|{'-'*111}|")

    # print initial pasture each week and number of dried cows
    for t in range(13):
        for i in range(4):
            l = feed_dict[t+13*i][1]
            dry_cows = ''
            for j in range(4):
                if l[j] == 0:
                    dry_cows = dry_cows + names[j][0] + ' '
            if i == 3:
                print(f"| {t+13*i:<6} {feed_dict[t+13*i][0]:<9} {dry_cows:<8} |")
            else:
                print(f"| {t+13*i:<6} {feed_dict[t+13*i][0]:<9} {dry_cows:<8} ", end='')
    print(f"{'-'*113}\n")

    feed0, feed1, feed2, feed3, feed4 = ([] for i in range(5))
    x0, x1, x2, x3, x4 = ([] for i in range(5))
    for t in range(52):
        x = feed_dict[t]
        if sum(x[1]) == 4:
            feed0.append(x[0])
            x0.append(t)
        elif sum(x[1]) == 3:
            if len(x1) == 0:
                feed0.append(x[0])
                x0.append(t)
            feed1.append(x[0])
            x1.append(t)
        elif sum(x[1]) == 2:
            if len(x2) == 0:
                feed1.append(x[0])
                x1.append(t)
            feed2.append(x[0])
            x2.append(t)
        elif sum(x[1]) == 1:
            if len(x3) == 0:
                feed2.append(x[0])
                x2.append(t)
            feed3.append(x[0])
            x3.append(t)
        elif sum(x[1]) == 0:
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
    plt.ylabel ('Initial Units of Grass')

    plt.show()
