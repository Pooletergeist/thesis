# Apr. 7 - tested it works!

# 200-gen grid search took 257 seconds
# expect 20 seeds to take 86 minutes

'''
## Test: 
# write_pop_counts to file


### HOW DO YOU IMPOSE A RELATIONSHIP BETWEEN THE COLNAMES YOU PROVIDE
### AND THE DATA YOU RECORD, WHEN THE DATA REQUIRES CODE TO GET IT?
### DO YOU JUST NOT HAVE COLNAMES AS ARGUMENT?

## introduce indirection in a dictionary to give an equality check 
## for indices. but that's so much complexity.
# it would need a dictionary being recorded in simulation...

## tag each value with a title, as a list of tuples, and call a function
## doing comparisons and putting them in order
'''


import time

from energy_sim_tuning import *
from Visualizer import Visualizer # for test
from UTILS import *
print(CELL_LIST)
print(NODE_LIST)
print(CLONE_ID_LIST)

W=50
H=50
r = 1.5
h = 0.2
seed = 123 

import random as rand
import numpy as np
rand.seed(seed)
np.random.seed(seed)

rRange = (0.5, 1.5)
rInc = 0.1
hRange = (0.0, 0.4)
hInc = 0.05
gens = 200

n_seeds=20

drcty = 'energy_results'
fname = 'atest.csv'

testing = [2] # 0-3 init, simulation, grid_search, seed_wrap respectively

#init
if 0 in testing:
    print("testing init")
    connect_cells_and_roots(CELL_LIST, NODE_LIST)
    m = energy_model(W, H, r, h)
    place_cells(m, CELL_LIST, NODE_LIST)
    v = Visualizer(W, H, m)
    v.display("start")

# simulation itself

if 1 in testing:
    print("testing Sim")
    connect_cells_and_roots(CELL_LIST, NODE_LIST)
    COLNAMES = ["clone", "livePop", "historicPop", "divRt", "movRt",
                "rA", "hA", "generations", "seed", "nInitCell", "w", "h"]
    write_colnames_to_file(fname, COLNAMES, drcty)
    m = run_and_record_simulation(W=W, H=H, rsrc_amt = r, hzrd_amt = h,
        seed = seed, nInitCell = 1, 
        CELL_LIST=CELL_LIST, NODE_LIST = NODE_LIST, 
        CLONE_ID_LIST = CLONE_ID_LIST, GENERATIONS = 200, N_SNAPSHOTS = 2, 
        fname = fname, DIRECTORY = drcty, pickle_title="delete",
        VISUALIZE=True)

if 2 in testing:
    print("testing grid search")
    # reset make sure cells/nodes separate
    cs, ids, ns = make_untracked_energy_cells(N=1, NAME="null")
    COLNAMES = ["clone", "livePop", "historicPop", "divRt", "movRt",
                "rA", "hA", "generations", "seed", "nInitCell", "w", "h"]
    write_colnames_to_file(fname, COLNAMES, drcty)
    # grid search wrapper
    start = time.time()
    grid_search(SEED=seed, fname=fname,
                   RSRC_RANGE = rRange,
                   R_INCREMENT = rInc,
                   HZRD_RANGE = hRange,
                   H_INCREMENT = hInc,
                   CELL_LIST = cs,
                   NODE_LIST = ns, # passed
                   CLONE_ID_LIST = CLONE_ID_LIST, # passed
                   nInitCell = len(CELL_LIST),
                   W=W, H=H,
                   GENERATIONS=gens,
                   N_SNAPSHOTS = 2,
                   TITLE_PREFIX = 'delete', DIRECTORY=drcty,
                   VISUALIZE=False)
    end = time.time()
    print("grid search took", end-start)

if 3 in testing:
    print("testing seed wrapper")
    cs, ids, ns = make_untracked_energy_cells(N=1, NAME="null")
    start = time.time()
    seeded_grid_search(
                        SEED=seed,
                        N_SEEDS=n_seeds,
                        RSRC_RANGE=rRange,
                        R_INCREMENT=rInc,
                        HZRD_RANGE=hRange,
                       H_INCREMENT=hInc,
                       CELL_LIST=cs,
                       NODE_LIST=ns,
                       CLONE_ID_LIST=CLONE_ID_LIST,
                       W=W, H=H,
                       GENERATIONS=gens//n_seeds,
                       N_SNAPSHOTS=2,
                       TITLE_PREFIX='delete', # used here, and later
                       DIRECTORY=drcty,
                       VISUALIZE=False
                    )
    end = time.time()
    print("wrapped seed took", end-start)
