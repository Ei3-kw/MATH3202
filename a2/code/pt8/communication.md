---
geometry: margin=2cm
---
# Pt7

### Sets
- $F:$ Farms
- $P:$ Facilities
- $T:$ Tankers
- $R:$ Milkruns
- $I=\{\textrm{PF, FARMS, TIME, COST}\}$: Indexes for milkrun list

### Data
- $Milkruns_{ri}$ - list of milkruns $r \in R$ indexed by $i \in I$
- $Supply_{f}$ - milk supply from each farm $f \in F$ (L)
- $PMin_{p}$ - minimum daily processing at processing facility $p \in P$ (L)
- $PMax_{p}$ - maximum daily processing at processing facility $p \in P$ (L)
- $Maintenance_{t}$ - daily cost of maintenance for tanker $t \in T$
- $MMax$ - maximum number of minutes a tanker can be used for each day (min)

### Variables
- $W_{pt}$ - binary assignment of tankers $t \in T$ to processing facilities $p \in P$
- $X_{prt}$ - binary assignment of routes $r \in R$ to processing facilities $p \in P$ and tankers $t \in T$

### Objective function
$$\textrm{min} \Big(\sum_{p \in P} \, \sum_{r \in R} \, \sum_{t \in T} \big( X_{prt} \times Milkruns_{r,\textrm{COST}} \big) + \sum_{p \in P} \, \sum_{t \in T} \big( W_{pt} \times Maintenance_{t} \big) \Big)$$

### Constraints
- Total milk processed at processing facility $p \in P$ cannnot exceed the processing capacity. 
$$\sum_{r \in R} \, \sum_{t \in T} \, \sum_{f \in F \textrm{ st. } f \in Milkruns_{r,\textrm{FARMS}}}X_{prt} \times Supply_{f} \leq PMax_{p}, \quad \forall p \in P$$

- Total milk processed at processing facility $p \in P$ must meet the minimal operational requirement. 
$$\sum_{r \in R} \, \sum_{t \in T} \, \sum_{f \in F \textrm{ st. } f \in Milkruns_{r,\textrm{FARMS}}}X_{prt} \times Supply_{f} \geq PMin_{p}, \quad \forall p \in P$$

- Each tanker $t \in T$ for processing facility $p \in P$ cannot be operational for more than $10$ hours ($600$min). 
$$\sum_{r \in R} X_{prt} \times Milkruns_{r,\textrm{TIME}} \leq MMax, \quad \forall p \in P, \; t \in T$$

- If a tanker $t \in T$ is used, the binary tanker variable must be set. 
$$X_{prt} = 1 \implies W_{pt} = 1, \quad \forall p \in P, \; t \in T, \; r \in R$$

- Tankers must be used in order, i.e., tanker 1 and then tanker 2 etc., 
$$W_{pt} = 1 \implies W_{p(t-1)} = 1, \quad \forall p \in P, \; t \in T, \; t > 0$$

- If a milkrun does not originate from processing facility $p \in P$, it cannot be assigned to a tanker at that facility.
$$X_{prt} = 0, \quad \forall p \in P, \; t \in T, \; r \in R \textrm{ if } Milkruns_{r,\textrm{PF} \neq p}$$ 

- Each farm $f \in F$ must be visited on one of the assigned routes. 
$$\sum_{p \in P} \, \sum_{r \in R} \, \sum_{t \in T} X_{prt} = 1, \quad \forall f \in F \textrm{ such that } f \in Milkruns_{r,\textrm{FARMS}}$$

