---
geometry: margin=2cm
---
# Pt6

### Sets
- $F:$ Farms
- $P:$ Facilities

### Data
- $Supply_{f}$ - milk supply from each farm $f \in F$ (L)
- $Distance_{fp}$ - distance between farm $f \in F$ and processing facility $p \in P$ (km) 
- $PMin$ - minimum daily processing at processing facility $p \in P$ (L)
- $PMax$ - maximum daily processing at processing facility $p \in P$ (L)
- $TRound$ - cost of round trip travel ($/km)

### Variables
- $X_{fp}$ - boolean assignment of farms $f \in F$ to processing facilities $p \in P$

### Objective function
$$\textrm{min} \Big(\sum_{f \in F} \sum_{p \in P}  Distance_{fp} \times TRound \Big)$$

### Constraints
- Total milk processed at processing facility $p \in P$ cannnot exceed the processing capacity. 
$$\sum_{f \in F} X_{fp} \times Supply_{f} \leq PMax, \quad \forall p \in P$$

- Total milk processed at processing facility $p \in P$ must meet the minimal operational requirement. 
$$\sum_{f \in F} X_{fp} \times Supply_{f} \geq PMin, \quad \forall p \in P$$

- Each farm $f \in F$ must be assigned to exactly one processing facility. 
$$\sum_{p \in P} X_{fp} = 1, \quad \forall f \in F$$



