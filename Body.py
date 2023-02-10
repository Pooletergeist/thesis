#
#
## Feb. 9
#
#
import random as rand

COST_OF_LIVING = 0.1
PROLIFERATIVE_COST = 0.5
    
class Body:

    def __init__(self, width, height, resource=None, hazard=None):
        # initializes width-many lists of length height: 
        self.grid = [[None]*height for n in range(width)]
        # grid[i][j], i is width, j is height
        self.width = width
        self.height = height
        self.live_cells = []

        # should these be objects?
        self.resource_model = resource
        self.hazard_model = hazard

    ### UPDATE ####
    def update(self):
        self.update_resources()
        self.update_hazards()
        self.update_cells()
        
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

            if dest != None:
                # Move the cell
                self.move_cell(x,y, dest[0], dest[1]) 
                # Update cell's position
                cell.set_location(dest[0], dest[1])

            if daughter_tuple != (None,None):
                # Place the daughter
                print(daughter_tuple)
                self.place_cell(daughter_tuple[0],
                                daughter_tuple[1][0],
                                daughter_tuple[1][1])
                # consume resources 
                self.resource_model.deplete_resources(PROLIFERATIVE_COST,
                                                        x,
                                                        y)
            if dead != False:
                pass # for now
                        
            # reduce hazards?

    ### MOVEMENT HELPERS ###
    def place_cell(self, cell, x, y):
        '''puts cell at gridspace (x,y)'''
        self.grid[x][y] = cell
        self.live_cells.append(cell)

    def remove_cell(self, x,y):
        '''removes cell from gridspace (x,y)'''
        self.grid[x][y] = None

    def move_cell(self, x1, y1, x2, y2):
        self.place_cell(self.grid[x1][y1], x2, y2)
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
