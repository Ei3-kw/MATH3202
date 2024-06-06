#set text(13pt)
#show par: set block(spacing: 1.3em)



= Q1
== (a)
\
$B = mat(
	2, 0, 0;
	3, 1, 0;
	1, 0, 1;
)$

$b = mat(10; 16; 15;)$

$x_B = B^(-1) b = mat(1/2, 0, 0; -3/2, 1, 0; -1/2, 0, 1;) mat(10;16;15) = mat(5; 1; 10;)$ \
\ and $x_2 = x_3 = 0$

$z_B = mat(3, 0, 0) mat(5; 1; 10) = 15$

\
== (b)
=== Dual Vars:
\
$y = mat(1/2, -3/2, -1/2; 0, 1, 0; 0, 0, 1;) mat(3;0;0) = mat(3/2; 0; 0)$

\
=== Reduced Cost:

$C_2 ' = 2 - mat(3/2, 0, 0) mat(1; 2; 4;) = 2 - 3/2 = 1/2 > 0$

$C_3 ' = 0 - mat(3/2, 0, 0) mat(1; 0; 0;) = - 3/2 < 0$

$therefore "Adding" x_2 "into basis would increase the objective"$

\
=== Leaving Var:
\
$alpha^2 = mat(1/2,0,0;-3/2,1,0;-1/2,0,1;) mat(1;2;4) = mat(1/2;1/2;7/2;)$

==== Ratio:
\
- $x_1 = 5 div 1/2 = 10$
- $x_4 = 1 div 1/2 = 2$
- $x_5 = 10 div 7/2 = 20/7$

$therefore x_4 "has the lowest ratio, " x_4 "leaves basis"$

\
== (c)
New basis $x_1, x_2, x_5$

$B = mat(2,1,0;3,2,0;1,4,1)$

$b = mat(10;16;15)$

$x_B = B^(-1) b = mat(2, -1, 0; -3, 2, 0; 10, -7, 1;) mat(10;16;15) = mat(4; 2; 3)$ \

$z_B = mat(3, 2, 0) mat(4; 2; 3) = 16$

=== Dual Vars:
\
$y = mat(2, -3, 10; -1, 2, -7; 0, 0, 1;) mat(3;2;0) = mat(0; 1; 0)$

\
=== Reduced Cost:

$C_3 ' = 0 - mat(0, 1, 0) mat(1; 0; 0) = 0$

$C_3 ' = 0 - mat(0, 1, 0) mat(0; 1; 0) = - 1 < 0$

$therefore C_3 ' <= 0 and C_4 ' <= 0$

$therefore "solution is optimal"$
$ x_1 = 4 $
$ x_2 = 2 $
$ x_3 = 0 $
$ x_4 = 0 $
$ x_5 = 3 $
$ z = 16 $

= (d)
$C_3 ' = 0 --> $ Coefficient can be changed to any positive number.
\
= (e)

$ z^Delta = y^T (b + Delta e^j) \ = y^T b + y^T Delta e^j \ = z + Delta y_j $

Dual var is $n = 1$ in the second constraint
$-> z = z + n delta = z + delta$

#pagebreak()

= Q2
== (a)
=== Sets
- S - Stores
- W - warehouse sites
\
=== Data
- $C_w$ - cost for warehouse $w in W$
- $A_w$ - capacity of warehouse
- $d_(s, w)$ - cost of supplying $s in S$ from $w in W$
- $t_s$ - tonnes of orders for $s in S$
\
=== Variables
- $x_(s, w) in {0, 1}$ assign store $s in S$ to warehouse $w in W$
- $y_w in {0, 1}$ build warehouse $w in W$ at site
\
=== Objective
$ min sum_(s in S) sum_(w in W) d_(s,w) times x_(s,w) + sum_(w in W) C_w times y_w $
\
=== Constraints
- Warehouse capacity
	$ sum_(s in S) t_s times x_(s, w) <= A_w times y_w, forall w in W$

- Assign each store to a warehouse
$ sum_(w in W) x_(s,w) = 1, forall s in S $

