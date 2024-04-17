---
geometry: margin=2cm
---
# Pt10

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

