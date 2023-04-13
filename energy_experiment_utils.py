#
## Apr. 12: 
#

from Energy_Body import Body
from Energy_Cell import Cell
from Energy_Resource import Resource

from Hazard import Hazard
from Visualizer import Visualizer
from Tree import Tree, Node

import random as rand
import numpy as np
import time
from math import sqrt


def energy_model(W=50, H=50, RSRC_AMT=0.5, HZRD_AMT=0.2, IV=0, 
    INIT_RSRC_FCTR=None):
    '''returns body object with modules initialized'''
    r = Resource(width=W, height=H, munificence=RSRC_AMT, start=IV)
    if INIT_RSRC_FCTR != None:
        r.bestow_resources(INIT_RSRC_FCTR)
    h = Hazard(W, H, HZRD_AMT)
    b = Body(W, H, r, h) 
    ## give RSRC Refs to BODY. Used by RSRC to get cell consumption
    r.body = b
    h.body = b
    return b

def make_untracked_energy_cells(N=1,
            MUT_RATE=0.0,
            DIV_RATE=0.1,
            HAZ_RES=1,
            MOV_RATE=0.2,
            NAME=""):
    ''''returns a list of cells with given paramaters, and tree nodes'''
    cells = []
    nodes = []
    ids = []
    for i in range(N):
        c = Cell(
                mutation_rate = MUT_RATE,
                proliferation_rate = DIV_RATE,
                hazard_resistance = HAZ_RES,
                motility_rate = MOV_RATE
                )
        n = Node(parent = None, born_location = (None, None), cell = None)
        cell_id = (NAME, DIV_RATE, MOV_RATE)

        cells.append(c)
        ids.append(cell_id)
        nodes.append(n)

    return cells, ids, nodes

def connect_cells_and_roots(cell_list, node_list):
    '''in-place connects cells with tree positionally: exchanging references'''
    assert(len(cell_list) == len(node_list))
    for i in range(len(cell_list)):
        # give cell a reference to its tree node
        cell_list[i].set_tree_node(node_list[i])
        # give tree node a reference to its cell
        node_list[i].set_cell_reference(cell_list[i])
        

def single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25, 
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.2, verbose=True, INIT_RSRC_FCTR=100, SEED=124):
    # SEED RNG
    rand.seed(SEED)
    np.random.seed(SEED)

    # SETUP OBJECTS
    r = Resource(W, H, RSRC_AMT)
    r.bestow_resources(INIT_RSRC_FCTR)
    h = Hazard(W, H, HZRD_AMT)
    b = Body(W, H, r, h) 

    ## give RSRC Refs to BODY. Used by RSRC to get cell consumption
    r.body = b
    h.body = b
    v = Visualizer(W,H, b)
    c = Cell(mutation_rate = MUT_RATE,
            proliferation_rate = DIV_RATE,
            hazard_resistance = HAZ_RES,
            motility_rate = MOV_RATE,
            x = INIT_X,
            y = INIT_Y 
            )
    b.place_cell(c, INIT_X, INIT_Y)
    c_node = Node(parent = None, born_location = (INIT_X, INIT_Y), cell = c)
    c.set_tree_node(c_node)

    #v.display("cells: ", mode = "Cell")

    if TIME:
        start = time.time()
    else:
        if verbose:
            v.display("initial resources: ", mode = "Resource")
        v.display("start")

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()
        if i == GENERATIONS//2 and not TIME:
            if verbose:
                v.display("resources after " + str(i) + 
                    " generations: ", mode = "Resource")
                print(r)
            v.display("cells after " + str(i) + " generations")

    if TIME:
        end = time.time()
        print("Sim Time: ", end-start)

    if verbose:
        v.display("resources after " + str(GENERATIONS) + "generations", 
                mode = "Resource")
        print(r)
    v.display("cells after " + str(GENERATIONS) + " generations")
    if TIME:
        vend = time.time()
        print("Display Time: ", vend-end)

    c_node.children[0].color_subtree((200,0,100))
    c_node.children[1].color_subtree((100,0,200))
    print(c_node.children)
    v.display("first-division's subtrees colored")

##########################
### Multi-cell experiments
##########################
def tuning_multi_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25, 
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5, N_CELLS=6):
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H, HZRD_AMT)
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h) # body doesn't know visualizer yet
    v = Visualizer(W,H, b)

    originators = []
    x = INIT_X
    y = INIT_Y
    n_placed = 0
    spacing = 5
    boundary = round(sqrt(N_CELLS))
    for i in range(N_CELLS):
        # make them placed in box on grid* TODO
        x = (x + (n_placed % boundary)*spacing) % W
        y = (y + (n_placed // boundary)*spacing) % H
        print(x, y)
        n_placed += 1
        c = Cell(mutation_rate = MUT_RATE,
                proliferation_rate = DIV_RATE,
                hazard_resistance = HAZ_RES,
                motility_rate = MOV_RATE,
                x = x,
                y = y, 
                )
        b.place_cell(c, x, y)
        c_node = Node(parent = None, born_location = (x, y), cell = c)
        c.set_tree_node(c_node)
        originators.append(c_node)

    #v.display("resources: ", mode = "Resource")
    #v.display("hazards: ", mode = "Hazard")
    #v.display("cells: ", mode = "Cell")

    if TIME:
        start = time.time()
    else:
        v.display("start")

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()
        if i == GENERATIONS//2 and not TIME:
            v.display("after " + str(i) + " generations")

    if TIME:
        end = time.time()
        print("Sim Time: ", end-start)

    v.display("after " + str(GENERATIONS) + " generations")
    if TIME:
        vend = time.time()
        print("Display Time: ", vend-end)

    red = 0
    green = 255
    blue = 255
    for ancestor in originators:
        ancestor.color_subtree((red,green,blue))
        red += 50
        if red > 255:
            red %= 255
            green += 50
        if green > 255:
            green %= 255
            blue += 50
        if blue > 255:
            blue %= 255
            
    v.display("first cells' subtrees colored")


