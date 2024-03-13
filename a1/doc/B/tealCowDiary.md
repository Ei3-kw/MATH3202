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

Task:
\begin{enumerate}
    \item Brief insights into the: solution, such as identifying key constraints or explaining the effects of the additional requirements and options on costs. 3 marks
\end{enumerate}

## Communication 1
Based on your initial communication, we understand you desire to determine the volume of whole and low fat milk which should be produced from your total supply to maximise income, all subject to constraints on milk fat. 

Your pricing for each of the milk types - whole and low fat - indicates that low fat milk production should be maximised as it shall reap the greatest profit. However, due to the requirement that all fat of your supply is to be used, a large proportion of your supply must still be processed into whole milk to use up this fat in supply. 

Through mathematical modelling, it was determined that to optimise  profit, 35317L of whole milk and 5183L of low fat milk should be processed from the supply of the five farms.

## Communication 2
In response to Haven and Silo Springs converting to organic production and the inclusion of your new organic products, the model we provided previously has been revised to include additional constraints. 

In this revised model, organic milks will now achieve the greatest profit and so, it is inferred that these products will be maximised. 

We have ensured that all organic products are processed only from the supply of the organic suppliers - Haven and Silo Springs. Based on your communication with us, it was also specified that the fat content of organic product is equal to the fat content of organic supply, and similarly for non-organic product and supply. 

With the addition of these new constraints, our mathematical formulations suggest you process 14363.33L of whole organic milk, 1936.67L of low fat organic milk, 20953.33L of whole milk and 3246.67L of low fat milk from your total supply.

## Communication 3
Thank you for bringing these marketing restrictions to our attention. In response to these restrictions, we have revised our model. 

We have added constraints on the percentage of production which can be low fat for each of organic and non-organic products. Further, it is constrained that no more that 15% of production is organic. 

The revised model suggests that from the total supply, 4556.25L of whole organic milk, 1518.75L of low fat organic milk, 25818.75L of whole milk and 8606.25L of low fat milk is processed.


## Communication 4
We are pleased to hear of your increased revenue and have devised a new model to optimise your operations based on your new suppliers and the changed requirements of your operation. 

In this new model, as requested, we have removed all constraints regarding organic products and focus only on standard whole milk and low fat milk. In line with the new information regarding demand for the products, we have implemented a constraint to ensure that the volume of sold milk of each type does not exceed demand on any given day.  

Similarly to out previous responses, the percentage fat in the product is less than or equal to the percentage fat of supply to reflect what is realistically possible in such a scenario. 

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

To address the constraint, we have enforced that each day the cumulative sold milk must include any milk stored from yesterday. This ensures that there will never be milk in storage for more than one day and no stored milk goes towaste. 

Using this new model, the optimised plan for your milk processing over the next seven days is as follows:

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
