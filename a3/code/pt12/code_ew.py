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

def pasture(p):
    return round(p + 0.61*p*(1-p/300))


f_0 = 100
feed_amounts = [0] * 52


@lru_cache(maxsize=None)
def max_revenue(t, grass, remaining):
    max_rev = 0

    # end of the season
    if t == 52:
        return max_rev - max(0, 5 * (150 - remaining))

    r = required(t)
    feed_amounts[t] = r

    for feed in range(r, r+41):
        # update remaining
        remaining = pasture(grass) - feed

        # simulate to end of season assume feeding required
        for d in range(t+1, 52):
            # negative grass remaining -> fail
            if remaining < 0:
                break
            remaining = pasture(remaining) - required(d)

        # Cows can’t eat more than the amount of existing grass
        if feed > grass or remaining < 0:
            continue

        # total = this wk + future - penalty
        total_rev = (feed - r) * P \
            + max_revenue(t + 1, pasture(grass) - feed, remaining) \
            - max(0, 5 * (150 - remaining)) # updating penalty

        if total_rev > max_rev:
            max_rev = total_rev
            feed_amounts[t] = feed

    return max_rev


print(f"Total revenue from milk sold: {max_revenue(0, f_0, f_0)}")
print(feed_amounts)