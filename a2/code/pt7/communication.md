---
geometry: margin=2cm
---
# Pt7

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

