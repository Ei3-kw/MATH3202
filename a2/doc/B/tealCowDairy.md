---
geometry: margin=2cm
header-includes:
    - \usepackage{multicol}
    - \usepackage{multirow}
    - \usepackage{pgfplots}
    - \usepackage{color}
    - \definecolor{lightcornflowerblue}{rgb}{0.6, 0.81, 0.93}
    - \definecolor{egyptianblue}{rgb}{0.06, 0.2, 0.65}
    - \definecolor{classicrose}{rgb}{0.98, 0.8, 0.91}
    - \definecolor{frenchrose}{rgb}{0.96, 0.29, 0.54}
    - \definecolor{dollarbill}{rgb}{0.52, 0.73, 0.4}
    - \definecolor{sacramentostategreen}{rgb}{0.0, 0.34, 0.25}
    - \newcommand{\hideFromPandoc}[1]{#1}
    - \hideFromPandoc{
        \let\Begin\begin
        \let\End\end
        }
    - \pgfplotsset{
        every axis plot/.append style={line width=0.8pt},
        }
    - \usepackage{fancyhdr}
    - \pagestyle{fancy}
    - \fancyhead[LO,LE]{Sophie Ivanovic - s4703035 \\ Jiayi WANG - s4682239}
---


# Section A: Internal Report
We were once again consulted by Teal Cow Dairy to maximise the profit of their business subject to certain constraints. An outline of the problem and our resultant mathematical formulations to optimise their business strategy are given in this report. We have also made the Python code available for your perusal. 

## Problem Summary
Teal Cow Dairy are in the process of expanding their operations since their previous communication. They now have additional farms and processing facilities whose relative positions are depicted in the below map: 

\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.8,
    grid = major,
    xmin=-6, xmax=105,
    ymin=5, ymax=105,
    xtick={0,5,...,105},
    ytick={0,5,...,105},
    xticklabel=\empty,
    yticklabel=\empty
]

\addplot[scatter, mark=*, only marks, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
2   18  {Cowbell}
25  11  {Creamy Acres}
10  32  {Milky Way}
2   34  {Happy Cows}
36  16  {Udder Delight}
7   48  {Fresh Pail}
36  41  {Cowabunga}
22  50  {Utopia}
55  23  {Moo Meadows}
61  17  {Bluebell}
55  34  {Harmony}
34  56  {Velvet Valley}
16  69  {Moonybrook}
80  30  {Cloven Hills}
71  56  {Midnight Moo}
67  63  {Willows Bend}
81  48  {Moosa Heads}
91  56  {Dreamy Dairies}
73  98  {Happy Hooves}
89  98  {Highlands}
};

\addplot[scatter, mark=*, only marks, mark = o, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
93  14  PF0
54  84  PF1
13  88  PF2
};

\end{axis}
\end{tikzpicture}

Each of of the processing facilities has a fleet of 5 tanker trucks which are used to collect milk from the supplying farms and transport it to the processing facilities where it is turned into saleable product. The client aims to optimise the use of these tankers in consideration of running, maintenance and cleaning costs and constraints on processing and supply. 

## Mathematical Formulations
### Communication 7
### Sets
- $F:$ Farms
- $P:$ Facilities
- $T:$ Tankers

### Data
- $\textrm{Supply}_{f}$ - milk supply from each farm $f \in F$ (L)
- $\textrm{Distance}_{fp}$ - distance between farm $f \in F$ and processing facility $p \in P$ (km) 
- $\textrm{PMin}_{p}$ - minimum daily processing at processing facility $p \in P$ (L)
- $\textrm{PMax}_{p}$ - maximum daily processing at processing facility $p \in P$ (L)
- $\textrm{Maintenance}_{t}$ - daily cost of maintenance for tanker $t \in T$
- $\textrm{DMax}$ - maximum number of kilometers a tanker can be used for each day (km)
- $\textrm{TRound}$ - cost of round trip travel ($/km)

### Variables
$$
\begin{split}
W_{pt}  &= \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ is operational} \\ 0 &\quad \textrm{otherwise} \end{cases} \\
X_{prt} &= \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ performs milk run } r \in R \\ 0 &\quad \textrm{otherwise} \end{cases}
\end{split}
$$

