#
#
## Apr 12.
#
#
#### V2 - ENERGY BUDGET
# INTERFACE: Cells pickup what they can up to some budget, burn on prolif..
# when resources update, communicate cell's cost to square

import random as rand
import numpy

## munificence scales normal, centred on 10. 
RESOURCE_EXPECTATION = 10

class Resource:
    
    def __init__(self, width, height, munificence=0.05, start=0, body=None):
        # initializes width-many lists of length height: 
        self.grid = [[start]*height for n in range(width)] 
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.munificence = munificence
        self.body = body
        #self.debug = 0
        #self.avgamt = 0
        #self.updated = 0

    def bestow_resources(self, largess):
        '''initializes rsrc at each grid position from pos laplace'''
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y] = numpy.random.normal(loc=RESOURCE_EXPECTATION, 
                                    scale = self.munificence*largess)

    def update_resource_at(self, x, y):
        '''adds resource at (x,y) equal to draw from laplace (possibly <0)'''
        #print(self.munificence, "here")
        amount = numpy.random.laplace(loc=RESOURCE_EXPECTATION,
                                scale = self.munificence)
        new_resource = self.grid[x][y] + amount
        #self.avgamt += amount
        self.grid[x][y] = new_resource
        #self.updated+=1

    def deplete_resource_at(self, x, y, amount):
        '''Removes resources specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_resource_amount(self, x,y):
        '''Reports resource amount at cell (x,y)'''
        #print("x: ", x)
        #print("y: ", y)
        #print(self.grid[x][y])
        return self.grid[x][y]

    def update(self):
        # for each cell, get its energy consumption 
        # and deposit a new energy amount?
#        print(self.get_resource_amount(0,0), " at 0,0")
        #total = 0
        #delta_total = 0
        for x in range(self.width):
            for y in range(self.height):
        #        total += self.get_resource_amount(x,y)
                cell_ate = self.body.get_energy_ate_at(x,y)
                self.deplete_resource_at(x,y, cell_ate)
        #        pre = self.get_resource_amount(x,y)
                self.update_resource_at(x,y)
        #        post = self.get_resource_amount(x,y)
        #        delta = post-pre
        #        delta_total += delta
        #self.debug += delta_total
        #print("---")
        #print(self)
        #print("---")
        #print(self.debug)
        #print(self.avgamt/self.updated, "avg-amt")
        #print("total on grid=", total)
        #print("delta total=", delta_total)

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " "
            string += "\n"
        return string
                


