#
## Apr 5

from Body import Body
from Cell import Cell
from Hazard import Hazard
from Resource import Resource
from Visualizer import Visualizer
from Tree import Tree, Node

import random as rand
import numpy as np
import time
from math import sqrt

def single_cell_experiment(W=1000, H=1000, INIT_X=500, INIT_Y=500, 
        GENERATIONS=100, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=1,
        VISUALIZE=True):
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

    if VISUALIZE:
        print("Sim Time: ", end-start)
        v.display("cells")
        vend = time.time()
        print("Display Time: ", vend-end)

    return b # for stats on grid

def tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25, 
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5, VISUALIZE=True):
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H, HZRD_AMT)
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h) # body doesn't know visualizer yet
    ### give HZRD/RSRC Refs to BODY. Used by density systems
    #h.body = b
    #r.body = b
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
        if VISUALIZE:
            v.display("start")

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()
        if i == GENERATIONS//2 and not TIME and VISUALIZE:
            v.display("after " + str(i) + " generations")

    if TIME:
        end = time.time()
        print("Sim Time: ", end-start)

    if VISUALIZE:
        v.display("after " + str(GENERATIONS) + " generations")
    if TIME:
        vend = time.time()
        print("Display Time: ", vend-end)

    if VISUALIZE:
        c_node.children[0].color_subtree((200,0,100))
        c_node.children[1].color_subtree((100,0,200))
        print(c_node.children, "exp-util")
        v.display("first-division's subtrees colored")

    return b # for stats on result grid

def running_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25, 
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
        RSRC_AMT=0.5, HZRD_AMT=0.5, VISUALIZE=None):
        # nice TODO: add debug for this
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H, HZRD_AMT)
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h) # body doesn't know visualizer yet
    ### give HZRD/RSRC Refs to BODY. Used by density systems
    #h.body = b
    #r.body = b
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

    for i in range(GENERATIONS):
        b.update(hint=False) # make body not write to console

    return b # for stats on result grid


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

##############
### Helper ###
##############


def almost_cbrt(x):
    '''rtrns smallest integer such that integer^3 < x'''
    guess = 1
    while guess ** 3 < x:
        guess += 1
    return guess

def color_subtrees(cell_list, debug=False):
    '''given a list of cell nodes to color, assign different rgb's sensibly'''
    # how-to break/sanitize this?
    n_cells = len(cell_list)
    gap = 150 // almost_cbrt(n_cells)
    red = 50
    blue = 50
    green = 50
    # color with colors
    for cell_node in cell_list:
        if debug:
            print(red,blue,green, "exp-util coloring_subtrees")
        cell_node.color_subtree((red,blue,green))
        red += gap
        if green >= 200:
            raise Exception("green too high")
        if blue >= 200 and red >= 200:
            green += gap
            red = 50
            blue = 50
        elif red >= 200:
            blue += gap
            red = 50

def uncolor_subtrees(cells):
    '''turns cells and descendants black'''
    for cell in cells:
        cell.color_subtree(0,0,0)

def count_living_subtrees(cell_node_list):
    '''given a list of cell nodes, return list of counts of still-live cells'''
    counts = [0] * len(cell_node_list)
    i = 0
    for cell_node in cell_node_list:
        counts[i] = cell_node.count_living_subtree()
        i += 1 
    return counts
        
