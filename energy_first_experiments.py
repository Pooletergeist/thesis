#
## Mar. 18

from energy_experiment_utils import single_cell_experiment

RUNNING = [2]

if 0 in RUNNING:
    # default - empty core, expanding perimiter
    single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=100, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.3, HZRD_AMT=0.5, verbose=True, INIT_RSRC_FCTR=100)

if 1 in RUNNING:
    # dies out
    single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=100, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.3, HZRD_AMT=0.5, verbose=True, INIT_RSRC_FCTR=10)

if 2 in RUNNING:
    # dies out
    single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
        GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=100, MOV_RATE=0.2,
        TIME=False, RSRC_AMT=0.3, HZRD_AMT=0.1, verbose=False, 
        INIT_RSRC_FCTR=20, SEED=789)



