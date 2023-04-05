#
## Mar 18

from Body import Body
from Cell import Cell
from Stateful_Hazard import Hazard
from Stateful_Resource import Resource
from Visualizer import Visualizer
from Tree import Tree, Node

import random as rand
import numpy as np
import time
from math import sqrt

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
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5, verbose=False):
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H, HZRD_AMT) 
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h) # body doesn't know visualizer yet
    ## give HZRD/RSRC Refs to BODY. Used by RSRC to get cell consumption
    h.body = b
    r.body = b
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
        v.display("start")

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()
        if i == GENERATIONS//2 and not TIME:
            if verbose:
                v.display("resources: ", mode = "Resource")
                print(r)
                v.display("hazards: ", mode = "Hazard")
                print(h)
            v.display("after " + str(i) + " generations")

    if TIME:
        end = time.time()
        print("Sim Time: ", end-start)

    if verbose:
        v.display("resources: ", mode = "Resource")
        v.display("hazards: ", mode = "Hazard")
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


