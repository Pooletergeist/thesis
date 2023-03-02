#
#
## Feb. 2
#
#

## should cells be passed 'proliferation cost' in init or know as constant?
## does grid compute hazard death chance? or does the cell?

## should cells check if they have enough resources, or sometimes divide into
## death?

## TODO: report resource cost?
import random as rand

PROLIFERATION_COST = 0.5

class Cell:
    '''basic cell class, able to move grow and die'''

    def __init__(self, mutation_rate, 
                    proliferation_rate, 
                    hazard_resistance, 
                    motility_rate, 
                    x, 
                    y, 
                    t=None):
        self.mutation_rate = mutation_rate
        self.proliferation_rate = proliferation_rate
        self.hazard_resistance = hazard_resistance
        self.motility_rate = motility_rate
        self.x = x
        self.y = y
        self.tree_node = t
        self.dead = False
        self.color = (0,0,0) # default cells to black rgb

    def update(self, space, resources, hazards):
        destination = None # would samelocation be fewer checks?
        daughter = None
        daughter_location = None
        # Mutate?
        if hazards > self.hazard_resistance:
            print("ded")
            # Die
            self.dead = True
            if self.tree_node != None:
                self.tree_node.track_death((self.x,self.y))
        elif space != []:
            # Move - QUESTION: leave grid to update my position?
            move_chance = rand.random()
            print(move_chance)
            if move_chance < self.motility_rate:
                print("moving")
                rand.shuffle(space)
                print(space)
                destination = space.pop()
                print(destination)
                space.append((self.x,self.y)) 
                if self.tree_node != None:
                    self.tree_node.track_move(destination)
            # Divide
            if resources > PROLIFERATION_COST:
                if rand.random() < self.proliferation_rate:
                    rand.shuffle(space)
                    daughter_location = space.pop()
                    daughter = Cell(
                                mutation_rate = self.mutation_rate,
                                proliferation_rate = self.proliferation_rate,
                                hazard_resistance = self.hazard_resistance,
                                motility_rate = self.motility_rate,
                                x = daughter_location[0],
                                y = daughter_location[1]
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
                        daughter.tree_node.set_cell_reference(self)
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
        string = "mutation rate: " + str(self.mutation_rate) + "\n"
        string += "proliferation_rate: " + str(self.proliferation_rate) + "\n"
        string += "hazard_resistance: " + str(self.hazard_resistance) + "\n"
        string += "motility_rate: " + str(self.motility_rate) + "\n"
        string += "x: " + str(self.x) + "\n"
        string += "y: " + str(self.y) + "\n"
        string += "dead: " + str(self.dead) + "\n"
        return string


## just use id function on cells ##
class debugCell(Cell):
    
    def __init__(self, mutation_rate=0, proliferation_rate=0, hazard_resistance=0, motility_rate=0, x=0, y=0, tree=None, idn=None):
        super().__init__(mutation_rate, proliferation_rate, hazard_resistance, motility_rate, x, y, tree)
        self.idn = idn

    def __repr__(self):
        return str(self.idn)
