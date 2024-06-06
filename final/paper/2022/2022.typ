= Q1

== (d)
$x_2$ is part of basis

$C_B = mat(2, 1-Delta, 0)$

$y = mat(1, -2, 6; -1, 3, -11; 0, 0, 1) mat(2; 1-Delta; 0) = mat(Delta; 1 - 3 Delta; 0)$
\

$Delta$ has negative impact on $x_2$:
$ 1 - 3 Delta < 0 $
$ 1/3 < Delta $
$therefore, C_2 = 1 - 1/3 = 2/3, x_2 = 0$ in the optimal solution.


= Q2

== (a)
=== Sets
- P - players
- C - cities
- S - positions

=== Data
- $C_p$ - cost of a player $p in P$
- $R_p$ - rating of a player $p in P$
- $H_(p, c) in {0, 1}$ - player $p in P$ is from city $c in C$
- $L_p$ - sqares player $p in P$ can play
- $B$ - budget of the team 
- $M$ - minimum number of cities which must be represented in the team
- $O$ - maximum number of players that can be selected from any one city

=== Variables
$x_(p, s) in {0, 1}$ - player $p in P$ play in position $s in S$

=== Objective
$ sum_(p in P) sum_(s in S) x_(p, s) times R_p$

=== Constraints
- within budget
	$ sum_(p in P) sum_(s in S) x_(p, s) times C_p <= B $
- all position filled
	$ sum_(p in P) sum_(s in S) x_(p, s) = 9 $
- player plays at most one position
	$ sum_{s in S} x_(p, s) <= 1, forall p in P $
- city reqs
	$ sum_(p in P) sum_{s in S} x_(p, s) times H_(p, c) <= O, forall c in C $
	$ sum_(p in P) sum_(c in C) H_(p, c) times sum_{s in S} x_(p, s) >= M $


== (b)
=== Data
- $A_s$ - adjacent squares of position $s in S$

=== Variables
- $y_(p, s)$ - number of adjacent players from the same city $c in C$ if we put player $p in P$ at position $s in S$

=== Objective
$ sum_(p in P) sum_(s in S) x_(p, s) times (R_p + y_(p, s)/2) $

=== Constraints
- $forall s' in S, forall p' in P, sum_(s in A_s') sum_(c in C) sum_(p in P) H_(p, c) times x_(p, s) = x_(p', s') times y_(p', s')$


= Q3
== (a)

=== Data
- $k_0 = k$ - currently owns $𝑘$ sheep
- $p_i$ - profit per sheep when sell in year $i$

=== Stages
- $0 <= i <= T$ - years

=== State
- $k_i$ - number of sheep in year $i$

=== Action
- $0 <= S_i <= 2 times k_i$ - number of sheep sold in year $i$

=== Value Function
- $V(i, k_i) :=$ expected profit if we have $k_i$ sheep at the start of year $i$
- Base case:
	$ forall i, k_i < 0 --> V(i, k_i) = 0 $
	$ i = T : V(T, k_T) = p_t times 2 times k_T$
- General case:
	$ V(i, k_i) = p_i times S_i + V(i + 1, 2 times k_i - S_i) $

== (b)

#emph("1.")

=== Data
- $"PFG" = 0.8$ - the chance of soil being good with fertiliser the following year given it's good one year
- $"PFB" = 0.6$ - the chance of soil being good with fertiliser the following year given it's bad one year
- $"PG" = 0.4$ - the chance of soil being good without fertiliser the following year given it's good one year
- $"PB" = 0.1$ the chance of soil being good without fertiliser the following year given it's bad one year
- $E_S = cases(700 ", if" S = 1, 400 ", if" S = 0)$ - expectation of growth given soil condition $S$
- $C = 150$ - Applying fertiliser in a year costs 150

=== Stages
- $0 <= t <= T$ - years

=== State
- $S_t in {0, 1}$ - the condition of the soil in year $t$, where
	- 0 - bad
	- 1 - good

=== Action
- $F_t in {0, 1}$ - fertilise in year $t$, where
	- 0 - don't fertilise
	- 1 - fertilise

=== Value Function
- $V_t(S_t) :=$ expected profit if we start year t with soil condition $S_t$

- Base case: The gardener will retire after $𝑇$ years, with the plot then having no value, regardless of the soil condition.
	$ t = T, V_T(S_T) = 0 $

- General case:
	$ V_t (S_t) = max{E_S_t - C + V_(t+1)^"fertilise", E_S_t + V_(t+1)^"not fertilise"} $
	where
	- $V_(t+1)^"fertilise" = cases(
		"PFG" times V_(t+1)(1) + (1-"PFG") times V_(t+1)(0) ", if" S_t = 1,
		"PFB" times V_(t+1)(1) + (1-"PFB") times V_(t+1)(0) ", if" S_t = 0
	)$
	\
	- $V_(t+1)^"not fertilise" = cases(
		"PG" times V_(t+1)(1) + (1-"PG") times V_(t+1)(0) ", if" S_t = 1,
		"PB" times V_(t+1)(1) + (1-"PB") times V_(t+1)(0) ", if" S_t = 0
	)$




