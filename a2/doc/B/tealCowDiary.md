---
geometry: margin=2cm
header-includes:
    - \usepackage{multicol}
    - \usepackage{pgfplots}
    - \newcommand{\hideFromPandoc}[1]{#1}
    - \hideFromPandoc{
        \let\Begin\begin
        \let\End\end
        }
    - \usepackage{fancyhdr}
    - \pagestyle{fancy}
    - \fancyhead[LO,LE]{Sophie Ivanovic - s4703035 \\ Jiayi WANG - s4682239}
---


# Section A: Internal Report
We were once again consulted by Teal Cow Dairy to maximise the profit of their business subject to certain constraints. An outline of the problem and our resultant mathematical formulations are given in this report. We have also made the Python code available for your perusal. 

## Problem Summary
Teal Cow Dairy are in the process of expanding their operations since their previous communcation. They now have additional farms and processing facilities which are depicted in the below map: 

\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.5,
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

Each of processing facilities has a fleet of 5 tanker trucks which are used to transport collect milk from the supplying farms and transport it to the processing facilities. The client aims to optimise the use of these tankers in consideration of the cost of running them. 

## Communication 7

## Communication 10

# Section B: Report to the client

## Communication 6
Based on the communicated information, the minimum total cost of travel such that the supply of all dairy farms is collected and transported to processing facilities is $4,555. Broken down by processing facility, the cost of collection is as follows:

### Table 1 - Breakdown of transport costs per processing facility 
\begin{tabular}{l|l}
                                    & \textbf{Cost (\$)}  \\ \hline
\textbf{Processing Facility 0}      & 1590                 \\
\textbf{Processing Facility 1}      & 1445                 \\
\textbf{Processing Facility 2}      & 1520
\end{tabular}

The routes which should be chosen are depicted below: 

\begin{tikzpicture}
\tikzstyle{every node}=[font=\tiny]

\begin{axis}[
    scale = 1.5,
    grid = major,
    xmin=-6, xmax=105,
    ymin=5, ymax=105,
    xtick={0,5,...,105},
    ytick={0,5,...,105},
    xticklabel=\empty,
    yticklabel=\empty,
    legend pos=outer north east
    ]

\addplot[color=teal,mark=\empty] coordinates {(93, 14) (25, 11)};
\addplot[color=pink,mark=\empty] coordinates {(54, 84) (36, 41)};
\addplot[color=cyan,mark=\empty] coordinates {(13, 88) (2, 18)};

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

\draw[teal] (axis cs:93,14) -- node[left]{} (axis cs:36,16);
\draw[teal] (axis cs:93,14) -- node[left]{} (axis cs:55,23);
\draw[teal] (axis cs:93,14) -- node[left]{} (axis cs:61,17);
\draw[teal] (axis cs:93,14) -- node[left]{} (axis cs:80,30);
\draw[teal] (axis cs:93,14) -- node[left]{} (axis cs:81,48);
\draw[teal] (axis cs:93,14) -- node[left]{} (axis cs:91,56);

\draw[pink] (axis cs:54,84) -- node[left]{} (axis cs:55,34);
\draw[pink] (axis cs:54,84) -- node[left]{} (axis cs:34,56);
\draw[pink] (axis cs:54,84) -- node[left]{} (axis cs:71,56);
\draw[pink] (axis cs:54,84) -- node[left]{} (axis cs:67,63);
\draw[pink] (axis cs:54,84) -- node[left]{} (axis cs:73,98);
\draw[pink] (axis cs:54,84) -- node[left]{} (axis cs:89,98);

\draw[cyan] (axis cs:13,88) -- node[left]{} (axis cs:10,32);
\draw[cyan] (axis cs:13,88) -- node[left]{} (axis cs:2,34);
\draw[cyan] (axis cs:13,88) -- node[left]{} (axis cs:7,48);
\draw[cyan] (axis cs:13,88) -- node[left]{} (axis cs:22,50);
\draw[cyan] (axis cs:13,88) -- node[left]{} (axis cs:16,69);

\addplot[scatter, mark=*, only marks, mark = o, point meta=explicit symbolic, nodes near coords,] table[x=x, y=y, meta=label] {
x   y   label
93  14  PF0
54  84  PF1
13  88  PF2
};

\legend{PF0 - Tanker 1, PF1 - Tanker 1, PF2 - Tanker 1}

\end{axis}
\end{tikzpicture}

