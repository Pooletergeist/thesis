### Problem: sometimes prints cells forever ###


#3 add a cell with links to tree
from Body import Body
from Hazard import Hazard
from Resource import Resource
from Tree import Tree, Node
from Cells import debugCell
import random as rand

rand.seed(423) # run it 3x and it breaks... Seed not constant?

WIDTH = 4
HEIGHT = 5

X = 1
Y = 2

cell_number = 0
r = Resource(WIDTH, HEIGHT)
h = Hazard(WIDTH, HEIGHT)
b = Body(WIDTH, HEIGHT, r, h)
print("Place & Display with Tree")
progenitor = debugCell(mutation_rate = 0,
                proliferation_rate=0,
                hazard_resistance=1,
                motility_rate=1,
                x=X,
                y=Y,
                idn=cell_number
                )
cell_number += 1
root = Node(parent=None, born_location=(X,Y))
progenitor.set_tree_node(root)
t = Tree(root)

b.place_cell(progenitor, X,Y)
print(b)
print(t)

## breaks?
print("body updates: ")
b.update()
print("resource: ")
print(b.resource_model)
print("hazard: ")
print(b.hazard_model)
print("body: ")
print(b)
