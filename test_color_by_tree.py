#
## Feb 25.
#

## Make tree of cells, visualize, visualize with color-by-tree

from Visualizer import Visualizer
from Body import Body
from Cells import Cell
from Tree import Node, Tree # do I need tree?

W = 50
H = 50
COLOR1 = (200,0,200)
COLOR2 = (100, 200, 200)

b = Body(W,H)

root = Cell(0,0,0,0,0,0)
b.place_cell(root, 0,0)
print(b)

v = Visualizer(W,H, b)
v.display("just one cell 0,0")

print(root.color)
root_tree_node = Node(parent=None, born_location=(0,0), cell=root)
root_tree_node.color_subtree(COLOR1)
print(root.color)

#print(b.get_cell_color(0,0))

v.display("color changed to " + str(root.color))

c1 = Cell(0,0,0,0,0,1)
b.place_cell(c1, 0,1)
c1_tree_node = Node(parent = root_tree_node, born_location=(0,1), cell = c1)
c2 = Cell(0,0,0,0,1,0)
b.place_cell(c2, 1,0)
c2_tree_node = Node(parent = root_tree_node, born_location = (1,0), cell=c2)
## make root know they're children
root_tree_node.add_child(c1_tree_node)
root_tree_node.add_child(c2_tree_node)
## child of c2
c2_2 = Cell(0,0,0,0,1,1)
b.place_cell(c2_2, 1,1)
c2_2_tree_node = Node(parent = c2_tree_node, born_location = (1,1), cell = c2_2)
## make it known
c2_tree_node.add_child(c2_2_tree_node)

v.display("+ new cells at 01, 10, and 11")
#print(c2.color)
c2_tree_node.color_subtree(COLOR2)
#print(c2.color)
#print(c2_2.color)

v.display("subtree 10 and 11 colored")





