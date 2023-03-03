#
# Feb 9.
#

## Functionalities of simulation:

WIDTH = 4
HEIGHT = 5

X = 1
Y = 2
# 1. init.
## initialize a grid with resource & hazard modules. Distribute both & display
from Body import Body
from Hazard import Hazard
from Resource import Resource
from Visualizer import Visualizer
##
import random as rand
import numpy as np

rand.seed(12)
np.random.seed(12)

r = Resource(WIDTH, HEIGHT)
h = Hazard(WIDTH, HEIGHT)
b = Body(WIDTH, HEIGHT, r, h)
v = Visualizer(WIDTH, HEIGHT, b)

#print("resource: ")
#print(b.resource_model)
r.create_resources()
print(b.resource_model)
v.display("resources: ", mode="Resource")
print("hazard: ")
print(b.hazard_model)
print("body: ")
print(b)


#2. add a cell
## place a cell at a position. display
from Cells import Cell

print("Place & Display:")
progenitor = Cell(mutation_rate = 0,
                proliferation_rate=1,
                hazard_resistance=1,
                motility_rate=1,
                x=X,
                y=Y
                )
b.place_cell(progenitor, X,Y)
print(b)

#3 add a cell with links to tree
from Tree import Tree, Node

print("Place & Display with Tree")
progenitor = Cell(mutation_rate = 0,
                proliferation_rate=1,
                hazard_resistance=1,
                motility_rate=1,
                x=X,
                y=Y
                )
root = Node(parent=None, born_location=(X,Y))
progenitor.set_tree_node(root)
t = Tree(root)

b.place_cell(progenitor, X,Y)
print(b)
print(t)


#3. cell cycle.
## a) have cell update, change resources
print("body updates: ")
b.update()
print("resource: ")
print(b.resource_model)
print("hazard: ")
print(b.hazard_model)
print("body: ")
print(b)

print(b.width)
print(b.height)

v = Visualizer(rows=b.height, columns=b.width, body=b)
b.update()
b.update()

v = Visualizer(rows=b.height, columns=b.width, body=b)
## b) have cell update, die from hazards

#4. let the cells go wild.
## test pure mover
## test pure divider
## test mover & divider

