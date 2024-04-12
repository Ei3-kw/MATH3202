---
geometry: margin=2cm
---
# Pt7

### Sets
- $F:$ Farms
- $P:$ Facilities
- $T:$ Tankers

### Data
- $Supply_{f}$ - milk supply from each farm $f \in F$ (L)
- $Distance_{fp}$ - distance between farm $f \in F$ and processing facility $p \in P$ (km) 
- $PMin_{p}$ - minimum daily processing at processing facility $p \in P$ (L)
- $PMax_{p}$ - maximum daily processing at processing facility $p \in P$ (L)
- $Maintenance_{t}$ - daily cost of maintenance for tanker $t \in T$
- $TRound$ - cost of round trip travel ($/km)
- $DMax$ - maximum number of kilometers a tanker can be used for each day (assuming an average speed of $60$km/h)

### Variables
- $W_{pt}$ - binary assignment of tankers $t \in T$ to processing facilities $p \in P$
- $X_{pft}$ - binary assignment of farms $f \in F$ to processing facilities $p \in P$ and tankers $t \in T$

### Objective function
$$\textrm{min} \Big(\sum_{p \in P} \, \sum_{f \in F} \sum_{t \in T}  \big( X_{pft} \times Distance_{fp} \times TRound \big) + \sum_{p \in P} \, \sum_{t \in T} \big( W_{pt} \times Maintenance_{t} \big) \Big)$$

### Constraints
- Total milk processed at processing facility $p \in P$ cannnot exceed the processing capacity. 
$$\sum_{f \in F} \, \sum_{t \in T} X_{pft} \times Supply_{f} \leq PMax_{p}, \quad \forall p \in P$$

- Total milk processed at processing facility $p \in P$ must meet the minimal operational requirement. 
$$\sum_{f \in F} \, \sum_{t \in T} X_{pft} \times Supply_{f} \geq PMin_{p}, \quad \forall p \in P$$

- Each tanker $t \in T$ for processing facility $p \in P$ cannot be operational for more than $10$ hours ($600$km). 
$$\sum_{f \in F} X_{pft} \times Distance_{fp} \times 2 \leq DMax, \quad \forall p \in P, \; t \in T$$

- If a tanker $t \in T$ is used, the binary tanker variable must be set. 
$$X_{pft} = 1 \implies W_{pt} = 1, \quad \forall p \in P, \; t \in T, \; f \in F$$

- Tankers must be used in order, i.e., tanker 1 and then tanker 2 etc., 
$$W_{pt} = 1 \implies W_{p(t-1)} = 1, \quad \forall p \in P, \; t \in T, \; t > 0$$

- Each farm $f \in F$ must be assigned to exactly one processing facility and one tanker. 
$$\sum_{p \in P} \, \sum_{t \in T} X_{pft} = 1, \quad \forall f \in F$$