### Objective function
$$\textrm{min} \Big(\sum_{p \in P} \, \sum_{f \in F} \sum_{t \in T}  \big( X_{pft} \times \textrm{Distance}_{fp} \times \textrm{TRound} \big) + \sum_{p \in P} \, \sum_{t \in T} \big( W_{pt} \times \textrm{Maintenance}_{t} \big) \Big)$$

### Constraints
- Total milk processed at processing facility $p \in P$ cannnot exceed the daily processing capacity.
$$\sum_{f \in F} \, \sum_{t \in T} X_{pft} \times \textrm{Supply}_{f} \leq \textrm{PMax}_{p}, \quad \forall p \in P$$

- Total milk processed at processing facility $p \in P$ must meet the minimal daily operational requirement. 
$$\sum_{f \in F} \, \sum_{t \in T} X_{pft} \times \textrm{Supply}_{f} \geq \textrm{PMin}_{p}, \quad \forall p \in P$$

- Each tanker $t \in T$ for processing facility $p \in P$ cannot be operational for more than $10$ hours ($600$km). 
$$\sum_{f \in F} X_{pft} \times \textrm{Distance}_{fp} \times 2 \leq \textrm{DMax}, \quad \forall p \in P, \; t \in T$$

- If a tanker $t \in T$ is operation, set the binary variable to indicate this. 
$$W_{pt} \geq X_{prt}, \quad \forall p \in P, \; t \in T, \; r \in R$$

- Tankers must be used in order, i.e., tanker 1 and then tanker 2 etc., 
$$W_{pt} \leq W_{p(t-1)}, \quad \forall p \in P, \; t \in T, \; t > 0$$

- Each farm $f \in F$ must be assigned to exactly one processing facility and one tanker. 
$$\sum_{p \in P} \, \sum_{t \in T} X_{pft} = 1, \quad \forall f \in F$$

### Communication 10
### Sets
- $F:$ Farms
- $P:$ Facilities
- $T:$ Tankers
- $R:$ Milkruns
- $K:$ Milk Types

### Data
- $\textrm{Supply}_{f}$ - milk supply from each farm $f \in F$ (L)
- $\textrm{PMin}_{p}$ - minimum daily processing at processing facility $p \in P$ (L)
- $\textrm{PMax}_{p}$ - maximum daily processing at processing facility $p \in P$ (L)
- $\textrm{Maintenance}_{t}$ - daily cost of maintenance for tanker $t \in T$
- $\textrm{MMax}$ - maximum number of minutes a tanker can be used for each day (min)
- $\textrm{DClean}$ - cost of deep clean between organic and non-organic milk runs ($)
- $\textrm{RunP}_{r}$ - origin processing facility for milk run $r \in R$
- $\textrm{RunF}_{r}$ - farms visited on milk run $r \in R$
- $\textrm{RunT}_{r}$ - time taken to complete milk run $r \in R$ (min)
- $\textrm{RunC}_{r}$ - cost of travel for milk run $r \in R$ ($)
- $\textrm{RunO}_{r}$ - binary value indicating whether milk run $r \in R$ is organic
- $\textrm{BFarms}$ - delay between farms on a milk run (min)
- $\textrm{BRuns}$ - cleaning time between milk runs (min)

### Variables
$$
\begin{split}
U_{ptk} &= \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ performs a milk run for milk type } k \in K \\ 0 &\quad \textrm{otherwise} \end{cases} \\
V_{pt}  &= \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ performs both organic and non-organic milk runs} \\ 0 &\quad \textrm{otherwise} \end{cases} \\
W_{pt}  &= \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ is operational} \\ 0 &\quad \textrm{otherwise} \end{cases} \\
X_{prt} &= \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ performs milk run } r \in R \\ 0 &\quad \textrm{otherwise} \end{cases} \\
Y_{prt} &\; \textrm{- number of extra minutes taken by a tanker } t \in T \textrm{ from facility } p \in P \textrm{ between the farms on milk run } r \in R \\
Z_{pt}  &\; \textrm{- number of routes performed by tanker } t \in T \textrm{ from processing facility } p \in P
\end{split}
$$

### Objective function
$$\textrm{min} \Big(\sum_{p \in P} \, \sum_{r \in R} \, \sum_{t \in T} \big( X_{prt} \times \textrm{RunC}_{r} \big) + \sum_{p \in P} \, \sum_{t \in T} \big( W_{pt} \times \textrm{Maintenance}_{t} + V_{pt} \times \textrm{DClean} \big) \Big)$$

