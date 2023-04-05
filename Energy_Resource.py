#
#
## Mar. 18
#
#
#### V2 - ENERGY BUDGET
# INTERFACE: Cells pickup what they can up to some budget, burn on prolif..
# when resources update, communicate cell's cost to square

import random as rand
import numpy

## Floats over range 0-1
## munificence scales laplace. expect float 0->1

class Resource:
    
    def __init__(self, width, height, munificence=0.05, body=None):
        # initializes width-many lists of length height: 
        self.grid = [[0]*height for n in range(width)] 
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.munificence = munificence
        self.body = body

    def bestow_resources(self, largess):
        '''initializes rsrc at each grid position from pos laplace'''
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y] = numpy.random.laplace(loc=0.0, 
                                    scale = self.munificence*largess)

    def update_resource_at(self, x, y):
        '''adds resource at (x,y) equal to draw from laplace (possibly <0)'''
        amount = numpy.random.laplace(loc=0.0,
                                scale = self.munificence)
        new_resource = self.grid[x][y] + amount
        if new_resource < 0: # make sure no negatives
            new_resource = 0
        elif new_resource > 10: # max at 5 divisions?
            new_resource = 10 
        self.grid[x][y] = new_resource

    def deplete_resource_at(self, x, y, amount):
        '''Removes resources specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_resource_amount(self, x,y):
        '''Reports resource amount at cell (x,y)'''
        #print("x: ", x)
        #print("y: ", y)
        return self.grid[x][y]

    def update(self):
        # for each cell, get its energy consumption 
        # and deposit a new energy amount?
        for x in range(self.width):
            for y in range(self.height):
                cell_ate = self.body.get_energy_ate_at(x,y)
                self.deplete_resource_at(x,y, cell_ate)
                self.update_resource_at(x,y)

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " "
            string += "\n"
        return string
                


