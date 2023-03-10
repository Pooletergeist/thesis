#
## Mar 9
from Body import Body
from Cell import Cell
from Hazard import Hazard
from Resource import Resource
from Visualizer import Visualizer
from Tree import Tree, Node

import random as rand
import numpy as np
import time

def single_cell_experiment(W=1000, H=1000, INIT_X=500, INIT_Y=500, 
        GENERATIONS=100, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=1):
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H)
    r = Resource(W, H)
    b = Body(W, H, r, h) # body doesn't know visualizer. unnecessary?
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
    c.set_tree_node(c_node) # necessary for update division tracking

    #v.display("resources: ", mode = "Resource")
    #v.display("hazards: ", mode = "Hazard")
    #v.display("cells: ", mode = "Cell")

    start = time.time()

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()

    end = time.time()

    print("Sim Time: ", end-start)
    v.display("cells")
    vend = time.time()
    print("Display Time: ", vend-end)


def tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25, 
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5):
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H, HZRD_AMT)
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h) # body doesn't know visualizer yet
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

    c_node.children[0].color_subtree((200,0,100))
    c_node.children[1].color_subtree((100,0,200))
    print(c_node.children)
    v.display("first-division's subtrees colored")

##############################
# Calculate Good Window Size #
##############################

def window_size(W=2000, H=2000, INIT_X=500, INIT_Y=500, 
        GENERATIONS=1, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=1):
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H)
    r = Resource(W, H)
    b = Body(W, H, r, h) # body doesn't know visualizer. unnecessary?
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
    c.set_tree_node(c_node) # necessary for update division tracking

    #v.display("resources: ", mode = "Resource")
    #v.display("hazards: ", mode = "Hazard")
    #v.display("cells: ", mode = "Cell")

    start = time.time()

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()

    end = time.time()

    ## Make a line of cells at intervals to calculate window size: Width
    x = 500 # some number in window
    while x < W:
    #    x //= 2 
        for i in range(H//2):
            cprime = Cell(mutation_rate = MUT_RATE,
            proliferation_rate = DIV_RATE,
            hazard_resistance = HAZ_RES,
            motility_rate = MOV_RATE,
            x = x,
            y = i
            )
            b.place_cell(cprime, x, i)
        x += 100

    print("Sim Time: ", end-start)
    v.display("cells", gridlines=False)
    vend = time.time()
    print("Display Time: ", vend-end)