### Constraints
- Total milk processed at processing facility $p \in P$ cannnot exceed the daily processing capacity. 
$$\sum_{r \in R} \, \sum_{t \in T} \, \sum_{\substack{ f \in F \textrm{ st. } \\ f \in \textrm{RunF}_{r}}} X_{prt} \times \textrm{Supply}_{f} \leq \textrm{PMax}_{p}, \quad \forall p \in P$$

- Total milk processed at processing facility $p \in P$ must meet the minimal daily operational requirement. 
$$\sum_{r \in R} \, \sum_{t \in T} \, \sum_{\substack{ f \in F \textrm{ st. } \\ f \in \textrm{RunF}_{r}}} X_{prt} \times \textrm{Supply}_{f} \geq \textrm{PMin}_{p}, \quad \forall p \in P$$

- Each tanker $t \in T$ from processing facility $p \in P$ cannot be operational for more than $10$ hours ($600$ min) including any required breaks between farms and milk runs. 
$$\Bigg( \sum_{r \in R} X_{prt} \times \textrm{RunT}_{r} + Y_{prt} \Bigg) + \Big( Z_{pt} - W_{pt} \Big) \times \textrm{BRuns} \leq \textrm{MMax}, \quad \forall p \in P, \; t \in T$$

- The number of routes performed by tanker $t \in T$ from facility $p \in P$ equals the sum of route assignments to that tanker and processing facility. 
$$Z_{pt} = \sum_{r \in R} X_{prt}, \quad \forall p \in P, \; t \in T$$

- If a tanker $t \in T$ from processing facility $p \in P$ performs both organic and non-organic milk runs, set the binary variable to indicate this. 
$$V_{pt} = \Big( \sum_{k \in K} U_{ptk} \Big) - W_{pt}, \quad \forall p \in P, \; t \in T$$

- If a tanker $t \in T$ from processing facility $p \in P$ performs a non-organic milk run, set the binary variable to indicate this. 
$$U_{ptk} >= X_{pr0}, \quad \forall p \in P, \; t \in T, \; r \in R \textrm{ if not RunO}_r$$

- If a tanker $t \in T$ from processing facility $p \in P$ performs an organic milk run, set the binary variable to indicate this. 
$$U_{ptk} >= X_{pr1}, \quad \forall p \in P, \; t \in T, \; r \in R \textrm{ if RunO}_r$$

- If a milk run does not originate from processing facility $p \in P$, it cannot be assigned to a tanker at that facility.
$$X_{prt} = 0, \quad \forall p \in P, \; t \in T, \; r \in R \textrm{ if RunP}_{r} \neq p $$ 

- If a tanker $t \in T$ is operation, set the binary variable to indicate this. 
$$W_{pt} \geq X_{prt}, \quad \forall p \in P, \; t \in T, \; r \in R$$

- If a milk run is assigned to a tanker $t \in T$ and processing facility $p \in P$ and the run visits multiple farms, the number of minutes required for breaks between the farms is recorded. If there is only one farm on the milk run, no breaks are required. 
$$
Y_{prt} = \begin{cases} 
X_{prt} \times \big( | RunF_{r} | - 1 \big) \times \textrm{BFarms}, &\quad \textrm{if } | \textrm{RunF}_{r} | > 0 \\
0, &\quad \textrm{otherwise} 
\end{cases}, \quad \forall p \in P, \; t \in T, \; r \in R 
$$

- Tankers must be used in order, i.e., tanker 1 and then tanker 2 etc., 
$$W_{pt} \leq W_{p(t-1)}, \quad \forall p \in P, \; t \in T, \; t > 0$$

- Each farm $f \in F$ must be visited on one of the assigned routes. 
$$\sum_{p \in P} \, \sum_{r \in R} \, \sum_{t \in T} X_{prt} = 1, \quad \forall f \in F \textrm{ if } f \in \textrm{RunF}_{r}$$

\newpage

# Section B: Report to the client
Minimising cost while continuing to deliver exceptional services is one of the most challenging problems that companies face and we are pleased you chose our operations research firm to find solutions to this problem. After extensive review of the updated business goals and requirements of Teal Cow Dairy, we have devised an optimal strategy for expansion which minimises cost of milk collections while conforming to constraints and regulations. In this report, we provide a break-down of this strategy and offer key insights to support future growth of Teal Cow Dairy. 

