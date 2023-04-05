#
#
## Mar. 13
#
# supports updating based on getting density from body.

import random as rand
import numpy

## munificence scales laplace. expect float 0->1

class Resource:
    
    def __init__(self, width, height, munificence=0.5, body=None, 
        density_radius=1):
        # initializes width-many lists of length height: 
        self.grid = [[0]*height for n in range(width)] 
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.munificence = munificence
        self.body = body
        self.density_radius=1
    
    def update_resource_at(self, x,y, cell_density):
        '''sets resource at (x,y) equal to draw from positive laplace'''
        amount = abs(numpy.random.laplace(loc=0.0, 
                            scale = self.munificence * (1-cell_density)))
        self.grid[x][y] = amount

    def deplete_resources(self, amount, x, y):
        '''Removes resources specified by "amount" from space on grid (x,y)'''
        self.grid[x][y] -= amount

    def get_resource_amount(self, x,y):
        '''Reports resource amount at cell (x,y)'''
        #print("x: ", x)
        #print("y: ", y)
        return self.grid[x][y]

    def update(self):
        '''updates resource at every position from laplace scaled by 1/'''
        for x in range(self.width):
            for y in range(self.height):
                try:
                    cell_density = self.body.get_density_at(x,y,
                                                            self.density_radius) 
                except:
                    raise ReferenceError( 
        "self.body.get_density_at(x,y) failed to return a cell density. \n"+ 
        "Did you make sure to init Resource with a pointer to your body object?"
                    )
                self.update_resource_at(x, y, cell_density)

    def __repr__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                string += str(round(self.grid[x][y],3)) + " "
            string += "\n"
        return string
                


