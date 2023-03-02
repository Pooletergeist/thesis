#
#
## Feb. 9
#
#
import random as rand
from Visualizer import Visualizer

COST_OF_LIVING = 0.1
PROLIFERATIVE_COST = 0.5
    
class Body:

    def __init__(self, width, height, resource=None, hazard=None, vis=None):
        # initializes width-many lists of length height: 
        self.grid = [[None]*height for n in range(width)]
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.live_cells = []

        # should these be objects?
        self.resource_model = resource
        self.hazard_model = hazard
        self.visualizer = vis # UNUSED

    ### UPDATE ####
    def update(self, visualize=False):
        self.update_resources()
        print("r-done")
        self.update_hazards()
        print("h-done")
        self.update_cells()
        print("c-done")
        if visualize:
            v = Visualizer(self.width, self.height, self)
        
    def update_resources(self):
        if self.resource_model != None:
            self.resource_model.update()

    def update_hazards(self):
        if self.hazard_model != None:
            self.hazard_model.update()

    def update_cells(self):
        rand.shuffle(self.live_cells) # this better be in-place under the hood
        print(self.live_cells)
        for cell in self.live_cells:
            print(cell)
            x,y = cell.get_location()
            dest, daughter_tuple, dead = cell.update(
                    space = self.adjacent_spaces(x,y), 
                    resources = self.resource_model.get_resource_amount(x,y),
                    hazards = self.hazard_model.get_hazard_amount(x,y))
            print("done cell update")
            print(self.live_cells)

            if dest != None:
                print('moving')
                # Move the cell
                self.move_cell(x,y, dest[0], dest[1]) 
                # Update cell's position
                cell.set_location(dest[0], dest[1])

            if daughter_tuple != (None,None):
                print('birthing')
                # Place the daughter
                print(daughter_tuple)
                self.place_cell(daughter_tuple[0],
                                daughter_tuple[1][0],
                                daughter_tuple[1][1])
                print("placed daughter. Alive: " + str(self.live_cells))
                # consume resources 
                self.resource_model.deplete_resources(PROLIFERATIVE_COST,
                                                        x,
                                                        y)
            if dead != False:
                self.remove_cell(x,y)
                pass # for now
                        
            # reduce hazards?

    ### MOVEMENT HELPERS ###
    def place_cell(self, cell, x, y):
        '''puts cell at gridspace (x,y) AND adds to live_cells'''
        self.grid[x][y] = cell
        self.live_cells.append(cell)

    def remove_cell(self, x,y):
        '''removes cell from gridspace (x,y)'''
        self.grid[x][y] = None

    def move_cell(self, x1, y1, x2, y2):
        self.grid[x2][y2] = self.grid[x1][y1]
        # self.place_cell(self.grid[x1][y1], x2, y2) vicious bug here
        self.remove_cell(x1,y1)

    ### SPACE SELECTION ###
    def is_empty(self, x, y):
        '''returns bool indicating whether space (x,y) is empty'''
        if self.grid[x][y] == None:
            return True
        return False

    def adjacent_spaces(self, x, y):
        '''returns list of up to 8 adjacent spaces'''
        empty = []

        if x > 0:
            ### left side
            if y > 0 and self.is_empty(x-1, y-1):
                empty.append((x-1,y-1))

            if self.is_empty(x-1, y):
                empty.append((x-1,y))

            if y < self.height-1 and self.is_empty(x-1, y+1):
                empty.append((x-1,y+1))

        if x < self.width-1:
            ### right side
            if y > 0 and self.is_empty(x+1, y-1):
                empty.append((x+1, y-1))

            if self.is_empty(x+1, y):
                empty.append((x+1, y))

            if y < self.height-1 and self.is_empty(x+1, y+1):
                empty.append((x+1, y+1))

            ## top and bot mid.
        if y > 0 and self.is_empty(x,y-1):
            empty.append((x, y-1))
        
        if y < self.height-1 and self.is_empty(x,y+1):
            empty.append((x, y+1))

        return empty


    ### DISPLAY ###
    def get_cell_color(self, x,y):
        color = (255,255,255) # default empty to rgb white.
        if not self.is_empty(x,y):
            color = self.grid[x][y].color
        return color
         

    def __repr__(self):
        string = ""
        for y in range(self.height):
            string += "\n"
            for x in range(self.width):
                if not self.is_empty(x,y):
                    string += "x "
                else:
                    string += "o "
        return string