#emph("check all the data and make sure they're used somewhere.")

#pagebreak()

== (b)
#emph("inherite everything from (a)")
=== Sets
- $S' subset S$ - set of chain stores
\
=== Variables
- $z_w in {0, 1}$ - if $w in W$ supplies a chain store
\
=== Constraints
- At least K warehouses
	$ sum_(w in W) z_w >= K $
- Link z to x
	$ z_w <= sum_(s in S') x_(s, w), forall w in W $
- Ar most 2 chain stores per warehouse
	$ sum_(s in S') x_(s, w) <= 2, forall w in W $

#pagebreak()


= Q3
== Part A
#emph("(a)")
=== Data
- $P_(f, a)$ - probability of winning a race given fatigue $f$ and action $a$
- $d_a$ - change in fatigue from action $a$

=== Stages
- $t in T$ - races

=== State
- $f_t$ - fatigue at start of race $t$

=== Action
- $A_t = {0, 1}$, where
	- $0$ - not enter the race
	- $1$ - entering the race

=== Value Function
- $V_t (f_t)$ - total expected score when starting race $t$ with fatigue $f_t$
- Base case
$ V_T (f_T) = P_(f_T, 1) $
- General case
$ V_t (f_t) = max_(a_t in A_t) {P_(f_t, a_t) + V_(t+1) (max (f_t + d_(a_t), 0))} $

#emph("(b)")

$f_1 = 0$

$V_1(0) = max{1/2 + V_2(3), V_2(0) = 6/5$

$V_2(0) = max{1/2 + V_2(3), V_3(0) = 1$

$V_2(3) = max{1/5 + V_2(6), V_3(0) = 7/10$

$V_3(0) = max{1/2 + V_4(3), V_4(0) = 7/10$

$V_3(3) = max{1/5 + V_4(6), V_4(0) = 1/2$

$V_3(5) = max{1/8 + V_4(9), V_4(2) = 1/4$


$V_4(0) = 1/2,$
$V_4(2) = 1/4,$
$V_4(3) = 1/5,$
$V_4(6) = 1/8,$
$V_4(9) = 1/11$

$therefore$ Race 1 - YES, 2 - NO, 3 - YES, 4 - YES.
#pagebreak()

== Part B

=== Data
- $P_(f, a)$ - probability of winning a race given fatigue $f$ and action $a$
- $p_3$ - probability of fatigue increase by 3 after a race

=== Stages
- $t in T$ - races

=== State
- $f_t$ - fatigue at start of race $t$
- $W_t$ - number of races have been won at the start of race $t$

=== Action
- $A_t = {0, 1}$, where
	- $0$ - not enter the race
	- $1$ - entering the race

=== Value Function
- $V_t (f_t, W_t)$ - chance of wining $>= 3$ races when starting race $t$ with fatigue $f_t$ and current num of wins $W_t$

- Base case
	- $forall 0 <= t <= T, W_t >= 3 --> V_t(f_t, W_t) = 1$
	- $forall 0 <= t <= T, W_t + (T - t + 1) < 3 --> V_t(f_t, W_t) = 0$
	- $t = T, V_T (f_T, W_T) = P_(f_T, 1)$

- General case
$ V_t (f_t, W_t) = max{V_(t+1)^("race"), V_(t+1)^("not race")} $

where

- $V_(t+1)^("not race") = V_(t+1)(max(f_t - 4, 0), W_t)$
- $V_(t+1)^("race") = P_(f_t, 1) times V_(t+1)^"win" + 1 - P_(f_t, 1)) times V_(t+1)^"lose"$, where
	- $V_(t+1)^"win" = p_3 times V_(t+1)(f_t + 3, W_t + 1) + (1-p_3) times V_(t+1)(f_t + 2 , W_t + 1)$
	- $V_(t+1)^"lose" = p_3 times V_(t+1)(f_t + 3, W_t) + (1-p_3) times V_(t+1)(f_t + 2 , W_t)$




