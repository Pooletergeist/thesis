#
#
## Feb. 3 (copy of Resource.py)
#
#
## Mar 2: must export a "get_hazard_amount" for visualizing

import random as rand
import numpy # for laplace

## peril scales laplace. expect float 0->1

class Hazard:

    def __init__(self, width, height, peril=0.5, body=None, density_radius=1):
        # initializes width-many lists of length height: 
        self.grid = [[0]*height for n in range(width)]
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.peril = peril
        self.body = body
        self.density_radius = density_radius

    def update_hazard_at(self, x, y, cell_density):
        '''draws hazard from positive laplace for each grid position'''
        amount = abs(numpy.random.laplace(loc=0.0, 
                                scale = self.peril * (1-cell_density)))
        self.grid[x][y] = amount

    def deplete_hazards(self, amount, x, y):
        '''Removes hazards specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_hazard_amount(self, x,y):
        '''Reports hazard amount at cell (x,y)'''
        return self.grid[x][y]

    def update(self):
        for x in range(self.width):
            for y in range(self.height):
                try:
                    cell_density = self.body.get_density_at(x,y,
                                                            self.density_radius)
                except:
                    raise ReferenceError(
        "self.body.get_density_at(x,y) failed to return a cell density. \n"+
        "make sure to init Hazard with a pointer to your body object"
                    )
                self.update_hazard_at(x,y, cell_density)

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " " 
            string += "\n"
        return string
