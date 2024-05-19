= Communication 11

== Sets
- $C$ - cows
- $T$ - time (week)
\
== Data
- $P$ - price of the milk from per unit of grass (\$) $= 4.2$
- $R_t$ - units of grass required to feed the herd in week $t$
- $G \(S_t\)$ - units of grass available next week given $S_t$ the amount at the start of week t
- $S_0$ - units of grass on the field at time initially $= 100$
- $"MF"$ - maximum units of feed that can be converted into milk across the herd $= 40$
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
- End of the season, compute feed amount for week 51 maximising the profit
$ V_51 = max(a times P," "forall a in A_51) $
\
== General Case
- explore the action space $A_t$ to find the optimal feeding strategy that maximises the profit \
$ V_t (S_t) = max(a times P + V_(t+1) (G (S_t) - a - R_t)," "forall a in A_t) $

#pagebreak()

= Communication 12

== Sets
- $C$ - cows
- $T$ - time (week)
\
== Data
- $P$ - price of the milk from per unit of grass (\$) $= 4.2$
- $R_t$ - units of grass required to feed the herd in week $t$
- $G \(S_t\)$ - units of grass available next week given $S_t$ the amount at the start of week t
- $S_0$ - units of grass on the field at time initially $= 100$
- $"MF"$ - maximum units of feed that can be converted into milk across the herd $= 40$
- $"MG"$ - minimum units of grass before penalty is applied $= 150$
- $L$ - penalty cost per unit under 150 (\$) $= 5$
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
- End of the season, compute feed amount for week 51 maximising the profit taking penalty for each unit under 150 into consideration \
$ V_51 = max(a times P - L times (G (S_51) - a - R_51)," "forall a in A_51)) $
\
== General Case
- explore the action space $A_t$ to find the optimal feeding strategy that maximises the profit \
$ V_t (S_t) = max(a times P + V_(t+1) (G (S_t) - a - R_t)," "forall a in A_t) $

#pagebreak()

= Communication 13

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

#pagebreak()

= Communication 14

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
- $"MF"$ - maximum units of feed that can be converted into milk across the herd $= 10 times (4-d)$
- $"MG"$ - minimum units of grass before penalty is applied $= 150$
- $L$ - penalty cost per unit under 150 (\$) $= 5$
- $P_"good"$ - probability of having good weather in the region $= 0.5$
- $"DRF"$ - dry reduced feed in units of grass $= 3$
\
== Stages
- Weeks - $0 <= t <= 51$
\
== State
- $S_t$ - pasture at the start of week t
- $d$ - number of dried cows
\
== Action
- $A_t = [0, min(S_t, "MF")]$   - extra feed to the herd on week t
- $D = {d, d+1}$             - dry a cow or not
\
== Value Function
$ V_t (S_t, d) = "maximum expected income if we start week" t "with" S_t "pasture and " d "cows dried" $
\
== Base Case
- Insufficient units of pasture to meet the feeding requirement $->$ Infeasible\ $forall 0 <= t <= 51," "S_t <= R_t - d times "DRF" -> V_t (S_t, d) = -infinity$
- End of the season, apply penalty for each unit under 150
    - All cows dried $->$ deterministic\
        $V_51 (S_51, 4) = -L times (P_"good" times (G (S_51, "good") - R_51 + 4 times "DRF") + (1 - P_"good") times (G (S_51, "bad")) - R_51 + 4 times "DRF")$
    \
    - otherwise $->$ compute feed amount for week 51 taking penalty into consideration to maximise the profit\
        $V_51 (S_51, d) = max(a times P - L times (P_"good" times (G (S_51, "good") - a - R_51 + d times "DRF") + (1 - P_"good") times (G (S_51, "bad") - a - R_51 + d times "DRF"))," "forall a in A_51))$
\
== General Case
- All cows dried $->$ deterministic, compute to end of the season\
    $V_t (S_t, 4) = P_"good" times V_(t+1) (G (S_t, "good") - a - R_t - 4 times "DRF") + (1 - P_"good") times V_(t+1) (G (S_t, "bad") - a - R_t - 4 times "DRF")$
