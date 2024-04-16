---
geometry: margin=2cm
---
# Pt10

### Sets
- $F:$ Farms
- $P:$ Facilities
- $T:$ Tankers
- $R:$ Milkruns
- $K:$ Milktypes

### Data
- $Supply_{f}$ - milk supply from each farm $f \in F$ (L)
- $PMin_{p}$ - minimum daily processing at processing facility $p \in P$ (L)
- $PMax_{p}$ - maximum daily processing at processing facility $p \in P$ (L)
- $Maintenance_{t}$ - daily cost of maintenance for tanker $t \in T$
- $MMax$ - maximum number of minutes a tanker can be used for each day (min)
- $RunP_{r}$ - origin processing facility for milk run $r \in R$
- $RunF_{r}$ - farms visited by milk run $r \in R$
- $RunT_{r}$ - time taken to complete milk run $r \in R$ (min)
- $RunC_{r}$ - cost of travel for milk run $r \in R$ ($)
- $RunO_{r}$ - binary variable indicating whether a run is organic
- $BFarms$ - delay between farms on a milk run (min)
- $BRuns$ - cleaning time between milk runs (min)
- $DClean$ - cost of deep clean between organic and non-organic milk runs ($)

### Variables
- $A_{ptk} = \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ has a milkrun for milktype } k \in K \\ 0 &\quad \textrm{otherwise} \end{cases}$

- $B_{pt} = \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ has both organic and non organic runs} \\ 0 &\quad \textrm{otherwise} \end{cases}$

- $W_{pt} = \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ is used for milk runs} \\ 0 &\quad \textrm{otherwise} \end{cases}$

- $X_{prt} = \begin{cases} 1 &\quad \textrm{if tanker } t \in T \textrm{ from } p \in P \textrm{ performs milk run } r \in R \\ 0 &\quad \textrm{otherwise} \end{cases}$

- $Y_{prt}$ - number of extra minutes taken by a tanker $t \in T$ from facility $p \in P$ between farms on a milk run $r \in R$

- $Z_{pt}$ - number of routes each tanker $t \in T$ from processing facility $p \in P$ is assigned to 

### Objective function
$$\textrm{min} \Big(\sum_{p \in P} \, \sum_{r \in R} \, \sum_{t \in T} \big( X_{prt} \times C_{r} \big) + \sum_{p \in P} \, \sum_{t \in T} \big( W_{pt} \times Maintenance_{t} + O_{pt} \times DClean\big) \Big)$$

### Constraints
- Total milk processed at processing facility $p \in P$ cannnot exceed the processing capacity. 
$$\sum_{r \in R} \, \sum_{t \in T} \, \sum_{\substack{ f \in F \textrm{ st. } \\ f \in RunF_{r}}} X_{prt} \times Supply_{f} \leq PMax_{p}, \quad \forall p \in P$$

- Total milk processed at processing facility $p \in P$ must meet the minimal operational requirement. 
$$\sum_{r \in R} \, \sum_{t \in T} \, \sum_{\substack{ f \in F \textrm{ st. } \\ f \in RunF_{r}}} X_{prt} \times Supply_{f} \geq PMin_{p}, \quad \forall p \in P$$

- Each tanker $t \in T$ from processing facility $p \in P$ cannot be operational for more than $10$ hours ($600$ min) including breaks. 
$$\Bigg( \sum_{r \in R} X_{prt} \times RunT_{r} + Y_{prt} \Bigg) + \Big( Z_{pt} - W_{pt} \Big) \times BRuns \leq MMax, \quad \forall p \in P, \; t \in T$$

- The number of routes a tanker is assigned to equals the sum of route assignments to that tanker and processing facility. 
$$Z_{pt} = \sum_{r \in R} X_{prt}, \quad \forall p \in P, \; t \in T$$

- Set binary variables to indicate the milk type on each run performed by a tanker.
$$X_{prt} = 1 \implies A_{ptk} = 1, \quad \forall p \in P, \; t \in T, \; r \in R \textrm{ such that } RunO_{r} = k$$

- If a tanker is not used, variables indicating whether the run is organic must not be set. 
$$W_{pt} = 0 \implies A_{ptk} = 0, \quad \forall p \in P, \; t \in T, \; k \in K$$

- If a tanker $t \in T$ from facility $p \in P$ has both organic and non-organic milk runs, set the binary variable to indicate this.
$$
B_{pt} = \begin{cases} 
1, &\quad \textrm{ if } \sum_{k \in K} A_{ptk} = 2 \\
0, &\quad \textrm{ if } \sum_{k \in K} A_{ptk} < 2
\end{cases}
$$

- If a milkrun does not originate from processing facility $p \in P$, it cannot be assigned to a tanker at that facility.
$$X_{prt} = 0, \quad \forall p \in P, \; t \in T, \; r \in R \textrm{ if } RunP_{r} \neq p $$ 

- If a tanker $t \in T$ is used, the binary tanker variable must be set. 
$$X_{prt} = 1 \implies W_{pt} = 1, \quad \forall p \in P, \; t \in T, \; r \in R$$

- Tankers must be used in order, i.e., tanker 1 and then tanker 2 etc., 
$$W_{pt} = 1 \implies W_{p(t-1)} = 1, \quad \forall p \in P, \; t \in T, \; t > 0$$

- If a milk run is assigned to a tanker and processing facility and the run visits multiple farms, the number of minutes required for breaks between the farms is recorded. If there is only one farm on the milk run, no breaks are required. 
$$
Y_{prt} = \begin{cases} 
X_{prt} \times \big( | RunF_{r} | - 1 \big) \times BFarms, &\quad \textrm{if } | RunF_{r} | > 0 \\
0, &\quad \textrm{otherwise} \end{cases}, \quad \forall p \in P, \; t \in T, \; r \in R 
$$

- Each farm $f \in F$ must be visited on one of the assigned routes. 
$$\sum_{p \in P} \, \sum_{r \in R} \, \sum_{t \in T} X_{prt} = 1, \quad \forall f \in F \textrm{ such that } f \in RunF_{r}$$

