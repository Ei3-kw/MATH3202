---
geometry: margin=2cm
header-includes:
    - \usepackage{multicol}
    - \newcommand{\hideFromPandoc}[1]{#1}
    - \hideFromPandoc{
        \let\Begin\begin
        \let\End\end
      }

    - \usepackage{fancyhdr}
    - \pagestyle{fancy}
    - \fancyhead[LO,LE]{Sophie Ivanovic - s4703035 \\ Jiayi WANG - s4682239}
---
# Section A: Report to the boss
## Communication 3

### Sets
- $F$ - set of supplying farms

### Data
- $O_{w}$ - price of organic whole milk ($/L)
- $O_{l}$ - price of organic low fat milk ($/L)
- $C_{w}$ - price of whole milk ($/L)
- $C_{l}$ - price of low fat milk ($/L)
- $F_{w}$ - fat content of whole milk (%)
- $F_{l}$ - fat content of low fat milk (%)
- $S_{f}$ - supply from each farm $f \in F$ (L)
- $F_{f}$ - fat content of milk from each farm $f \in F$ (%)

- $Org_{f}$ - boolean value representing whether a farm is organic
- MaxPercentLow - maximum percentage of normal and organic milk that can be low fat 
- MaxPercentOrg - maximum percentage of total supply that can be organic

### Variables
- $w_{f}$ - volume of organic whole milk produced from farm $f \in F$ (L)
- $x_{f}$ - volume of organic low fat milk produced from farm $f \in F$ (L)

- $y_{f}$ - volume of normal whole milk produced from farm $f \in F$ (L) 
- $z_{f}$ - volume of normal low fat milk produced from farm $f \in F$ (L) 

### Objective function
The goal is to determine the required volumes of milk of each variety to be processed from supply such that the overall income is maximised. 
$$
\textrm{max} \bigg( \sum_{f \in F} 
    O_{w} \times w_{f} + O_{l} \times x_{f} +
    C_{w} \times y_{f} + C_{l} \times z_{f} \bigg)
$$

### Constraints
- For each farm, the sum of all processed milk is equal to the supply. This ensures supply is not wasted.  
$$ S_{f} = w_{f} + x_{f} + y_{f} + z_{f}, \quad \forall \; f \in F $$

- For non-organic farms, the volume of organic whole and low fat milk processed from its supply must be zero. 
$$ w_{f} = 0, \quad \forall f \in F \textrm{ if not } Org_{f} $$
$$ x_{f} = 0, \quad \forall f \in F \textrm{ if not } Org_{f} $$

- The supplied milk is processed into whole milk and low fat milk so that the total milk fat content of production is at most the total milk fat of the input - excess milk fat can be potentially used for other purposes.
$$
\sum_{f \in F} 
    F_{w} \times (w_{f} + y_{f}) + 
    F_{l} \times (x_{f} + z_{f}) \leq 
    \sum_{f \in F} (w_{f} + x_{f} + y_{f} + z_{f}) \times F_{f}
$$

- The percentage milk fat in organic products must be less than or equal to the percentage milk fat of their input (since organic products can only be produced from organic supply).
$$
\sum_{f \in F} F_{w} \times w_{f} + F_{l} \times x_{f} \leq 
\sum_{f \in F \textrm{ if } Org_{f}} (w_{f} + x_{f}) \times F_{f}
$$

- Low fat milk can make up at most 25% of the total of low fat and whole milk, for each of organic and normal products.
$$ \textrm{MaxPercentLow} \times \bigg( \sum_{f \in F} w_{f} + x_{f} \bigg) \geq \sum_{f \in F} x_{f} $$
$$ \textrm{MaxPercentLow} \times \bigg( \sum_{f \in F} y_{f} + z_{f} \bigg) \geq \sum_{f \in F} z_{f} $$

- Organic products can make up at most 15% of all milk sold.
$$\textrm{MaxPercentOrg} \times \bigg( \sum_{f \in F} S_{f} \bigg) - \bigg( \sum_{f \in F} w_{f} + x_{f} \bigg) \geq 0$$

## Communication 5

### Sets
- $F$ - set of supplying farms 
- $T$ - set of days

### Data
- $W_{w}$ - wholesale price of whole milk ($/L)
- $W_{l}$ - wholesale price of low fat milk ($/L)
- $F_{w}$ - fat content of whole milk (%)
- $F_{l}$ - fat content of low fat milk (%)
- $C_{s}$ - cost of storage ($/L/day)

- $Dw_{t}$ - demand for whole milk each day (L)
- $Dl_{t}$ - demand for low fat milk each day (L)
- $S_{f}$ - supply from each farm $f \in F$ (L)
- $F_{f}$ - fat content of milk from each farm $f \in F$ (%)

### Variables
- $x_{tf}$ - volume of whole milk produced from farm $f \in F$ on day $t \in T$ (L)
- $y_{tf}$ - volume of low fat milk produced from farm $f \in F$ on day $t \in T$ (L)

- $z_{t}$ - volume of whole milk stored on day $t \in T$ (L)
- $w_{t}$ - volume of low fat milk stored on day $t \in T$ (L)

- $a_{t}$ - total volume of whole milk sold on day $t \in T$ (L)
- $b_{t}$ - total volume of low fat milk sold on day $t \in T$ (L)

### Objective function
The goal of the program is to determine the volume of each variety of milk that needs to be processed from the daily supply to achieve a maximal profit, and hence to establish what this optimal profit is. 
$$
\textrm{max} \bigg( \sum_{t \in D} 
    W_{w} \times  a_{t} + 
    W_{l} \times  b_{t} - 
    (z_{t} + w_{t}) \times C_{s} \bigg)
$$

### Constraints
- Each day, for each of the milk varieties, the volume of sold milk cannot exceed the demand for that variety
$$a_{t} \leq Dw_{t}, \quad \forall \; t \in D$$
$$b_{t} \leq Dl_{t}, \quad \forall \; t \in D$$

- The total milk processed each day from each farm must be less than or equal to that farm's daily supply  
$$x_{tf} + y_{tf} \leq S_{f}, \quad \forall \; f \in F, \; t \in D$$

- Each day, the cumulative fat content of processed milk must be less than or equal to the fat content of its input. It is assumed in this constraint that milk fat left over from previous days cannot be used in processing on subsequent days. 
$$\sum_{f \in F} \big( F_{w} \times x_{tf} + F_{l} \times y_{tf} \big) \leq \sum_{f \in F} S_{f} \times F{f}$$

*Monday:*
- On mondays, for each milk variety, the volume of stored milk must equal processed milk minus sold milk 
$$
z_{t} = \bigg( \sum_{f \in F} x_{tf} \bigg) - a_{t}, \quad \forall \; t \in D, \quad \textrm{ and } \quad
w_{t} = \bigg( \sum_{f \in F} y_{tf} \bigg) - b_{t}, \quad \forall \; t \in D
$$

*Other Days:*
- On days other than monday, for each milk variety, the volume of stored milk must equal the sum of the processed milk from that day and stored milk from the previous day (this makes up all available milk to be sold) minus sold milk
$$
z_{t} = \bigg( \sum_{f \in F} x_{tf} \bigg) + z_{t-1} - a_{t}, \quad \forall \; t \in D, \quad \textrm{ and } \quad w_{t} = \bigg( \sum_{f \in F} y_{tf} \bigg) + w_{t-1} - b_{t}, \quad \forall \; t \in D
$$

- For each milk variety, the total sold milk must be greater than or equal to the stored milk from the previous day (as this milk has to be sold and cannot remain in storage)
$$
a_{t} = z_{t-1}, \quad \forall \; t \in D, \quad \textrm{ and } \quad b_{t} = w_{t-1}, \quad \forall \; t \in D
$$

\newpage 

# Section B: Report to the client

## Communication 1
Based on your initial communication, we understand you desire to determine the volume of whole and low fat milk which should be produced from your total daily supply to maximise income, all subject to constraints on milk fat and supply. 

Your pricing for each of the milk types - $1.10 for whole and $1.12 for low fat milk - indicates that low fat milk production should be maximised, as it shall reap the greatest profit for your dairy. However, to ensure that all fat content of your supply is used, as requested, a large proportion of your supply must still be processed into whole milk. Low fat milk only contains 1% fat, while your supply has an average fat content of 3.62% at each farm, so limiting production only to low fat would not utilise all fat from supply and would leave wastage which should be avoided.

In consideration of all constraints you provided to us, we have devised a mathematical model to optimise your daily income while ensuring that all of your supply, including the fat cotent, is used, and the outcome of this model reflects our above expectations. 

Our model reveals that the optimal daily income for your dairy is $44653.67. To achieve this optimal income, out of the total daily supply of 40500L from the five dairy farms, 35316.67L of whole milk and 5183.33L of low fat milk should be processed. In other words, 87.20% of supply should be processed into whole milk and 12.80% into low fat milk. 

Evidently, the proportion of supply that is processed into low fat milk is low compared to whole milk, despite the higher selling price of this product. As was inferred, the restriction you provided on fat content greatly decreases the proportion of low fat milk that can be processed, thus restricting daily income. We suggest that this restriction on fat content is loosened to allow for more production of low fat milk. 

## Communication 2
In response to Haven and Silo Springs converting to organic production and with the inclusion of your new organic products, we revised the model we provided previously to include additional constraints and variables to match your new circumstance.  

In this revised model, organic milks will now achieve the greatest profit since they sell for $0.20 more than their non-organic equivalents and so, it is evident that maximising the volume of organic products produced will maximise income. Any non-organic milk production in an optimised plan will be due to other restrictions such as those on organic supply. 

The revised mathematical model ensures that all organic products are processed only from the supply of the organic suppliers - Haven and Silo Springs - to guarantee the quality of the product as requested. Based on your communication with us, it has also been specified that for each farm, the total fat content of product is equal to the fat content of supply and further, the fat content of organic product is equal to the fat content of its input.

With the addition of these new constraints, our formulations suggest that your daily supply is processed into product in the following manner: 14363.33L of whole organic milk, 1936.67L of low fat organic milk, 20953.33L of whole milk and 3246.67L of low fat milk. With this production plan, an optimal daily income of $47913.67 is achieved. With the inclusion of organic productions, we are pleased to report that your projected income has increased by $3260.

At this stage, we noticed that due to your specified constraints on production - specifically the limit on organic supply and a requirement that all fat content of supply is used - only 40.25% of your product is organic and 12.80% is low fat despite these being the varieties with the highest selling point. Similarly to before, if you were to consider weakening the arforementioned constraints, the optimal daily income of your dairy would increase. 

## Communication 3
In response to the marketing restrictions that you brought to our attention in your third communication with us, we once again revised our model and hope it will now suit your needs. 

In the third revision of our model, we added constraints on the percentage of production which can be low fat for each of organic and non-organic products - namely, low fat production is capped at 25%. Further, it was specified that no more than 15% of daily milk production could be organic so to follow market trends as required. This constraint in particular had a significant impact on the optimal production plan since the previous optimal plan resulted in 40.25% of production being organic. 

Based on the new model, the optimal income that can be achieved from daily supply is $45967.50. The following table provides an example production plan broken down by supplier which can achieve the optimal income. 

### Table 1 - Example breakdown of daily milk processing by supplier 
\begin{tabular}{l|llllll}
                               & \textbf{Barnwood} & \textbf{Thistlebrook} & \textbf{Rustic Ranch} & \textbf{Haven} & \textbf{Silo Springs} & \textit{\textbf{Total}} \\ \hline
\textbf{Organic Whole Milk}    & 0                 & 0                     & 0                     & 0              & 4556.25               & 4556.25                 \\
\textbf{Organic Low Fat Milk}  & 0                 & 0                     & 0                     & 1518.75        & 0                     & 1518.75                 \\
\textbf{Standard Whole Milk}   & 993.75            & 5300                  & 9300                  & 7681.25        & 2543.75               & 25818.75                \\
\textbf{Standard Low Fat Milk} & 8606.25           & 5300                  & 0                     & 0              & 0                     & 8606.25                
\end{tabular}

As shown above, the revised model suggests that from the total daily supply, 4556.25L of whole organic milk, 1518.75L of low fat organic milk, 25818.75L of whole milk and 8606.25L of low fat milk should processed to achieve an optimal income. This amounts to exactly 15% of supply being processed into organic milk, thus satisfying the marketing restriction on organic milk production. And similarly, exactly 25% of organic and non-organic supply is low fat. 

In addition to creating a model to optimise profit, we conducted analysis on variables and constraints to provide mathematically justified insight into possible directions that can be taken by Teal Cow Dairy to increase income. 

As depicted by the outcome of the model, due to stringent regulations on organic production, a significant portion of organic milk supply is diverted for the production of non-organic milk, thereby decreasing overall income. Considering the restriction of organic production to 15% of the total production, our analysis suggests that total income would increase by $81.00 per 1% increase in this percent up to a cap of 40.25%. For example, allowing 20% of production to be organic would result in a revised income of $46372.5, which is a $405 increase from the previous optimal income. The maximum income that can be achieved by adjusting this constraint is $48012.50, corresponding to 40.25% of total production being organic as opposed to 15%. 

We understand that marketing restrictions prevent such an adjustment from being made at this point; however, it may be possible to take actions to loosed these restrictions, such as utilising marketing campaigns to promote organic products and collaborating with decision makers behind this regulation. 

## Communication 4
We were pleased to hear of your increased revenue and devised a new model to optimise your operations based on your new six suppliers and the changed requirements of your operation. 

In this new model, as requested, we removed all constraints regarding organic products and focussed only on standard whole milk and low fat milk. In line with the new information regarding demand for your products, we implemented a constraint to ensure that the volume of sold milk of each type does not exceed demand on any given day.  

Similarly to our models for the previous stages of your organisational growth, it was ensured that the cumulative percentage fat of product is less than or equal to the percentage fat of its input to reflect what is realistically possible. 

The wholesale price of low fat milk is greater than the wholesale price of whole milk, so it is intuitive that in an optimal solution, the proporthe solution maximises low fat milk production and this is reflected in the results. 

As there is no limit on production apart from the limit on supply from each farm, the final solution reflects that demand is met on each day.

Out devised plan using mathematical modelling is as follows:

### Table 2 - Seven day plan for communication 4
\begin{tabular}{lllll}
\textbf{Day} & \textbf{Category} & \textbf{Sold(L)} & \textbf{Demand(L)} & \textbf{Stored(L)} \\ \hline
\textit{Mon} & Whole             & 13778            & 13778              & 25975.33           \\
             & Low Fat           & 3485             & 3485               & 3261.67            \\
             &                   &                  &                    &                    \\
\textit{Tue} & Whole             & 27488            & 27488              & 31039.67           \\
\textit{}    & Low Fat           & 6896             & 6896               & 10313.33           \\
             &                   &                  &                    &                    \\
\textit{Wed} & Whole             & 68427            & 68427              & 2366               \\
\textit{}    & Low Fat           & 17060            & 17060              & 0                  \\
             &                   &                  &                    &                    \\
\textit{Thu} & Whole             & 13740            & 13740              & 28379.33           \\
\textit{}    & Low Fat           & 3543             & 3543               & 3203.67            \\
             &                   &                  &                    &                    \\
\textit{Fri} & Whole             & 27428            & 27428              & 29865.33           \\
\textit{}    & Low Fat           & 6756             & 6756               & 14099.67           \\
             &                   &                  &                    &                    \\
\textit{Sat} & Whole             & 27519            & 27519              & 42099.67           \\
\textit{}    & Low Fat           & 6794             & 6794               & 13989.33           \\
             &                   &                  &                    &                    \\
\textit{Sun} & Whole             & 81853            & 82193              & 0                  \\
             & Low Fat           & 20733            & 20733              & 0                 
\end{tabular}

## Communication 5
Your final communication with us introduced an important constraint on duration of milk storage and in resoponse to this, we once again updated our model. 

To address this constraint, we enforced that each day the cumulative sold milk must include any milk stored from the previous day. This ensures that there will never be milk in storage for more than one day, and no stored milk goes to waste. 

Using this new model, the optimised plan for your milk processing over the next seven days is as follows:

### Table 3 - Seven day plan for communication 4
\begin{tabular}{lllll}
\textbf{Day} & \textbf{Category} & \textbf{Sold(L)} & \textbf{Demand(L)} & \textbf{Stored(L)} \\ \hline
\textit{Mon} & Whole             & 13778            & 13778              & 24161.4            \\
             & Low Fat           & 3485             & 3485               & 2709.6             \\
             &                   &                  &                    &                    \\
\textit{Tue} & Whole             & 27488            & 27488              & 28673.67           \\
\textit{}    & Low Fat           & 6896             & 6896               & 10313.33           \\
             &                   &                  &                    &                    \\
\textit{Wed} & Whole             & 68427            & 68427              & 0                  \\
\textit{}    & Low Fat           & 17060            & 17060              & 0                  \\
             &                   &                  &                    &                    \\
\textit{Thu} & Whole             & 13740            & 13740              & 19274.67           \\
\textit{}    & Low Fat           & 3543             & 3543               & 2722.33            \\
             &                   &                  &                    &                    \\
\textit{Fri} & Whole             & 27428            & 27428              & 27519              \\
\textit{}    & Low Fat           & 6756             & 6756               & 6794               \\
             &                   &                  &                    &                    \\
\textit{Sat} & Whole             & 27519            & 27519              & 32513.67           \\
\textit{}    & Low Fat           & 6794             & 6794               & 13986.33           \\
             &                   &                  &                    &                    \\
\textit{Sun} & Whole             & 72267            & 82193              & 0                  \\
             & Low Fat           & 20733            & 20733              & 0                 
\end{tabular}

The total weekly income you can expect using this plan is $277194.54. This income is based on 250647L of whole milk and 65267L of low fat milk being sold in total over the week. 

As shown above, with this plan, milk demands for each variety are met every day except Sunday, which should be a source of satisfaction for customers. However, there is opportunity for further income in the 9926L of whole milk demand that is not being met on a Sunday, and this should be considered when moving forward with the business. Additionally, since demand is almost completely met and is restricting further sales, it may be worthwhile to implement marketing strategies to potentially increase demand so that sales can increase. 

In addition to creating this model and our general insights, we once again performed mathematical analysis on the solution to provide insight into potential opportunities for future growth. Our analysis shows that increasing the supply from each of the farms could increase the optimal income. For example, the daily supply from Fresh Pail is currently 9300L. For every litre of milk added to this supply, we predict an extra $0.90 can be earned on a Sunday, $0.85 on a Saturday, $0.10 on a Wednesday and $0.05 on either a Tuesday or Friday. However, it should be noted that this is not an unbounded constraint and after a certain volume of supply, this increase in profit is no longer guaranteed. The bound changes depending on the day and farm. 

