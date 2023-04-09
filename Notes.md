#
## Apr. 7

Laplace Distribution Info
```python
import numpy as np

# Generate a Laplace distribution
mean = 0
scale = 1
laplace_dist = abs(np.random.laplace(mean, scale, size=1000))

# Compute the third quartile
q3 = np.percentile(laplace_dist, 75)

print("Third quartile of Laplace distribution:", q3)
```

We also have a `MAX_ENERGY` constant in energy sims that dictates total
energy a cell can hold. Changing this value might affect sims?

making tracked-cells tied together with tree nodes is bad if done too high-up
because it makes copying difficult.


## PROBLEM:
I have a deepcopy of nodes, and the original changes after the simulation
I don't pass the original to the function, and I can't see a single pointer
to it..
# Explanation:
Deepcopy didn't call itself recursively. I wound up setting fields for a 
new node with things like `new.children = self.children`, which didn't copy
the field, and instead gave the new node a reference to the old node's field,
so when the new node changed something it also changed for the old node