## Communication 6
Based on the communicated information, the minimum total cost of collections such that the supply of all dairy farms is transported to processing facilities is $4555. This minimum cost assumes an average speed of 60 km/h for each tanker and an average travel cost of 5 $/km. 

This optimal solution takes into consideration the maximum daily capacities of the processing facilities and the minimum processing requirements to keep the facilities running. 

Broken down by processing facility, the cost of collections in the optimal strategy are as follows:

### Table 1 - Breakdown of collection costs per processing facility 
\begin{tabular}{l|l l}
                & \textbf{Distance (km)}    & \textbf{Cost (\$)}    \\ \hline
\textbf{PF0}    & 636                       & 1590                  \\
\textbf{PF1}    & 578                       & 1445                  \\
\textbf{PF2}    & 608                       & 1520                  \\ \hline
                & 1822                      & 4555
\end{tabular}

Graphically, farms should be assigned to processing facilities as follows:

\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.8,
    grid = major,
    xmin=-6, xmax=105,
    ymin=5, ymax=105,
    xtick={0,5,...,105},
    ytick={0,5,...,105},
    xticklabel=\empty,
    yticklabel=\empty,
    legend pos=outer north east
    ]

\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (25, 11)};           % PF0
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (36, 41)};           % PF1
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 18)};            % PF2

\addplot[scatter, mark=*, only marks, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
2   18  {Cowbell}
25  11  {Creamy Acres}
10  32  {Milky Way}
2   34  {Happy Cows}
36  16  {Udder Delight}
7   48  {Fresh Pail}
36  41  {Cowabunga}
22  50  {Utopia}
55  23  {Moo Meadows}
61  17  {Bluebell}
55  34  {Harmony}
34  56  {Velvet Valley}
16  69  {Moonybrook}
80  30  {Cloven Hills}
71  56  {Midnight Moo}
67  63  {Willows Bend}
81  48  {Moosa Heads}
91  56  {Dreamy Dairies}
73  98  {Happy Hooves}
89  98  {Highlands}
};

% PF0
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (36, 16)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (55, 23)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (61, 17)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (80, 30)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (81, 48)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (91, 56)};

% PF1
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (55, 34)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (34, 56)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (71, 56)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (67, 63)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (73, 98)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (89, 98)};

% PF2
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (10, 32)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 34)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (7, 48)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (22, 50)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (16, 69)};

\addplot[scatter, mark=*, only marks, mark = o, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
93  14  PF0
54  84  PF1
13  88  PF2
};

\legend{PF0, PF1, PF2}

\end{axis}
\end{tikzpicture}

### Key Insights
- The minimum cost of collections is not influenced by either the maximum capacity of the processing facility or the minimum processing requirement. Without these constraints, the optimal solution, including distances travelled by tankers during collection, remains the same, suggesting distances between farms and processing facilities to be the only key influencing factor in cost of collections. 

- As depicted in the graphical representation, there is some overlap in the one-way routes between farms and procesing facilities - for example, Fresh Pail is on the way to Cowbell - which suggests travel time has the potential to be reduced by allowing multiple farms to be collected from on each milk run performed by a tanker. 

- Assuming each processing facility has a single tanker, the optimal strategy requires that each tanker is operational for an average of 10.12 hours per day. 

## Communication 7
In response to your seventh communication, we revised our model to incorporate a fleet of 5 tankers for each processing facility. Considering restrictions on the maximum number of operational hours per day for each tanker and the important factor of maintenance costs, the revised optiminal strategy results in a minimum cost of collections of $6680. This is an increase from the previous estimate, but this is to be expected as additional costs have been introduced in order to account for operational restrictions vital to health and safety of tanker drivers. 

Broken down by processing facility, the revised optimal strategy for the cost of collections is as follows:

### Table 2 - Breakdown of collection costs per processing facility 
\begin{tabular}{l|l l l l}
                & \textbf{Distance (km)}    & \textbf{Travel (\$)}  & \textbf{Maintenance (\$)} & \textit{\textbf{Total (\$)}}  \\ \hline
\textbf{PF0}    & 738                       & 1845                  & 970                       & 2815                          \\
\textbf{PF1}    & 568                       & 1420                  & 500                       & 1920                          \\
\textbf{PF2}    & 578                       & 1445                  & 500                       & 1945                          \\ \hline
                & 1884                      & 4710                  & 1970                      & 6680
