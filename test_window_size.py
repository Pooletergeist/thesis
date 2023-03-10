#
## Mar 9.
## GOAL: find maximum visual window size on my machine:
### RESULTS:
## minsize=4 => 435x263 WxH grid.
## misize=1 => 1700x1000 WxH grid.

from experiment_utils import window_size 

window_size(W=1700, H=1000, INIT_X=50, INIT_Y=50,
    GENERATIONS=0, MUT_RATE=0, DIV_RATE=1, HAZ_RES=10, MOV_RATE=0)
