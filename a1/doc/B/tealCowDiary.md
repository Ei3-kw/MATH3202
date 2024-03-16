---
geometry: margin=2cm
header-includes:
    - \usepackage{multicol}
    - \newcommand{\hideFromPandoc}[1]{#1}
    - \hideFromPandoc{
        \let\Begin\begin
        \let\End\end
      }
---

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

### Table1.1.1
\begin{tabular}{l|llllll}
                               & \textbf{Barnwood} & \textbf{Thistlebrook} & \textbf{Rustic Ranch} & \textbf{Haven} & \textbf{Silo Springs} & \textit{\textbf{Total}} \\ \hline
\textbf{Organic Whole Milk}    & 0                 & 0                     & 0                     & 0              & 4556.25               & 4556.25                 \\
\textbf{Organic Low Fat Milk}  & 0                 & 0                     & 0                     & 1518.75        & 0                     & 1518.75                 \\
\textbf{Standard Whole Milk}   & 993.75            & 5300                  & 9300                  & 7681.25        & 2543.75               & 25818.75                \\
\textbf{Standard Low Fat Milk} & 8606.25           & 5300                  & 0                     & 0              & 0                     & 8606.25                
\end{tabular}

As shown above, the revised model suggests that from the total daily supply, 4556.25L of whole organic milk, 1518.75L of low fat organic milk, 25818.75L of whole milk and 8606.25L of low fat milk should processed to achieve an optimal income. This amounts to exactly 15% of supply being processed into organic milk, thus satisfying the marketing restriction on organic milk production. And similarly, exactly 25% of organic and non-organic supply is low fat. 

### Sensitivity Analysis
In addition to creating a model to optimise profit, we conducted analysis on variables and constraints to provide mathematically justified insight into possible directions that can be taken by Teal Cow Dairy to increase income. 

As depicted by the outcome of the model, due to stringent regulations on organic production, a significant portion of organic milk supply is diverted for the production of non-organic milk, thereby decreasing overall income. Considering the restriction of organic production to 15% of the total production, our analysis suggests that total income would increase by $81.00 per 1% increase in this percent up to a cap of 40.25%. For example, allowing 20% of production to be organic would result in a revised income of $46372.5, which is a $405 increase from the previous optimal income. The maximum income that can be achieved by adjusting this constraint is $48012.50, corresponding to 40.25% of total production being organic as opposed to 15%. 

We understand that marketing restrictions prevent such an adjustment from being made at this point; however, it may be possible to take actions to loosed these restrictions, such as utilising marketing campaigns to promote organic products and collaborating with decision makers behind this regulation. 


## Communication 4
We were pleased to hear of your increased revenue and devised a new model to optimise your operations based on your new suppliers and the changed requirements of your operation. 

In this new model, as requested, we removed all constraints regarding organic products and focussed only on standard whole milk and low fat milk. In line with the new information regarding demand for your products, we have implemented a constraint to ensure that the volume of sold milk of each type does not exceed demand on any given day.  

Similarly to our models for the previous stages of your organisational growth, we ensured the cumulative percentage fat of the product is less than or equal to the percentage fat of supply to reflect what is realistically possible in such a scenario. 

The wholesale price of low fat milk is greater than the wholesale price of whole milk, so it is intuitive that the solution maximises low fat milk production and this is reflected in the results. 

As there is no limit on production apart from the limit on supply from each farm, the final solution reflects that demand is met on each day.

Out devised plan using mathematical modelling is as follows:

\begin{multicols}{2}
\begin{tabular}{llll}
\textbf{Day} & \textbf{Category} & \textbf{Sold(L)} & \textbf{Demand(L)} \\ \hline
\textit{Mon} & Whole             & 13778            & 13778              \\
             & Low Fat           & 3485             & 3485               \\
             &                   &                  &                    \\
\textit{Tue} & Whole             & 27488            & 27488              \\
\textit{}    & Low Fat           & 6896             & 6896               \\
             &                   &                  &                    \\
\textit{Wed} & Whole             & 68427            & 68427              \\
\textit{}    & Low Fat           & 17060            & 17060              \\
             &                   &                  &                    \\
\textit{Thu} & Whole             & 13740            & 13740              \\
\textit{}    & Low Fat           & 3543             & 3543               \\
             &                   &                  &                    \\
\textit{Fri} & Whole             & 27428            & 27428              \\
\textit{}    & Low Fat           & 6756             & 6756               \\
             &                   &                  &                    \\
\textit{Sat} & Whole             & 27519            & 27519              \\
\textit{}    & Low Fat           & 6794             & 6794               \\
             &                   &                  &                    \\
\textit{Sun} & Whole             & 81853            & 82193              \\
             & Low Fat           & 20733            & 20733             
\end{tabular}

\begin{tabular}{lll}
\textbf{Day} & \textbf{Catogory} & \textbf{Amount(L)} \\ \hline
\textit{Mon} & Whole             & 18774.33           \\
             & Low Fat           & 10462.6            \\
\textit{}    &                   &                    \\
\textit{Tue} & Whole             & 31039.67           \\
\textit{}    & Low Fat           & 10313.33           \\
             &                   &                    \\
\textit{Wed} & Whole             & 2366               \\
\textit{}    & Low Fat           & 0                  \\
             &                   &                    \\
\textit{Thu} & Whole             & 25826              \\
\textit{}    & Low Fat           & 5757               \\
             &                   &                    \\
\textit{Fri} & Whole             & 37218.67           \\
\textit{}    & Low Fat           & 678.3              \\
             &                   &                    \\
\textit{Sat} & Whole             & 49453              \\
\textit{}    & Low Fat           & 6633               \\
             &                   &                    \\
\textit{Sun} & Whole             & 0                  \\
             & Low Fat           & 0                 
\end{tabular}

\end{multicols}


## Communication 5
We recognise the importance of this constraint on duration of milk storage and have once again updated out model to reflect this requirement. 

To address the constraint, we have enforced that each day the cumulative sold milk must include any milk stored from the previous day. This ensures that there will never be milk in storage for more than one day, and no stored milk goes to waste. 

Using this new model, the optimised plan for your milk processing over the next seven days, split into milk to sell and to store, is as follows:

\begin{multicols}{2}

\begin{tabular}{llll}
\textbf{Day} & \textbf{Category} & \textbf{Sold(L)} & \textbf{Demand(L)} \\ \hline
\textit{Mon} & Whole             & 13778            & 13778              \\
             & Low Fat           & 3485             & 3485               \\
             &                   &                  &                    \\
\textit{Tue} & Whole             & 27488            & 27488              \\
\textit{}    & Low Fat           & 6896             & 6896               \\
             &                   &                  &                    \\
\textit{Wed} & Whole             & 68427            & 68427              \\
\textit{}    & Low Fat           & 17060            & 17060              \\
             &                   &                  &                    \\
\textit{Thu} & Whole             & 13740            & 13740              \\
\textit{}    & Low Fat           & 3543             & 3543               \\
             &                   &                  &                    \\
\textit{Fri} & Whole             & 27428            & 27428              \\
\textit{}    & Low Fat           & 6756             & 6756               \\
             &                   &                  &                    \\
\textit{Sat} & Whole             & 27519            & 27519              \\
\textit{}    & Low Fat           & 6794             & 6794               \\
             &                   &                  &                    \\
\textit{Sun} & Whole             & 72267            & 82193              \\
             & Low Fat           & 20733            & 20733             
\end{tabular}


\begin{tabular}{lll}
\textbf{Day} & \textbf{Catogory} & \textbf{Amount(L)} \\ \hline
\textit{Mon} & Whole             & 19975              \\
             & Low Fat           & 6896               \\
\textit{}    &                   &                    \\
\textit{Tue} & Whole             & 32240.33           \\
\textit{}    & Low Fat           & 6746.67            \\
             &                   &                    \\
\textit{Wed} & Whole             & 0                  \\
\textit{}    & Low Fat           & 0                  \\
             &                   &                    \\
\textit{Thu} & Whole             & 15241              \\
\textit{}    & Low Fat           & 6756               \\
             &                   &                    \\
\textit{Fri} & Whole             & 27519              \\
\textit{}    & Low Fat           & 6794               \\
             &                   &                    \\
\textit{Sat} & Whole             & 39753.33           \\
\textit{}    & Low Fat           & 6746.67            \\
             &                   &                    \\
\textit{Sun} & Whole             & 0                  \\
             & Low Fat           & 0                 
\end{tabular}

\end{multicols}

The total weekly income you can expect using this plan is $277194.54. This income is based on 250647L of whole milk and 65267L of low fat milk being sold in total over the week. As shown above, with this plan, milk demands for each variety are met every day except Sunday which should be a source of satisfaction for customers. 

In addition to creating this model, we have perform some analysis on the data to provide insight into potential opportunities for growth. Our analysis has shown that on each day of the week except sunday, demand for both whole milk and low fat milk is being met. This is restricting profit as it is assumed in the model that demand cannot be exceeded. Thus, an oppotunity for growth exists here. Through implementing marketing strategies it may be possible to increase demand for the products, thus allowing more sales. 

An opportunity for growth exists in increasing the supply from each of the farms. For example, the daily supply from Fresh Pail is currently 9300L. For every litre of milk added to this supply, an extra $0.90 can be earned on a Sunday, $0.85 on a Saturday, $0.10 on a Wednesday and $0.05 on either a Tuesday or Friday. However, it should be noted that this is not an unbounded constraint and after a certain volume of supply, this increase in profit is no longer quaranteed. The bound changes depending on the day.  

In consideration of the constraint on fat percentage, each day there is left over fat from supply which is not utilised - displayed in the slack variables of the model. It is recommended that this excess fat is stored and put to use in other capacities to eliminate waste. 