\end{tabular}

The revised assignment of farms to processing facilities is as follows:
\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.8,
    grid = major,
    xmin=-6, xmax=105,
    ymin=5, ymax=105,
    xtick={0,5,...,105},
    ytick={0,5,...,105},
    xticklabel=\empty,
    yticklabel=\empty,
    legend pos=outer north east
    ]

\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (36, 16)};       % PF0 - Tanker 1
\addplot[color=lightcornflowerblue,mark=\empty] coordinates {(93, 14) (25, 11)};    % PF0 - Tanker 2
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (36, 41)};       % PF1 - Tanker 1
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 18)};        % PF2 - Tanker 1

\addplot[scatter, mark=*, only marks, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
2   18  {Cowbell}
25  11  {Creamy Acres}
10  32  {Milky Way}
2   34  {Happy Cows}
36  16  {Udder Delight}
7   48  {Fresh Pail}
36  41  {Cowabunga}
22  50  {Utopia}
55  23  {Moo Meadows}
61  17  {Bluebell}
55  34  {Harmony}
34  56  {Velvet Valley}
16  69  {Moonybrook}
80  30  {Cloven Hills}
71  56  {Midnight Moo}
67  63  {Willows Bend}
81  48  {Moosa Heads}
91  56  {Dreamy Dairies}
73  98  {Happy Hooves}
89  98  {Highlands}
};

% PF0 - Tanker 1
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (80, 30)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (81, 48)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (55, 34)};

% PF0 - Tanker 2
\addplot[color=lightcornflowerblue,mark=\empty] coordinates {(93, 14) (55, 23)};
\addplot[color=lightcornflowerblue,mark=\empty] coordinates {(93, 14) (61, 17)};
\addplot[color=lightcornflowerblue,mark=\empty] coordinates {(93, 14) (91, 56)};

% PF1
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (2, 34)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (71, 56)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (67, 63)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (73, 98)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (89, 98)};

% PF2
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (34, 56)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (10, 32)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (7, 48)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (22, 50)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (16, 69)};

\addplot[scatter, mark=*, only marks, mark = o, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
93  14  PF0
54  84  PF1
13  88  PF2
};

\legend{PF0 - Tanker 1, PF0 - Tanker 2, PF1 - Tanker 1, PF2 - Tanker 1}

\end{axis}
\end{tikzpicture}

### Key Insights
- The optimal solution uses the minimum possible number of total tankers between all processing facilities which is to be expected as the maintenance costs of tankers constitute a significant proportion of the total cost of collections - approximately 30%. To further reduce collection costs, Teal Cow Dairy can consider making adjustments to further decrease the number of operational tankers and hence reduce maintenance costs. In particular, in the optimal solution presented, the total collective distance travelled by the tankers to collect the supply of all farms is 1884km. This amounts to 31.4 travel hours for each tanker from which it can be concluded that reducing travel time by 1.4 hours will reduce the number of required tankers to 3, resulting in decreased maintenance costs and overall collection costs. 

- With the introduction of maintenance costs of tankers, additional farms are assigned to PF0 than in the previous optimal solution to allow for only 4 tankers being operational. This increases the total distance needing to be travelled to perform collections from 1822km to 1884km which amounts to a \$310 increase in travel costs. This consideration further establishes a need to optimise milk run routes so that the tankers of PF1 and PF2 have the operational capacity to perform milk runs for all nearby farms. 

## Communication 8
Allowing a tanker to visit multiple farms before returning to the processing facility provides an opportunity for decreasing the total distance travelled by the tanker fleets of each processing facility and hence, the operational time of each tanker and the total cost of collections. Reevaluating the model while taking into account the provided possible routes between farms and processing facilities gives a new minimum cost of collections of $4686. The optimal strategy results in a considerable \$1994 decrease in the cost of collections from the previous communication suggesting these operational changes to be for the benefit of Teal Cow Dairy. 

Broken down by processing facility, the new costs of collections in the optimal strategy are as follows:

### Table 3 - Breakdown of collection costs per processing facility 
\begin{tabular}{l|l l l l}
                & \textbf{Travel Time (min)}    & \textbf{Travel (\$)}  & \textbf{Maintenance (\$)} & \textit{\textbf{Total (\$)}}  \\ \hline
