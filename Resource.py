#
#
## Jan. 30
#
#

import random as rand
import numpy

## Floats over range 0-1
AMOUNT_RANGE = (0,1)

class Resource:
    
    def __init__(self, width, height):
        # initializes width-many lists of length height: 
        self.grid = [[0]*height for n in range(width)] 
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
    
    def create_resources(self):
        '''draws hazard from positive laplace for each grid position'''
        for x in range(self.width):
            for y in range(self.height):
                amount = abs(numpy.random.laplace(loc=0.0, scale = 0.5))
                self.grid[x][y] = amount

    def distribute_few_resources(self, amount, n):
        '''Gives resources specified by "amount" to "n" random grid positions'''
        for i in range(n):
            x = rand.randint(0, self.width-1)
            y = rand.randint(0, self.height-1)
            #print(x,y)
            self.grid[x][y] += amount

    def deplete_resources(self, amount, x, y):
        '''Removes resources specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_resource_amount(self, x,y):
        '''Reports resource amount at cell (x,y)'''
        #print("x: ", x)
        #print("y: ", y)
        return self.grid[x][y]

    def update(self):
        self.create_resources()

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " "
            string += "\n"
        return string
                


