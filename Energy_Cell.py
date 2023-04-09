#
#
## Mar. 18: give cells budget
#
#

import random as rand

MAX_ENERGY = 5 # make sure this is consistent with Body's number!!
BASE_CONSUMPTION = 0.1
PROLIFERATION_COST = BASE_CONSUMPTION * 10

class Cell:
    '''basic cell class, able to move grow and die'''

    def __init__(self, mutation_rate, 
                    proliferation_rate, 
                    hazard_resistance, 
                    motility_rate, 
                    x=None, 
                    y=None, 
                    t=None,
                    energy = PROLIFERATION_COST):
        self.energy_budget = energy 
        self.mutation_rate = mutation_rate
        self.proliferation_rate = proliferation_rate
        self.hazard_resistance = hazard_resistance
        self.motility_rate = motility_rate
        self.x = x
        self.y = y
        self.tree_node = t
        self.dead = False
        self.color = (0,0,0) # default cells to black rgb

    def __deepcopy__(self, memo):
        '''fresh cell object with same fields, except tree_node=None'''
        new = Cell(self.mutation_rate,
                self.proliferation_rate,
                self.hazard_resistance,
                self.motility_rate,
                self.x,
                self.y,
                None, 
                self.energy_budget)
        self.dead = self.dead
        self.color = self.color
        return new
        

    def update(self, space, resources, hazards, verbose=False):
        destination = None # would samelocation be fewer checks?
        daughter = None
        daughter_location = None
        # TODO: Mutate?
        if hazards > self.hazard_resistance or self.energy_budget < 0:
            if verbose:
                print("DEAD:")
                print("energy: ", self.energy_budget)
                print("hazards: ", hazards)
            if verbose:
                print(self.energy_budget, 'dead')
            # Die
            self.dead = True
            if self.tree_node != None:
                self.tree_node.track_death((self.x,self.y))
        else:
            # pickup energy from space
            vacuum = MAX_ENERGY - self.energy_budget
            self.energy_budget += min(vacuum, resources)
            # pay cost of living
            self.energy_budget -= BASE_CONSUMPTION
            if space != []:
                # Move - leave grid to update my position?
                move_chance = rand.random()
                if verbose:
                    print("move chance", move_chance)
                if move_chance < self.motility_rate:
                    rand.shuffle(space)
                    if verbose:
                        print("moving")
                        print(space)
                    destination = space.pop()
                    if verbose:
                        print("move to: ", destination) 
                    space.append((self.x,self.y)) 
                    if self.tree_node != None:
                        self.tree_node.track_move(destination)
                # Divide
                if rand.random() < self.proliferation_rate:
                    if verbose: 
                        print("Dividing")
                    # consume resources to divide
                    self.energy_budget -= PROLIFERATION_COST
                    self.energy_budget /= 2 # half for daughter
                    # proliferate
                    rand.shuffle(space)
                    daughter_location = space.pop()
                    daughter = Cell(
                                mutation_rate = self.mutation_rate,
                                proliferation_rate = self.proliferation_rate,
                                hazard_resistance = self.hazard_resistance,
                                motility_rate = self.motility_rate,
                                x = daughter_location[0],
                                y = daughter_location[1],
                                energy = self.energy_budget
                                )
                    if self.tree_node != None:
                        # clear the former tree-node's reference to this cell.
                        self.tree_node.set_cell_reference(None)
                        # make tree nodes for the products of the division/
                        daughter0_node, daughter1_node  = self.tree_node.track_division((self.x,self.y), daughter_location,)
                        # give the cells refs to new tree nodes
                        self.set_tree_node(daughter0_node)
                        daughter.set_tree_node(daughter1_node)
                        # give the tree nodes refs to cells
                        self.tree_node.set_cell_reference(self)
                        daughter.tree_node.set_cell_reference(daughter)
        return (destination, (daughter, daughter_location), self.dead)

    def set_location(self, x,y):
        self.x = x
        self.y = y

    def get_location(self):
        return (self.x, self.y)

    def set_tree_node(self, node):
        self.tree_node = node

    def set_color(self, color):
        self.color = color

    def __repr__(self):
        delim = "======="
        string = delim + "\nmutation rate: " + str(self.mutation_rate) + "\n"
        string += "proliferation_rate: " + str(self.proliferation_rate) + "\n"
        string += "hazard_resistance: " + str(self.hazard_resistance) + "\n"
        string += "motility_rate: " + str(self.motility_rate) + "\n"
        string += "x: " + str(self.x) + "\n"
        string += "y: " + str(self.y) + "\n"
        string += "dead: " + str(self.dead) + "\n"
        string += delim
        return string


## just use id function on cells ##
class debugCell(Cell):
    
    def __init__(self, mutation_rate=0, proliferation_rate=0, hazard_resistance=0, motility_rate=0, x=0, y=0, tree=None, idn=None):
        super().__init__(mutation_rate, proliferation_rate, hazard_resistance, motility_rate, x, y, tree)
        self.idn = idn

    def __repr__(self):
        return str(self.idn)