\textbf{PF0}    & 433                           & 960                   & 500                       & 1460                          \\
\textbf{PF1}    & 435                           & 980                   & 500                       & 1480                          \\
\textbf{PF2}    & 495                           & 1246                  & 500                       & 1746                          \\ \hline
                & 1363                          & 3186                  & 1500                      & 4686
\end{tabular}

This revised model takes into account all of the previously provided constraints while substituting information on distances between farms and processing facilities for the pre-computed times of each milk run. As travel time is reduced through allowing multiple farms to be visited on each milk run, only a single tanker from each processing facility needs to be utilised which reduces the cost of maintenance. 

A map of the milk runs which should be performed by each tanker in the the optimal strategy is given below:

\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.8,
    grid = major,
    xmin=-6, xmax=105,
    ymin=5, ymax=105,
    xtick={0,5,...,105},
    ytick={0,5,...,105},
    xticklabel=\empty,
    yticklabel=\empty,
    legend pos=outer north east
    ]

\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (25, 11)};                           % PF0
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (36, 41) (34, 56) (54, 84)};           % PF1
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 18) (22, 50) (13, 88)};  % PF2

\addplot[scatter, mark=*, only marks, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
2   18  {Cowbell}
25  11  {Creamy Acres}
10  32  {Milky Way}
2   34  {Happy Cows}
36  16  {Udder Delight}
7   48  {Fresh Pail}
36  41  {Cowabunga}
22  50  {Utopia}
55  23  {Moo Meadows}
61  17  {Bluebell}
55  34  {Harmony}
34  56  {Velvet Valley}
16  69  {Moonybrook}
80  30  {Cloven Hills}
71  56  {Midnight Moo}
67  63  {Willows Bend}
81  48  {Moosa Heads}
91  56  {Dreamy Dairies}
73  98  {Happy Hooves}
89  98  {Highlands}
};

% PF0
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (36, 16)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (61, 17) (55, 23) (93, 14)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (80, 30) (81, 48) (93, 14)};

% PF1
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (91, 56) (71, 56) (54, 84)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (55, 34) (67, 63) (54, 84)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (73, 98) (89, 98) (54, 84)};

% PF2
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 34) (10, 32) (13, 88)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (7, 48) (16, 69) (13, 88)};

\addplot[scatter, mark=*, only marks, mark = o, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
93  14  PF0
54  84  PF1
13  88  PF2
};

\legend{PF0 - Tanker 1, PF1 - Tanker 1, PF2 - Tanker 1}

\end{axis}
\end{tikzpicture}

### Key Insights
- Since only a single tanker out of each fleet is operational in the optimal strategy, further reduction in maintenance costs is not possible outside of researching alternative maintenance providers with lower daily fees. 

- The cost of collections for processing facility 2 is the greatest out of the three facilities by a margin of more than \$200. This correlates with the high travel times associated with milk runs to and from this facility. To further optimise collections, Teal Cow Dairy may want to consider reaching out to alternative suppliers within the vicinity of PF2 for which there is a lower cost of collections. 

## Communication 9
The mathematical model was again revised to include breaks of 15 minutes between farms on a milk run and 60 minute cleaning breaks between each milk run performed by a tanker. The minimum cost of collections in an optimal strategy which accounts for these breaks is \$5633. This is an increase of \$947 from the previous minimum cost of collections. 

Broken down by processing facility, the revised times and costs of collections are as follows:

### Table 4 - Breakdown of collection costs per processing facility 
\begin{tabular}{l|l l l}
                & \textbf{Travel (\$)}  & \textbf{Maintenance (\$)} & \textit{\textbf{Total (\$)}}  \\ \hline
\textbf{PF0}    & 1234                  & 970                       & 2204                          \\
\textbf{PF1}    & 713                   & 500                       & 1213                          \\
\textbf{PF2}    & 1246                  & 970                       & 2216                          \\ \hline
                & 3193                  & 2440                      & 5633
\end{tabular}

### Table 5 - Breakdown of collection times per processing facility 
\begin{tabular}{l|l l l l}
                & \textbf{Travel (min)} & \textbf{Breaks between farms (min)}   & \textbf{Breaks between runs (min)}    & \textit{\textbf{Total (min)}} \\ \hline
\textbf{PF0}    & 539                   & 30                                    & 180                                   & 749                           \\
\textbf{PF1}    & 312                   & 60                                    & 120                                   & 492                           \\
\textbf{PF2}    & 495                   & 30                                    & 120                                   & 645                           \\ \hline
                & 1346                  & 120                                   & 420                                   & 1886
