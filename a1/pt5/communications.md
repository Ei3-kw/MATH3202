---
geometry: margin=2cm
---


# Pt5

Thank you for your help in improving the revenue from our existing farms. Based on the increased revenue, we are now looking to expand our operations by working with additional farms to satisfy demand from industrial customers.

The six new farms have daily supply and milk fat content as given in the following table:

\begin{tabular}{lllllll}
\textit{\textbf{Farm}} & \textbf{Cowbell} & \textbf{Creamy Acres} & \textbf{Milky Way} & \textbf{Happy Cows} & \textbf{Udder Delight} & \textbf{Fresh Pail} \\
\textbf{Supply (L)}    & 8700             & 5400                  & 8800               & 5400                & 8900                   & 9300                \\
\textbf{Fat (\%)}      & 3.3              & 3.8                   & 3.6                & 3.4                 & 3.5                    & 3.8                
\end{tabular}

Note that none of these farms are organic and we do not have to take all the milk they supply.

The demand figures for whole milk and low fat milk on each day are given below:

\begin{tabular}{llllllll}
\textit{\textbf{Demand (L)}} & \textbf{Mon} & \textbf{Tue} & \textbf{Wed} & \textbf{Thu} & \textbf{Fri} & \textbf{Sat} & \textbf{Sun} \\
\textbf{Whole Milk}          & 13778        & 27488        & 68427        & 13740        & 27428        & 27519        & 82193        \\
\textbf{Low Fat Milk}        & 3485         & 6896         & 17060        & 3543         & 6756         & 6794         & 20733       
\end{tabular}

We do not have to meet all the demand. The wholesale selling prices for whole milk and low fat milk are $0.90/L and $0.92/L, respectively.

We effectively have no limit on production so we process as much milk as we need to every day, storing the finished product if necessary. We have no limit on storage, but there is a cost of $0.05 (5 cents) per litre per day for refrigeration. Once again excess milk fat can be put to other uses.

How should we best plan our milk processing for the next seven days? Please provide us with the total income from this industrial production.

--------------------------------------------------------------------------

It seems that the fluctuations in demand are resulting in some milk being stored for more than two days. However, to avoid spoilage, we must sell milk on the day it is processed or the next day.

Taking this into account, how should we best plan our milk processing for the next seven days? Please provide us with the total income from this industrial production.



### Sets
- $Farms$
- $S$ - Supply
- $F$ - Fat

### Data
- $W_w$ - wholesale price of whole milk ($/L)
- $W_l$ - wholesale price of low fat milk ($/L)
- $F_w$ - fat of whole milk (%)
- $F_l$ - fat of low fat milk (%)
- $S_f$ - supply from each farm (L)
- $F_f$ - fat from each farm (%)
- $C_s$ - cost of storage ($/L/day)
- $D_{wt}$ - demand of whole milk of a day (L)
- $D_{lt}$ - demand of low fat milk of a day (L)


### Variables
- $P_{wft}$ - Production of whole milk from each farm (L) of a day 
- $P_{lft}$ - Production of low fat milk from each farm (L) of a day
- $S_{wt}$ - Whole milk stored (L) on a day
- $S_{lt}$ - Low fat milk stored (L) on a day
- $V_{wt}$ - Whole milk sold (L) on a day
- $V_{lt}$ - Low fat milk sold (L) on a day

### Objective function
$$max(\sum_{t \in Days} W_w * V_{wt} + W_l * V_{lt} - (S_{wt} + S_{lt}) * C_s)$$

### Constraints
$$\forall f \in Farms,\space\forall t \in Days,\space P_{wft} + P_{lft} \leq S_f$$
$$\forall t \in Days,\space \sum_{f\in Farms} F_w * P_{wft} + F_l * P_{lft} \leq \sum_{f \in Farms} S_f * F_f$$
*Monday:*
$$S_{wt} = P_{wft} - V{wt}$$
$$S_{lt} = P_{lft} - V{lt}$$
$$V_{wt} \leq \sum_{f \in Farms} P_{wft}$$
$$V_{lt} \leq \sum_{f \in Farms} P_{lft}$$

*Other Days:*
$$S_{wt} = P_{wft} - V{wt} + S_{wt-1}$$
$$S_{lt} = P_{lft} - V{lt} + S_{lt-1}$$
$$S_{wt-2} \leq V_{wt} \leq \sum_{f \in Farms} P_{wft} + S_{wt-1}$$
$$S_{lt-2} \leq V_{lt} \leq \sum_{f \in Farms} P_{lft} + S_{lt-1}$$


