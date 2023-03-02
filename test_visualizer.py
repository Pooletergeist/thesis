#
## Mar. 3
#
#

# why does the third window quitting kill all 3 windows? -> program is done

## Problem: v displays once then done.
    # to update v you have to right code past the mainloop, but 
    # the window closes when you do that.

## Sol1: just create a new object for each display.
## Sol2: have 1 object that creates new windows for each display.
    ## REQUIRES: refactoring such that objects are built during display,
        ## not init

## Sol3: have event loop, in which the outer code can be run? breaks modularity
    # ^ this is why Jim had the grid run the simulation and do display 

from Visualizer import *
from Body import Body

WIDTH = 50
HEIGHT = 50

## display empty 
b = Body(WIDTH, HEIGHT)
print(b.width)
print(b.height)
v = Visualizer(rows = b.width, columns = b.height, body=b)
v.display("display empty (all cells white)", mode="Str")


## display full
for c in range(WIDTH):
    for r in range(HEIGHT):
        b.place_cell("X", c, r)

v.display("intended full (all cells black)", mode="Str")

## display patterned
for c in range(WIDTH):
    for r in range(HEIGHT):
        if (r+c)%3!=0:
            b.remove_cell(c, r)
v.display("(r+c) mod 3 = 0 are black", mode = "Str")
v.display("error", mode = "wrong")
