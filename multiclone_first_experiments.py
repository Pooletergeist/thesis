#
## Mar. 25
#
## does this only make sense with the resource model?

from Cell import Cell

from experiment_utils import tuning_multi_cell_experiment, generic_multi_cell_experiment

RUNNING = [3] # flags for which experiment(s) to run

if 0 in RUNNING: # control
    tuning_multi_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5, N_CELLS=2, VISUALIZE=True)

if 1 in RUNNING: # 2 cells same phenotype
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

    b = generic_multi_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
        GENERATIONS=200, TIME=False, RSRC_AMT=1, HZRD_AMT=0.2, 
        CELL_LIST=cells, VISUALIZE=True, debug=False)

    # with 0.5, 0.5, generation 3 one dies out but still there?
        # number 1 divided but number 0 died, so why still 1 of each color?
        # dead cells not removed from list
    # with bug, 1, 0.2 makes good picture
    # fixd, 0.5,0.5 dies

    # but 1,0.2 makes great picture!


if 2 in RUNNING: # 2 cells. clone1 double proliferation rate
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
                proliferation_rate = 0.2,
                hazard_resistance = 1,
                motility_rate = 0.2,
                x = None,
                y = None,
            )
    cells = [cell_0, cell_1]

    b = generic_multi_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
        GENERATIONS=200, TIME=False, RSRC_AMT=1, HZRD_AMT=0.2, 
        CELL_LIST=cells, VISUALIZE=True, debug=False)


if 3 in RUNNING: # 2 cells. same proliferation rate, lower rsrc.
    # 1 clone dominates by chance!
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

    b = generic_multi_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
        GENERATIONS=200, TIME=False, RSRC_AMT=0.8, HZRD_AMT=0.2, 
        CELL_LIST=cells, VISUALIZE=True, debug=False)

