# Apr. 6:
## demonstrates how clean simulation code could be

# seeding
import random as rand
import numpy as np
np.random.seed(123)
rand.seed(123)

# build sim
from build_null import *
b = null_model()
cs, ns = make_tracked_cells(N=9)
place_cells(b, cs, ns)

# make vis
import Visualizer
v = Visualizer.Visualizer(b.width, b.height, b)

# vis and run sim
v.display("test")
for i in range(200):
    b.update()
v.display("post-200")

# analyze results
from experiment_utils import color_subtrees
color_subtrees(ns)
v.display("colored")

from experiment_utils import count_living_subtrees
print(count_living_subtrees(ns))