def tuning_multi_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25, 
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5, N_CELLS=6, VISUALIZE=True):
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H, HZRD_AMT)
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h) # body doesn't know visualizer yet
    v = Visualizer(W,H, b)

    originators = []
    ## supposing we want grid to take up 1/5 of width,
    boundary = round(sqrt(N_CELLS))
    gap = round((1/5) * (W/boundary))
    x = INIT_X
    y = INIT_Y
    n_placed_in_row = 0
    for cell_n in range(N_CELLS):
        c = Cell(mutation_rate = MUT_RATE,
                proliferation_rate = DIV_RATE,
                hazard_resistance = HAZ_RES,
                motility_rate = MOV_RATE,
                x = x,
                y = y, 
                )
        b.place_cell(c, x, y)
        n_placed_in_row += 1
        c_node = Node(parent = None, born_location = (x, y), cell = c)
        c.set_tree_node(c_node)
        originators.append(c_node)
        # next position
        x += gap
        if n_placed_in_row >= boundary:
            x = INIT_X
            y += gap
            n_placed_in_row = 0
        
    if VISUALIZE:
        color_subtrees(originators,debug)

    #v.display("resources: ", mode = "Resource")
    #v.display("hazards: ", mode = "Hazard")
    #v.display("cells: ", mode = "Cell")

    if TIME:
        start = time.time()
    elif VISUALIZE:
        v.display("start")

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()
        if i == GENERATIONS//2 and not TIME and VISUALIZE:
            color_subtrees(originators,debug)
            v.display("after " + str(i) + " generations")

    if TIME:
        end = time.time()
        print("Sim Time: ", end-start)

    if VISUALIZE:
        color_subtrees(originators,debug)
        v.display("after " + str(GENERATIONS) + " generations")
    if TIME:
        vend = time.time()
        print("Display Time: ", vend-end)

    if VISUALIZE:
        v.display("first cells' subtrees colored")

    return b # for stats & analysis

def generic_multi_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25, 
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5, CELL_LIST=[],
        VISUALIZE=True, debug=False):
    if CELL_LIST == []:
        raise Exception("you need to supply cells for this one") 
    # SEED RNG
    rand.seed(123)
    np.random.seed(123)
    # SETUP OBJECTS
    h = Hazard(W, H, HZRD_AMT)
    r = Resource(W, H, RSRC_AMT)
    b = Body(W, H, r, h) # body doesn't know visualizer yet
    v = Visualizer(W,H, b)

    originators = []
    ## supposing we want grid to take up 1/5 of width,
    boundary = round(sqrt(len(CELL_LIST)))
    gap = round((1/5) * (W/boundary))
    x = INIT_X
    y = INIT_Y
    n_placed_in_row = 0
    for c in CELL_LIST:
        # set its position
        c.set_location(x,y)
        b.place_cell(c, x, y)
        n_placed_in_row += 1
        c_node = Node(parent = None, born_location = (x, y), cell = c)
        c.set_tree_node(c_node)
        originators.append(c_node)
        # next position
        x += gap
        if n_placed_in_row >= boundary:
            x = INIT_X
            y += gap
            n_placed_in_row = 0
        
    if VISUALIZE:
        color_subtrees(originators,debug)

    #v.display("resources: ", mode = "Resource")
    #v.display("hazards: ", mode = "Hazard")
    #v.display("cells: ", mode = "Cell")

    if TIME:
        start = time.time()
    elif VISUALIZE:
        v.display("start")

    if debug:
        for originator in originators:
            print(originator.check_living_children())

    for i in range(GENERATIONS):
        print("GENERATION: ", i)
        b.update()

        if debug:
            breaking=False
            for originator in originators:
                print(originator.check_living_children())
            for originator in originators:
                if not originator.check_living_children():
                    v.display("1 clone died out")
                    breaking = True
            if breaking:
                break

        if i == GENERATIONS//2 and not TIME and VISUALIZE:
            if debug:
                color_subtrees(originators, debug)
            v.display("after " + str(i) + " generations")


    if not debug or not breaking:
        if TIME:
            end = time.time()
            print("Sim Time: ", end-start)

        if VISUALIZE:
            if debug:
                color_subtrees(originators, debug)
            v.display("after " + str(GENERATIONS) + " generations")
        if TIME:
            vend = time.time()
            print("Display Time: ", vend-end)

        if VISUALIZE:
            color_subtrees(originators, debug)
            v.display("first cells' subtrees colored")

    return b, originators # for stats & analysis


