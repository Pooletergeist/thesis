#
#
## Mar. 18
#
## differs in that body doesn't call deplete resource after proliferation
## instead, cells track that inside their energy budget.
## resource depletion happens when cells eat to increase their energy budget
#
import random as rand
from Visualizer import Visualizer

MAX_ENERGY = 5 # used by energy sim
    
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
    def update(self, visualize=False, verbose=False, hint=True):
        self.update_resources(verbose)
        if verbose or hint:
            print("r-done")
        self.update_hazards(verbose)
        if verbose or hint:
            print("h-done")
        self.update_cells(verbose)
        if verbose or hint:
            print("c-done")
        if visualize:
            # messy
            v = Visualizer(self.width, self.height, self)
            v.display()
        
    def update_resources(self, verbose):
        if self.resource_model != None:
            self.resource_model.update()

    def update_hazards(self, verbose):
        if self.hazard_model != None:
            self.hazard_model.update()

    def update_cells(self, verbose):
        rand.shuffle(self.live_cells) # this better be in-place under the hood
        if verbose:
            print(self.live_cells)
        for cell in self.live_cells:
            if verbose:
                print(cell)
            x,y = cell.get_location()
            dest, daughter_tuple, dead = cell.update(
                    space = self.adjacent_spaces(x,y), 
                    resources = self.resource_model.get_resource_amount(x,y),
                    hazards = self.hazard_model.get_hazard_amount(x,y), 
                    verbose = verbose)
            if verbose:
                print("done cell update")
                print(self.live_cells)

            if dest != None:
                if verbose:
                    print('body -> moving')
                # Move the cell
                self.move_cell(x,y, dest[0], dest[1]) 
                # Update cell's position
                cell.set_location(dest[0], dest[1])

            if daughter_tuple != (None,None):
                if verbose:
                    print('birthing')
                # Place the daughter
                if verbose:
                    print(daughter_tuple)
                self.place_cell(daughter_tuple[0],
                                daughter_tuple[1][0],
                                daughter_tuple[1][1])
                if verbose:
                    print("placed daughter. Alive: " + str(self.live_cells))
            if dead != False:
                self.remove_cell(x,y) # remove from grid
                self.live_cells.remove(cell) # remove from live_cells list
                        

    ### DENSITY HELPER ###
    ## for Density-Based Resource & Hazard Modules
    def get_density_at(self, x, y, density_radius):
        '''returns 0-1 density around space (x,y)'''
        num_neighbors = 0
        for x_prime in range(x-density_radius, x+density_radius):
            for y_prime in range(y-density_radius, y+density_radius):
                if not self.is_empty(x_prime, y_prime):
                    num_neighbors += 1
        return num_neighbors / ((2*density_radius + 1) * (2*density_radius+1))

    ### CONSUMPTION HELPER ###
    ## for stateful resource & hazard modules
    def get_consumption_at(self, x, y):
        '''returns cell consumption or 0'''
        if self.grid[x][y] is not None:
            return self.grid[x][y].consumption 
        return 0

    def get_hazard_resistance_at(self, x, y):
        '''returns cell hazard tolerance or 0'''
        if self.grid[x][y] is not None:
            return self.grid[x][y].hazard_resistance
        return 0

    ## for energy simulation 
    def get_energy_ate_at(self, x, y):
        if self.grid[x][y] is not None:
            return MAX_ENERGY - self.grid[x][y].energy_budget
        return 0
            
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
        if x < 0 or x >= self.width or y < 0 or y >= self.width:
            return False
        elif self.grid[x][y] == None:
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
    def get_cell_color(self, x,y, mode):
        color = (255,255,255) # default empty to rgb white.
        if mode == "Cell":
            if not self.is_empty(x,y):
                color = self.grid[x][y].color
        elif mode == "Str":
            if not self.is_empty(x,y):
                color = (5,5,5)
        elif mode == "Resource":
            ## black is MAX_ENERGY. 
            if self.resource_model != None:
                saturation = self.resource_model.get_resource_amount(x,y)/MAX_ENERGY
                if saturation > 1: 
                    saturation = 1
                nmbr = round((1-saturation) * 255)
                #print(nmbr)
                color = (nmbr, nmbr, nmbr)
        elif mode == "Hazard":
            if self.hazard_model != None:
                saturation = self.hazard_model.get_resource_amount(x,y)/MAX_ENERGY
                if saturation > 1:
                    saturation = 1
                nmbr = round((1-saturation) * 255)
                color = (nmbr, nmbr, nmbr)
        else:
            raise Exception("get_cell_color called with bad mode: " + mode + 
                " \n => check the mode passed in call to visualizer.display?")
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
