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

    def update(self, space, resources, hazards):
        destination = None # would samelocation be fewer checks?
        daughter = None
        daughter_location = None
        # Mutate?
        if hazards > self.hazard_resistance:
            # Die
            self.dead = True
            if self.tree_node != None:
                self.tree_node.track_death((self.x,self.y))
        elif space != []:
            # Move - QUESTION: leave grid to update my position?
            if rand.random() < self.motility_rate:
                rand.shuffle(space)
                destination = space.pop()
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
                        daughter_node = self.tree_node.track_division( 
                                                        daughter_location)
                        daughter.set_tree_node(daughter_node)
        return (destination, (daughter, daughter_location), self.dead)

    def set_location(self, x,y):
        self.x = x
        self.y = y

    def get_location(self):
        return (self.x, self.y)

    def set_tree_node(self, node):
        self.tree_node = node

    def __str__(self):
        '''readable debug. just gives cell id'''
        return "X"

    def __repr__(self):
        string = "mutation rate: " + str(self.mutation_rate) + "\n"
        string += "proliferation_rate: " + str(self.proliferation_rate) + "\n"
        string += "hazard_resistance: " + str(self.hazard_resistance) + "\n"
        string += "motility_rate: " + str(self.motility_rate) + "\n"
        string += "x: " + str(self.x) + "\n"
        string += "y: " + str(self.y) + "\n"
        string += "dead: " + str(self.dead) + "\n"
        return string

