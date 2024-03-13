# Pt1

Teal Cow Dairy has a long history of providing quality products to customers. We are hoping you can help us maintain that quality while also improving our income.

One of the most important factors in our production is milk fat content. Our dairy is supplied by five dairy farms. For each farm we know the daily supply in litres and the milk fat content as a percentage, as set out below:

$\begin{tabular}{llllll}
\textit{\textbf{Farm}} & \textbf{Barnwood} & \textbf{Thistlebrook} & \textbf{Rustic Ranch} & \textbf{Haven} & \textbf{Silo Springs} \\
\textbf{Supply (L)}    & 9600              & 5300                  & 9300                  & 9200           & 7100                  \\
\textbf{Fat (\%)}      & 3.4               & 3.6                   & 3.8                   & 3.6            & 3.7                  
\end{tabular}$

We produce whole milk and low fat milk. Whole milk contains 4% milk fat and sells for $1.10 per litre. Low fat milk contains 1% milk fat and sells for $1.12 per litre. We process the supplied milk into whole milk and low fat milk so that the total milk fat content of production equals the total milk fat of supply.

How much whole milk and low fat milk should we produce from this total supply? Please provide us with the optimal daily income.

### Sets
- $Farms$
- $S:$ Supply
- $F:$ Fat

### Data
- $C_w$ - price of whole milk ($/L)
- $C_l$ - price of low fat milk ($/L)
- $F_w$ - fat of whole milk (%)
- $F_l$ - fat of ow fat milk (%)
- $S_f$ - supply from each farm (L)
- $F_f$ - fat from each farm (%)

### Variables
- $P_{wf}$ - Production of whole milk from each farm (L)

### Objective function
$$max(\sum_{f \in Farms} C_w*P_{wf}+C_l*(S_f-P_{wf}))$$

### Constraints
$$\sum_{f \in Farms} F_w*P_{wf} + F_l*(S_f-P_{wf}) = \sum_{f \in Farms} S_f*F_f $$
$$\forall f \in F,\; 0 \leq P_{wf} \leq S_f$$


