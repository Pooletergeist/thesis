#
#
## Feb. 3 (copy of Resource.py)
#
#
## Mar 2: must export a "get_hazard_amount" for visualizing

import random as rand
import numpy # for laplace

class Hazard:

    def __init__(self, width, height):
        # initializes width-many lists of length height: 
        self.grid = [[0]*height for n in range(width)]
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height

    def create_hazards(self):
        '''draws hazard from positive laplace for each grid position'''
        for x in range(self.width):
            for y in range(self.height): 
                amount = abs(numpy.random.laplace(loc=0.0, scale = 0.5))
                self.grid[x][y] = amount

    def deplete_hazards(self, amount, x, y):
        '''Removes hazards specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_hazard_amount(self, x,y):
        '''Reports hazard amount at cell (x,y)'''
        return self.grid[x][y]

    def update(self):
        self.create_hazards()

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " " 
            string += "\n"
        return string
