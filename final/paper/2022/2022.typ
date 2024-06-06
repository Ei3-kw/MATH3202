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
=== Sets
- $A subset S$ - adjacent squares

=== Variables
- y_(p, s) - number of adjacent players from the same city $c in C$ if we put player $p in P$ at position $s in S$

=== Objective
$ sum_(p in P) sum_(s in S) x_(p, s) times (R_p + y_(p, s)/2) $

=== Constraints
-

