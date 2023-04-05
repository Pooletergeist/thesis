#
#
## Mar. 18
#
#
#### V1
# TODO: grid prior and grid post? 
# INTERFACE: communicate cell's cost to hazard
#
#### V2 - ENERGY BUDGET
# INTERFACE: Cells pickup what they can up to some budget, burn on prolif..
# when hazards update, communicate cell's cost to square

import random as rand
import numpy

## Floats over range 0-1
## peril scales laplace. expect float 0->1

class Hazard:
    
    def __init__(self, width, height, peril=0.5, body=None):
        # initializes width-many lists of length height: 
        self.grid = [[0]*height for n in range(width)] 
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.peril = peril
        self.body = body

    def update_hazard_at(self, x, y):
        '''adds hazard at (x,y) equal to draw from laplace (possibly <0)'''
        amount = numpy.random.laplace(loc=0.0,
                                scale = self.peril)
        new_hazard = self.grid[x][y] + amount
        if new_hazard < 0: # make sure no negatives
            new_hazard = 0
        elif new_hazard > 2.5: # max? arbitrary
            new_hazard = 2.5
        self.grid[x][y] = new_hazard

    def deplete_hazard_at(self, x, y, amount):
        '''Removes hazards specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_hazard_amount(self, x,y):
        '''Reports hazard amount at cell (x,y)'''
        #print("x: ", x)
        #print("y: ", y)
        return self.grid[x][y]

    def update(self):
        # for each cell, get its energy consumption 
        # and deposit a new energy amount?
        for x in range(self.width):
            for y in range(self.height):
                cell_tanked = self.body.get_hazard_resistance_at(x,y)
                self.deplete_hazard_at(x,y, cell_tanked)
                self.update_hazard_at(x,y)

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " "
            string += "\n"
        return string
                


