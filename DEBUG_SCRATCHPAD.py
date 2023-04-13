# Apr. 9:
#
## show when these 9-cells are dying

from UTILS import place_cells

from energy_experiment_utils import (energy_model, make_untracked_energy_cells,
    connect_cells_and_roots)

from Visualizer import Visualizer

W = 50
H = 50
rsrc_amt = 0.5
hzrd_amt = 0.2

sim_state = energy_model(W, H, rsrc_amt, hzrd_amt)
CELL_LIST, CLONE_ID_LIST, NODE_LIST = make_untracked_energy_cells(N=1)
connect_cells_and_roots(CELL_LIST, NODE_LIST)

v = Visualizer(W, H, sim_state)
sim_state.add_visualizer(v)


from energy_experiment_utils import energy_model
b = energy_model(W=50, H=50)
for i in range(200):
    b.update()
