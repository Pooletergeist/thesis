#
## Apr 5th.
## Ran: 0.2-2 by 0.2, and hazard 0-0.4 by 0.05 grid searches over resources and hazards
## found: all cells die at hazards upwards of 0.35
## tuning seems pretty good
print("needs to be run from main folder directory, now tucked away for organization")
from TUNING_UTILS import grid_search
from experiment_utils import tuning_single_cell_experiment, running_single_cell_experiment
import time
import pickle

rrange = (0.2, 2) #0.2-2 (27->237 => 709->2466)
hrange = (0.2, 2) #0.2-2 anything 0.4 and up dies
hInc = 0.2
rInc = 0.2
# note hazard 0-4 by 0.05 gives sense for die-off at 0.35

s = time.time()
fname = grid_search(
            SIM_FUNC = tuning_single_cell_experiment,
            RSRC_RANGE = rrange,
            HZRD_RANGE = hrange,
            H_INCREMENT = hInc,
            R_INCREMENT = rInc,
        )
e = time.time()
print("look for new file called: " + fname)
print("that took: ", e-s, " seconds")

# earlier runs: timed pickles and console printing, found no significant 
# speed cost

''' 
rrange = (0.2, 2) #0.2-2 (27->237 => 709->2466)
hrange = (0.2, 2) #0.2-2 anything 0.4 and up dies
hInc = 0.2
rInc = 0.2
printStime = time.time()
fname = grid_search(
            SIM_FUNC = tuning_single_cell_experiment,
            RSRC_RANGE = rrange,
            HZRD_RANGE = hrange,
            H_INCREMENT = hInc,
            R_INCREMENT = rInc,
        )
printEtime = time.time()
print("look for new file called: " + fname)
noprintStime = time.time()
fname = grid_search(
            SIM_FUNC = running_single_cell_experiment,
            RSRC_RANGE = rrange,
            HZRD_RANGE = hrange,
            H_INCREMENT = hInc,
            R_INCREMENT = rInc,
            TITLE_PREFIX = "000"
        )
noprintEtime = time.time()
print("look for new file called: " + fname)
print("no console prints took", noprintEtime-noprintStime)
print("console prints took", printEtime-printStime)
# first timing took 140-seconds for both
# pickle-less timing took 137 seconds. Not much faster
print("both files should have the same contents!")
'''
