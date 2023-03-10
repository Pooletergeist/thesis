#
#
## Mar. 9 
#
#
#### V1
# TODO: grid prior and grid post? 
# INTERFACE: communicate cell's cost to resource
#
#### V2 - ENERGY BUDGET
# INTERFACE: Cells pickup what they can up to some budget, burn on prolif..
# when resources update, communicate cell's cost to square

import random as rand
import numpy

## Floats over range 0-1
AMOUNT_RANGE = (0,1) # unused

## munificence scales laplace. expect float 0->1

class Resource:
    
    def __init__(self, width, height, munificence=0.5):
        # initializes width-many lists of length height: 
        self.grid = [[0]*height for n in range(width)] 
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.munificence = munificence
    
    def create_resources(self, cell_density):
        '''draws hazard from positive laplace for each grid position'''
        for x in range(self.width):
            for y in range(self.height):
                amount = abs(numpy.random.laplace(loc=0.0, 
                                scale = self.munificence * (1/cell_density)))
                self.grid[x][y] = amount

    def distribute_few_resources(self, amount, n):
        '''Gives resources specified by "amount" to "n" random grid positions'''
        for i in range(n):
            x = rand.randint(0, self.width-1)
            y = rand.randint(0, self.height-1)
            #print(x,y)
            self.grid[x][y] += amount

    def deplete_resource_at(self, amount, x, y):
        '''Removes resources specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_resource_amount(self, x,y):
        '''Reports resource amount at cell (x,y)'''
        #print("x: ", x)
        #print("y: ", y)
        return self.grid[x][y]

    def update(self, cell_density=1):
        self.create_resources(cell_density)

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " "
            string += "\n"
        return string
                


