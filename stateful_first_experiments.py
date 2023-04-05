#
## Mar. 18
#

### RESULTS: hazards wind up high, things grow slow if at all, spaced out.


from stateful_experiment_utils import tuning_single_cell_experiment

RUNNING = ["high,mid"] # flags for which experiment(s) to run

## NOTE: rsrc>0.5 to proliferate, hzrd>1 to die. So high,high biases life
## IMG-LEGEND
# a from 0 gens
# b from 100
# c from 200
# d from 200, with first division subtrees colored

## Note: hazard as none is implied by cells having hazard
## resistance of 10, much higher than laplace scaled by 0.5 will likely produce

## low means laplace scaled by 0.3
## mid means laplace scaled by 0.5
## high means laplace scaled by 1
## veryhigh means laplace scaled by 2

## tiny resouces (no division)
if "0.1,none" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=0.1, HZRD_AMT=0.5)

## invulnerable cells, low rsrc
if "low,none" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=0.3, HZRD_AMT=0.5)

## susceptible cells, low rsrc, low hazard
if "low,low" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=0.3, HZRD_AMT=0.3)

# low high dies out

## invulnerable cells, middle resources,
if "mid,none" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5)

## invulnerable cells, high resources,
if "high,none" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=10, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=1, HZRD_AMT=0.5)

## middle resources, low hazards
if "mid,low" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.3)

## susceptible cells, middle rsrc&hazard
if "mid,mid" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=0.5, HZRD_AMT=0.5, verbose=True)

## susceptible cells, middle rsrc&hazard
if "mid,high" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=0.5, HZRD_AMT=1)

## susceptible cells, high rsrc, mid hazard
if "high,mid" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=1, HZRD_AMT=0.5)

## susceptible cells, high rsrc, high hazard
if "high,high" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=1, HZRD_AMT=1)

## susceptible cells, high rsrc, veryhigh hazard
if "high,veryhigh" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=1, HZRD_AMT=2)

## susceptible cells, high rsrc, low hazard
if "high,low" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=1, HZRD_AMT=0.3)

## susceptible cells, high rsrc, low hazard
if "2high,2low" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=2, HZRD_AMT=0.6)

## susceptible cells, high rsrc, low hazard
if "high,low,2" in RUNNING:
    tuning_single_cell_experiment(W=50, H=50, INIT_X=25, INIT_Y=25,
            GENERATIONS=200, MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2,
            TIME=False, RSRC_AMT=1, HZRD_AMT=0.3, DENSITY_RADIUS = 2)