\end{tabular}

Graphically, the optimal milk run assignments to processing facilities and tankers are as follows:

\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.8,
    grid = major,
    xmin=-6, xmax=105,
    ymin=5, ymax=105,
    xtick={0,5,...,105},
    ytick={0,5,...,105},
    xticklabel=\empty,
    yticklabel=\empty,
    legend pos=outer north east
    ]

\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (25, 11)};                   % PF0 Tanker 1
\addplot[color=lightcornflowerblue,mark=\empty] coordinates {(93, 14) (91, 56)};            % PF0 Tanker 2
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (36, 41) (34, 56) (54, 84)};   % PF1 Tanker 1
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (10, 32)};           % PF2 Tanker 1
\addplot[color=dollarbill,mark=\empty] coordinates {(13, 88) (7, 48) (16, 69) (13, 88)};    % PF2 Tanker 2

\addplot[scatter, mark=*, only marks, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
2   18  {Cowbell}
25  11  {Creamy Acres}
10  32  {Milky Way}
2   34  {Happy Cows}
36  16  {Udder Delight}
7   48  {Fresh Pail}
36  41  {Cowabunga}
22  50  {Utopia}
55  23  {Moo Meadows}
61  17  {Bluebell}
55  34  {Harmony}
34  56  {Velvet Valley}
16  69  {Moonybrook}
80  30  {Cloven Hills}
71  56  {Midnight Moo}
67  63  {Willows Bend}
81  48  {Moosa Heads}
91  56  {Dreamy Dairies}
73  98  {Happy Hooves}
89  98  {Highlands}
};

% PF0 - Tanker 1
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (36, 16)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (80, 30) (55, 34) (93, 14)};

% PF0 - Tanker 2
\addplot[color=lightcornflowerblue,mark=\empty] coordinates {(93, 14) (61, 17) (55, 23) (93, 14)};

% PF1 - Tanker 1
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (89, 98) (73, 98) (54, 84)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (71, 56) (81, 48) (67, 63) (53, 84)};

% PF2 - Tanker 1
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 34)};
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 18) (22, 50) (13, 88)};

\addplot[scatter, mark=*, only marks, mark = o, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
93  14  PF0
54  84  PF1
13  88  PF2
};

\legend{PF0 - Tanker 1, PF0 - Tanker 2, PF1 - Tanker 1, PF2 - Tanker 1, PF2 - Tanker 2}

\end{axis}
\end{tikzpicture}

### Key Insights
- With the inclusion of breaks between farms and milk runs, the time investment in collections is increased resulting in more tankers needing to be used so that no tanker is operational for more than 10 hours. In the revised optimal strategy, 2 tankers from the fleets of processing facilities 0 and 1 need to be operational. This has a significant impact on the minimum cost of collections as it means an extra \$940 needs to be spent on tanker maintenance. This brings the proportion of collection costs attributed to maintenance to 43%. 

- An area for consideration to reduce maintenance costs is increasing the capacity of tankers. The current operational time required to perform all collections for PF2 is only 45 minutes above the maximum for a single tanker. Using a tanker with a higher capacity could reduce the number of runs needed to perform all collections for PF2, thus reducing collection time and the number of necessary tankers. While investing in a new tanker may incur a high immediate cost, the long term savings on daily maintenance costs would cover this cost and result in net profit. 

## Communication 10
Taking into account organic and non-organic suppliers and related constraints, the minimum cost of collections in an optimal solution becomes \$5796. This is only a \$163 increase from the previous solution. 

Broken down by processing facility, the revised times and costs of collections are as follows:

### Table 6 - Breakdown of collection costs per processing facility 
\begin{tabular}{l|l l l}
                & \textbf{Travel (\$)}  & \textbf{Maintenance (\$)} & \textit{\textbf{Total (\$)}}  \\ \hline
\textbf{PF0}    & 934                   & 500                       & 1434                          \\
\textbf{PF1}    & 1176                  & 970                       & 2146                          \\
\textbf{PF2}    & 1246                  & 970                       & 2216                          \\ \hline
                & 3356                  & 2440                      & 5796
\end{tabular}

