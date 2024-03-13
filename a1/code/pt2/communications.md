# Pt2

Teal Cow Dairy has a long history of providing quality products to customers. We are hoping you can help us maintain that quality while also improving our income.

One of the most important factors in our production is milk fat content. Our dairy is supplied by five dairy farms. For each farm we know the daily supply in litres and the milk fat content as a percentage, as set out below:

$\begin{tabular}{llllll}
\textit{\textbf{Farm}} & \textbf{Barnwood} & \textbf{Thistlebrook} & \textbf{Rustic Ranch} & \textbf{Haven} & \textbf{Silo Springs} \\
\textbf{Supply (L)}    & 9600              & 5300                  & 9300                  & 9200           & 7100                  \\
\textbf{Fat (\%)}      & 3.4               & 3.6                   & 3.8                   & 3.6            & 3.7                  
\end{tabular}$

We produce whole milk and low fat milk. Whole milk contains 4% milk fat and sells for $1.10 per litre. Low fat milk contains 1% milk fat and sells for $1.12 per litre. We process the supplied milk into whole milk and low fat milk so that the total milk fat content of production equals the total milk fat of supply.

How much whole milk and low fat milk should we produce from this total supply? Please provide us with the optimal daily income.

--------------------------------------------------------------------------

Thank you for your initial estimate. However, Haven and Silo Springs are planning to switch to organic production, without any change in volume of supply. Organic whole milk and organic low fat milk sell for 20 cents more per litre compared to normal milks.

We can use organic supply in normal products, but our organic products must use only organic supply. The total milk fat content of each of organic and normal milk production must match the total milk fat content of their inputs.

How much whole milk and low fat milk, both organic and normal, should we produce from the total supply? Please provide us with the revised optimal daily income.


### Sets
- $Farms$
- $S:$ Supply
- $F:$ Fat

### Data
- $O_f$ - Farm being organic (binary)
- $O_w$ - Price of organic whole milk ($/L)
- $O_l$ - Price of organic low fat milk ($/L)
- $C_w$ - price of whole milk ($/L)
- $C_l$ - price of low fat milk ($/L)
- $F_w$ - fat of whole milk (%)
- $F_l$ - fat of low fat milk (%)
- $S_f$ - supply from each farm (L)
- $F_f$ - fat from each farm (%)

### Variables
- $P_{wf}$ - Production of normal whole milk from each farm (L)
- $P_{owf}$ - Production of organic whole milk from each farm (L)
- $P_{olf}$ - Production of organic low fat milk from each farm (L)

### Objective function
$$max(\sum_{f \in Farms} C_w \times P_{wf} + C_l \times (S_f-P_{wf}-P_{olf}-P_{owf}) + O_w \times P_{owf} + O_l \times P_{olf})$$

### Constraints
$$\sum_{f \in Farms} F_w \times (P_{wf}+P_{owf}) + F_l \times (S_f-P_{wf}-P_{owf}) = \sum_{f \in Farms} S_f \times F_f$$
$$\forall f \in F,\; 0 \leq P_{owf} \leq S_f \times O_f-P_{olf}$$
$$\forall f \in F,\; 0 \leq P_{wf} \leq S_f-P_{owf}-P_{olf}$$



