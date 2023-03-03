## Mar 3. Hardcoded basics that became experiment_utils
from Body import Body
from Cell import Cell
from Hazard import Hazard
from Resource import Resource
from Visualizer import Visualizer
from Tree import Tree, Node

import random as rand
import numpy as np

W= 1000
H= 1000

INIT_X = 500
INIT_Y = 500
GENERATIONS = 100

rand.seed(123)
np.random.seed(123)

import time

h = Hazard(W, H)
r = Resource(W, H)
b = Body(W, H, r, h) # body doesn't know visualizer yet
v = Visualizer(W,H, b)
c = Cell(mutation_rate = 0,
        proliferation_rate = 0.1,
        hazard_resistance = 100,
        motility_rate = 1,
        x = INIT_X,
        y = INIT_Y 
        )
b.place_cell(c, INIT_X, INIT_Y)
c_node = Node(parent = None, born_location = (INIT_X, INIT_Y), cell = c)

#v.display("resources: ", mode = "Resource")
#v.display("hazards: ", mode = "Hazard")
#v.display("cells: ", mode = "Cell")

start = time.time()

for i in range(GENERATIONS):
    print("GENERATION: ", i)
    b.update()

end = time.time()

print("Time: ", str(end-start))

v.display("cells")


