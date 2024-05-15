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
def max_revenue(t, grass):
    max_rev = 0

    # end of season
    if t == 52:
        return max_rev

    r = required(t)

    for feed in range(r, r+41):
        # Cows can’t eat more than the amount of existing grass
        if feed > grass:
            break

        # total = this wk + furture
        total_rev = (feed - r) * P \
            + max_revenue(t + 1, pasture(grass) - feed)

        if total_rev > max_rev:
            max_rev = total_rev
            feed_amounts[t] = feed

    return max_rev


print(f"Total revenue from milk sold: {max_revenue(0, f_0)}")
print(feed_amounts)