### Table 7 - Breakdown of collection times per processing facility 
\begin{tabular}{l|l l l l}
                & \textbf{Travel (min)} & \textbf{Breaks between farms (min)}   & \textbf{Breaks between runs (min)}    & \textit{\textbf{Total (min)}} \\ \hline
\textbf{PF0}    & 397                   & 15                                    & 180                                   & 592                           \\
\textbf{PF1}    & 525                   & 60                                    & 180                                   & 765                           \\
\textbf{PF2}    & 495                   & 30                                    & 120                                   & 645                           \\ \hline
                & 1417                  & 105                                   & 480                                   & 2002
\end{tabular}

The revised assignments of milk runs to processing facilities and tankers is as follows:

\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.8,
    grid = major,
    xmin=-6, xmax=105,
    ymin=5, ymax=105,
    xtick={0,5,...,105},
    ytick={0,5,...,105},
    xticklabel=\empty,
    yticklabel=\empty,
    legend pos=outer north east
    ]

\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (25, 11)};                           % PF0 Tanker 1
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (81, 48) (71, 56) (54, 84)};           % PF1 Tanker 1
\addplot[color=classicrose,mark=\empty] coordinates {(54, 84) (34, 56)};                            % PF1 Tanker 2
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (7, 48) (16, 69) (13, 88)};  % PF2 Tanker 1
\addplot[color=dollarbill,mark=\empty] coordinates {(13, 88) (10, 32)};                             % PF2 Tanker 2

\addplot[scatter, mark=*, only marks, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
2   18  {Cowbell}
25  11  {Creamy Acres}
10  32  {Milky Way}
2   34  {Happy Cows}
36  16  {Udder Delight}
7   48  {Fresh Pail}
36  41  {Cowabunga}
22  50  {Utopia}
55  23  {Moo Meadows}
61  17  {Bluebell}
55  34  {Harmony}
34  56  {Velvet Valley}
16  69  {Moonybrook}
80  30  {Cloven Hills}
71  56  {Midnight Moo}
67  63  {Willows Bend}
81  48  {Moosa Heads}
91  56  {Dreamy Dairies}
73  98  {Happy Hooves}
89  98  {Highlands}
};

% PF0
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (36, 16)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (80, 30)};
\addplot[color=egyptianblue,mark=\empty] coordinates {(93, 14) (61, 17) (55, 23) (93, 14)};

% PF1 - Tanker 1
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (91, 56) (67, 63) (54, 84)};
\addplot[color=frenchrose,mark=\empty] coordinates {(54, 84) (89, 98) (73, 98) (54, 84)};

% PF1 - Tanker 2
\addplot[color=classicrose,mark=\empty] coordinates {(54, 84) (55, 34) (36, 41) (54, 84)};

% PF2 - Tanker 1
\addplot[color=sacramentostategreen,mark=\empty] coordinates {(13, 88) (2, 18) (22, 50) (13, 88)};

% PF2 - Tanker 2
\addplot[color=dollarbill,mark=\empty] coordinates {(13, 88) (2, 34)};

\addplot[scatter, mark=*, only marks, mark = o, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
93  14  PF0
54  84  PF1
13  88  PF2
};

\legend{PF0 - Tanker 1, PF1 - Tanker 1, PF1 - Tanker 2, PF2 - Tanker 1, PF2 - Tanker 2}

\end{axis}
\end{tikzpicture}

### Key Insights
- Accounting for the distinction between organic and non-organic milk runs, including adding time for deep cleans between milk runs of different types, does not change the minimum number of operational tankers to perform collections. As with the previous communication, 5 tankers are required in total to perform all milk collections; however, it is now PF1, not PF0, which has two operational tankers. 

- Again, collections for PF2 take 645 minutes in total which is 45 minutes above the maximum operational time of a single tanker suggesting investment into a tanker with a greater capacity to still be a valid area for consideration to reduce costs. It is also worth noting that since all milk runs from PF2 are for non-organic milk, using only one tanker in this way will not incur additional fees for deep cleans. 

- By removing constraints on the maximum capacity and minimum processing requirement of each processing facility the minimum total cost of collections becomes \$5303 which is a decrease of \$493. This decrease comes from a reassignment of milk runs from PF1 to PF2 which reduces the minimum number of required tankers by one, thus cutting maintenance costs. In light of this, to reduce the cost of collections Teal Cow Dairy should consider investing in an increased capacity for PF2 and reduced operational requirement for PF1. 
