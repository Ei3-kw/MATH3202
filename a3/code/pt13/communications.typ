#set list(indent: 18pt)
#set page(margin: (
    top: 3cm,
    bottom: 2cm,
    x: 2cm,
))
#set text(11pt)
#set par(
    justify: true,
    leading: 1em,
)


= Pt11
\
A new farmer is starting out in our area and needs support in managing his herd of four cows: Emma, Betty, Clarabelle and Phoebe. He has a one-hectare field for the cows to graze on and needs to plan how he should feed the cows each week for a 52-week season.

We measure the amount of grass available in the field in 10 kg units. This field currently has 100 units of grass (i.e. 1000 kg). Each week grass will grow and our modelling suggests the growth is described well by the following function:

```py
def pasture(p):
    return round(p + 0.61*p*(1-p/300))
```

For example, if there are 100 units of grass at the start of a week then there will be 141 units of grass at the start of the following week.

However, each week the farmer needs to feed some of the grass to the herd. The herd requires a minimum amount of feed units to remain healthy and this depends on the time in the season. If the weeks are numbered from 0 to 51 then the required feed is given by the following function:

```py
def required(t):
    if t < 18:
        y = 10.088 + 0.1445*t
    else:
        y = 10.088 + 0.1445*18 + 0.01151*(t-18)**2
    return round(y)
```

At the start of the season the cows have all recently calved and started lactating. The feed required is low because they are using up reserves put on during pregnancy. At the end of the season they will be pregnant again and so their energy demands increase.

The farmer can choose to feed his herd more than this required amount of feed. The cows turn this extra energy into milk. One unit of feed is converted by a cow into milk that sells for \$4.20. Each cow can turn up to 10 units of feed into milk each week.

The farmer will only consider whole numbers of units of feed. By convention, we calculate the new amount of pasture for the following week before subtracting the amount used for feed in the current week (since in reality these are happening simultaneously).

How much should the farmer feed his herd each week during the season? Please provide us with the total revenue from milk sold.

= Pt12
\
We have realised that your proposal will leave the field with very little grass at the end of the season. We would actually like to improve the state of the field so suggest a penalty cost of \$5 per unit for every unit of grass below 150 at the end of the season.

Taking this into account, how much should the farmer feed his herd each week during the season? Please provide us with the total revenue from milk sold, minus any pasture penalty incurred.

= Pt13
\
In practice, the growth of grass depends on whether the weather has been favourable. In this region, half the time we would say the weather will be "Good" for growing, while half the time it will be "Poor". Here is a refinement of the previous growth model to take this into account:
```py
def pasture(p,weather):
    if weather == 'Good':
        return round(p + 0.66*p*(1-p/300))
    else:
        return round(p + 0.56*p*(1-p/300))
```

Incorporating the uncertainty in the weather, how much should the farmer feed his herd each week during the season? Please provide us with the total expected revenue from milk sold, minus any pasture penalty incurred.

#pagebreak()

== Sets
- $C$ - cows
- $T$ - time (week)
\
== Data
- $P$ - price of the milk from per unit of grass (\$) $= 4.2$
- $R_t$ - units of grass required to feed the herd in week $t$
- $G \(S_t, "good"\)$ - units of grass available next week if the weather is good, given $S_t$ pasture at the start of week $t$
- $G \(S_t, "bad"\)$ - units of grass available next week if the weather is bad, given $S_t$ pasture at the start of week $t$
- $S_0$ - units of grass on the field at time initially $= 100$
- $"MF"$ - maximum units of feed that can be converted into milk across the herd $= 40$
- $"MG"$ - minimum units of grass before penalty is applied $= 150$
- $L$ - penalty cost per unit under 150 (\$) $= 5$
- $P_"good"$ - probability of having good weather in the region $= 0.5$
\
== Stages
- Weeks - $0 <= t <= 51$
\
== State
- $S_t$ - pasture at the start of week t
\
== Action
- $A_t = [0, min(S_t, "MF")]$ - extra feed to the herd on week t
\
== Value Function
$ V_t (S_t) = "maximum expected income if we start week" t "with" S_t "pasture" $
\
== Base Case
- Insufficient units of pasture to meet the feeding requirement $->$ Infeasible\
$ forall 0 <= t <= 51," "S_t <= R_t -> V_t (S_t) = -infinity $
- End of the season, compute feed amount for week 51 maximising the profit, and apply penalty for each unit under 150 taking both good and bad weather into consideration
$ V_51 (S_51) = max(a times P - L times (P_"good" times (G (S_51, "good") - a - R_51) + (1 - P_"good") times (G (S_51, "bad") - a - R_51))," "forall a in A_51)) $
\
== General Case
- explore the action space $A_t$ to find the optimal feeding strategy that maximises the profit \
$ V_t (S_t) = max(a times P + P_"good" times V_(t+1) (G (S_t, "good") - a - R_t) + (1 - P_"good") times V_(t+1) (G (S_t, "bad") - a - R_t)," "forall a in A_t) $



