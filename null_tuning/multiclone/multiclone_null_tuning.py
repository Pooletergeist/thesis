#
## Apr 6.
#

# run and record null model with multiple starting cells
# when phenotypes are identical and when they're not.

from TUNING_UTILS import multicell_grid_search
from experiment_utils import generic_multi_cell_experiment
from Cell import Cell

RUNNING = [0]

if 0 in RUNNING: # two 0.1-div, 0.2-mov dividers
    rsrc_range = (0.2, 1.0)
    r_increment = 0.1
    hzrd_range = (0.0, 0.4)
    h_increment = 0.05
    
    # build cells
    cell_0 = Cell(
                mutation_rate = 0,
                proliferation_rate = 0.1,
                hazard_resistance = 1,
                motility_rate = 0.2,
                x = None,
                y = None,
            )

    cell_1 = Cell(
                mutation_rate = 0,
                proliferation_rate = 0.1,
                hazard_resistance = 1,
                motility_rate = 0.2,
                x = None,
                y = None,
            )
    cells = [cell_0, cell_1]

    # run sim

    fname = multicell_grid_search(
        SIM_FUNC = generic_multi_cell_experiment,
        CELL_LIST = cells,
        RSRC_RANGE = rsrc_range,
        HZRD_RANGE = hzrd_range,
        R_INCREMENT = r_increment,
        H_INCREMENT = h_increment,
        TITLE_PREFIX = "",
        DIRECTORY = "null_tuning/multiclone"
    )
        
