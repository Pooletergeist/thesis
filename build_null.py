#
## Apr. 6: utils for null model, connecting and returning simulation objects
#

## USAGE:
# 1. b = null_model() returns a body
# 2. cs, ns = make_tracked_cells() returns cells and nodes
# 3. place_cells(b, cs, ns) puts cells on body in grid pattern
# 4. calling b.update() many times will run the simulation
# 5. calling color_subtree or count_subtree on n in ns will allow for stats
# 6. importing Visualizer, building v=Visualizer(w,h,b), calling v.display()
        # will let you see visuals

# b = null_model()
# cs, ns = make_tracked_cells(N=9)
# place_cells(b, cs, ns)
# import Visualizer
# v = Visualizer.Visualizer(b.width, b.height, b)
# v.display("test")
# for i in range(200):
#   b.update()
# v.display("post-200")

from Body import Body
from Cell import Cell
from Hazard import Hazard
from Resource import Resource
from Tree import Tree, Node

def null_model(W=50, H=50, RSRC_AMT=0.5, HZRD_AMT=0.2):
    '''returns body object with hazard and resource modules initialized'''
    h = Hazard(W, H, HZRD_AMT)
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h)
    return b

def make_tracked_cells(N=1,
            MUT_RATE=0.0,
            DIV_RATE=0.1,
            HAZ_RES=1,
            MOV_RATE=0.2
            ):
    ''''returns a list of cells with given paramaters, and tree nodes'''
    cells = []
    nodes = []
    for i in range(N):
        c = Cell(
                mutation_rate = MUT_RATE,
                proliferation_rate = DIV_RATE,
                hazard_resistance = HAZ_RES,
                motility_rate = MOV_RATE
                )
        n = Node(parent = None, born_location = (None, None), cell = c)
        cells.append(c)
        nodes.append(n)
        c.set_tree_node(n)

    return cells, nodes
        
import math
def place_cells(body, cells, nodes, frac_of_grid=0.4):
    '''place cells in square, spaced, so they take ~ frac_of_grid'''
    assert(len(cells) == len(nodes))

    n_cells_in_line = math.sqrt(len(cells))
    spacing_intra_line = round((frac_of_grid * body.height) // n_cells_in_line)
    midX = body.width//2
    midY = body.height//2

    initX = midX - round(spacing_intra_line * (n_cells_in_line//2))
    initY = midY - round(spacing_intra_line * (n_cells_in_line//2))

    x = initX
    y = initY
    placed_in_line = 0
    for i in range(len(cells)):
        print("placing: ", x,",",y)
        cell = cells[i]
        # update position
        cell.set_location(x,y)
        # update tree node position
        cell.tree_node.set_born_location((x,y))

        # place
        body.place_cell(cell, x, y)
        placed_in_line += 1
       
        # set-up next spacing
        x += spacing_intra_line
        # new row after n_cells_in_line
        if placed_in_line >= n_cells_in_line:
            x = initX
            y += spacing_intra_line
            placed_in_line = 0
 
        # ensure nodes correspond to cells properly
        assert(cells[i].tree_node == nodes[i]) 
        assert(nodes[i].cell_reference == cells[i])
