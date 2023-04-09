#
## Apr. 8
#

from energy_1cell_tuning import seeded_grid_search

# constants
base_seed = 123
n_seeds = 20
rsrc_range = (0.5, 1.5) 
r_increment = 0.1
hzrd_range = (0.0, 0.4)
h_increment = 0.05

simulation_width = 50
simulation_height = 50
generations = 200
snapshots_per_sim = 2
title_prefix = "first_"
directory = 'energy_results'

# setup cells
from energy_experiment_utils import make_untracked_energy_cells
cell_division_rate = 0.1
cell_move_rate = 0.2

cell_list, clone_id_list, node_list = make_untracked_energy_cells(N=1,
                                                            MUT_RATE = 0.0,
                                                            DIV_RATE = 0.1,
                                                            HAZ_RES = 1,
                                                            MOV_RATE = 0.2,
                                                            NAME = "null")


seeded_grid_search(
                   SEED = base_seed,
                   N_SEEDS = n_seeds,
                   RSRC_RANGE = rsrc_range,
                   R_INCREMENT = r_increment,
                   HZRD_RANGE = hzrd_range,
                   H_INCREMENT = h_increment,
                   CELL_LIST = cell_list,
                   NODE_LIST = node_list,
                   CLONE_ID_LIST = clone_id_list,
                   W = simulation_width, H = simulation_height,
                   GENERATIONS = generations,
                   N_SNAPSHOTS = snapshots_per_sim,
                   TITLE_PREFIX = title_prefix,
                   DIRECTORY = directory
                 )
