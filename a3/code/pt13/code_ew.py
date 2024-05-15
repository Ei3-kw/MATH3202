from functools import lru_cache

# Sets
cows = ["Emma", "Betty", "Clarabelle", "Phoebe"]
C = range(len(cows))
T = range(52)

# Data
P = 4.2

def required(t):
    if t < 18:
        y = 10.088 + 0.1445*t
    else:
        y = 10.088 + 0.1445*18 + 0.01151*(t-18)**2
    return round(y)

def pasture(p, weather):
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))

f_0 = 100
feed_amounts = [0] * 52

@lru_cache(maxsize=None)
def max_revenue(t, grass_good, grass_poor, remaining):
    max_rev = 0

    # end of the season
    if t == 52:
        return max_rev - max(0, 5 * (150 - remaining))

    r = required(t)
    feed_amounts[t] = r

    for feed in range(r, r+41):
        # update remaining for both weather conditions
        remaining_good = pasture(grass_good, 'Good') - feed
        remaining_poor = pasture(grass_poor, 'Poor') - feed

        # simulate to end of season assume feeding required
        for d in range(t+1, 52):
            # negative grass remaining -> fail
            if remaining_good < 0 or remaining_poor < 0:
                break

            remaining_good = pasture(remaining_good, 'Good') - required(d)
            remaining_poor = pasture(remaining_poor, 'Poor') - required(d)

        # Cows can't eat more than the amount of existing grass
        if feed > grass_good or feed > grass_poor or remaining_good < 0 or remaining_poor < 0:
            break

        # total = this wk + future - penalty
        total_rev = (feed - r) * P \
                    + 0.5 * (max_revenue(t + 1, pasture(grass_good, 'Good') - feed, pasture(grass_poor, 'Good') - feed, remaining_good) \
                        + max_revenue(t + 1, pasture(grass_good, 'Poor') - feed, pasture(grass_poor, 'Poor') - feed, remaining_poor)) \
                    - 0.5 * (max(0, 5 * (150 - remaining_good)) + max(0, 5 * (150 - remaining_poor)))

        if total_rev > max_rev:
            max_rev = total_rev
            feed_amounts[t] = feed

    return max_rev

total_revenue = max_revenue(0, f_0, f_0, f_0)
print(f"Total expected revenue from milk sold: {total_revenue}")
print(feed_amounts)