
from TUNING_UTILS import *

print("testing count_cells")
empty_matrix = [[None] * 5 for i in range(5)]
c = count_cells(empty_matrix)
assert(c == 0)
full_matrix = [[1] * 5 for i in range(5)]
c = count_cells(full_matrix)
assert(c == 25)
semi_matrix = [[1] * 5 for i in range(5)]
semi_matrix[0][0] = None
semi_matrix[2][3] = None
semi_matrix[4][4] = None
c = count_cells(semi_matrix)
assert(c == 22)
print("count_cells passed!")

print("testing more_than_x")
assert(more_than_x(semi_matrix, 0.9) == (22, False))
assert(more_than_x(semi_matrix, 0.8) == (22, True))
assert(more_than_x(full_matrix, 0.9) == (25, True))
print("more_than_x passed")

print("testing gather_trial_data")
matrix = [[1] * 5 for i in range(5)]
threshold = 0.5
colnames_list = ["A", "B", "C","nCells", "D", "E", "moreThan0.5"]
v_d = {}
v_d["A"] = 123
v_d["B"] = 45
v_d["C"] = 3
v_d["D"] = 9
string = gather_trial_data(
            matrix,
            threshold,
            colnames_list,
            v_d
            )
print(string)
assert(string == "123, 45, 3, 25, 9, colname-not-present, True, \n")
print("gather_trial_data passed")

### FILE-FUNCTIONS CANT BE TESTED WITHOUT CHECKING FILES THEY PRODUCE ###
    # too much fs interaction without sys package...
# write_colnames_to_file seems ok
# write trial to file on similar principle
print("testing grid_search")
from experiment_utils import tuning_single_cell_experiment, running_single_cell_experiment
import time
rrange = (0.2, 2)
hrange = (0.2, 2)
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