\
- otherwise $->$ explore the action space $D times A_t$ - $("dry a cow?") times ("different amount of extra feed")$ to find the optimal strategy that maximises the profit\
    $V_t (S_t, d) = max(a times P + P_"good" times V_(t+1) (G (S_t, "good") - a - R_t - d times "DRF", d') + (1 - P_"good") times V_(t+1) (G (S_t, "bad") - a - R_t - d times "DRF", d')," "forall a in A_t," "forall d' in D)$

#pagebreak()

= Communication 15

== Sets
- $C$ - cows
- $T$ - time (week)
\
== Data
- $P$ - price of the milk from per unit of grass (\$) $= 4.2$
- $G \(S_t, "good"\)$ - units of grass available next week if the weather is good, given $S_t$ pasture at the start of week $t$
- $G \(S_t, "bad"\)$ - units of grass available next week if the weather is bad, given $S_t$ pasture at the start of week $t$
- $S_0$ - units of grass on the field at time initially $= 100$
- $"MF"$ - maximum units of feed that can be converted into milk across the herd $= 10 times sum l$
- $"MG"$ - minimum units of grass before penalty is applied $= 150$
- $L$ - penalty cost per unit under 150 (\$) $= 5$
- $P_"good"$ - probability of having good weather in the region $= 0.5$
- $R_t (l_t)$ - units of grass required to feed each cow in week $t$ given lactating tuple $l_t$
- $l_0 = (1, 1, 1, 1)$
- $l_"dried" = (0, 0, 0, 0)$

\
== Stages
- Weeks - $0 <= t <= 51$
\
== State
- $S_t$ - pasture at the start of week t
- $l_t$ - 4D tuple, specify which cows are still lactating in week $t$
\
== Action
- $A_t = [0, min(S_t, "MF")]$   - extra feed to the herd on week t
- $D_c$                        - dry cow c if c is still lactating
\
== Value Function
$ V_t (S_t, l_t) = "maximum expected income if we start week" t "with" S_t "pasture and lactating pattern" l_t $
\
== Base Case
- Insufficient units of pasture to meet the feeding requirement $->$ Infeasible\ $forall 0 <= t <= 51," "S_t <= R_t (l_t) -> V_t (S_t, l_t) = -infinity$
- End of the season, apply penalty for each unit under 150
    - All cows dried $->$ deterministic\
        $V_51 (S_51, l_"dried") = -L times (P_"good" times (G (S_51, "good") - R_51 (l_"dried")) + (1 - P_"good") times (G (S_51, "bad")) - R_51 (l_"dried"))$
    \
    - otherwise $->$ compute feed amount for week 51 taking penalty into consideration to maximise the profit\
        $V_51 (S_51, l_51) = max(a times P - L times (P_"good" times (G (S_51, "good") - a - R_51 (l_51)) + (1 - P_"good") times (G (S_51, "bad") - a - R_51 (l_51)))," "forall a in A_51)$
\
== General Case
- All cows dried $->$ deterministic, compute to end of the season\
    $V_t (S_t, l_"dried") = P_"good" times V_(t+1) (G (S_t, "good") - a - R_t (l_"dried")," "l_"dried") + (1 - P_"good") times V_(t+1) (G (S_t, "bad") - a - R_t (l_"dried")," "l_"dried")$
\
- otherwise $->$ explore the action space $D_c times A_t$ - $("drying cow" c) times ("different amount of extra feed")$ to find the optimal strategy that maximises the profit\
    $V_t (S_t, l_t) = max(a times P + P_"good" times V_(t+1) (G (S_t, "good") - a - R_t (l_t), l_(t+1)) + (1 - P_"good") times V_(t+1) (G (S_t, "bad") - a - R_t (l_t), l_(t+1))," "forall a in A_t," "forall l_(t+1) in {l_t, l_t "with one of the 1s changed to a 0"})$




