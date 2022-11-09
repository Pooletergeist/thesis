# Nov.2
#
# https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004025#sec008
#

## Note: only set up for 1CSC start
## Note: cells can only move so far per day (hard limit not stochastic, unsure from paper).

## TODO: complexity?
## Restructure st stem inherits from nonstem.

import random as rand
from collections import deque # for list prepend performance? access vs. prepend: what'll be slower? ## unimplemented
import time

#### Constants ####
# Body
N_CSCs = 1
N_Days = 730
Steps_Per_Day = 24

# Cell
P_Divide = 1/24
P_SymDiv = 0.05
P_Mutation = 0.5
Proliferative_Capacity = 10 
Migration_Potential = 15
P_Death = 0.01

rand.seed(123) # set seed


class host:
    ### Static Attribute Constants ###
    Lattice_Height = 4
    Lattice_Width = 4
    Lattice_Grow = 50 # when cell hits boundary, boundary expands

    def __init__(self, tumor):
        matrix = [] # 2-Dim. Lattice
        for i in range(host.Lattice_Width):
            matrix.append([None]*host.Lattice_Height) # Outer List: Col. Inner: row 
        starting_x = rand.randint(0,host.Lattice_Width-1)
        starting_y = rand.randint(0,host.Lattice_Height-1)
        matrix[starting_x][starting_y] = tumor   # Put in the cancer cell
        self.matrix = matrix # save in attribute
        self.day = 0         # attribute for tracking day. Cells can only move so many times per day.
        self.hour = 0

    def time_step(self):
        ## update time
        self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1
            print("day = " + str(self.day))     # debug
            print(self)
        ## Cells considered in random order...
        x_indices = list(range(len(self.matrix)))
        y_indices = list(range(len(self.matrix[0])))
        rand.shuffle(x_indices)
        rand.shuffle(y_indices)
        for col in x_indices:
            for row in y_indices:
                cell = self.matrix[col][row]
                if cell != None: # there's a cell
                    if col == len(self.matrix)-1:    # it's on an edge
                        self.grow_right()
                    elif col == 0:
                        self.grow_left()
                        col = col + self.Lattice_Grow       # re-index. since domain grew
                    if row == len(self.matrix[0])-1:            # it's on an edge
                        self.grow_down()
                    elif row == 0:
                        self.grow_up()
                        row = row + self.Lattice_Grow

                    space = cell.where_space(self, col, row)
                    if space != []:                               # check quiescence
                        action,obj = cell.time_step(space, self.day)            # activate cell
                        self.do(action, obj, col, row, space)

    def do(self, action, obj, col, row, space):
        print(action)
        if action != None:
            if action == "dead":
                self.matrix[col][row] = None
            else:
                place = rand.choice(space) 
                if action == "move":
                    #print(col)
                    self.matrix[place[0]][place[1]] = self.matrix[col][row] # copy cell to new place 
                    self.matrix[col][row] = None                            # remove cell from old spot
                elif action == "grow":
                    self.matrix[place[0]][place[1]] = obj                   # put newCell into place 
                else:
                    raise Exception("Unexpected action passed from time_step")

    def grow_right(self):
        # make Lattice_Grow more lists
        print("growing right")
        height = len(self.matrix[0])
        for i in range(self.Lattice_Grow):
            self.matrix.append([None]*height)
    
    def grow_left(self):
        # make Lattice_Grow more lists
        print("growing left")
        height = len(self.matrix[0])
        for i in range(self.Lattice_Grow):
            self.matrix.insert(0,[None]*height)
        
    def grow_down(self):
        print("growing down")
        # make each inner list Lattice_Grow longer
        for colList in self.matrix:
            colList.extend([None]*self.Lattice_Grow)

    def grow_up (self):
        print("growing up")
        # make each inner list Lattice_Grow longer
        for ix in range(len(self.matrix)):
            self.matrix[ix] = [None] * self.Lattice_Grow + self.matrix[ix]

    def __repr__(self):
        string = ""
        for row in range(len(self.matrix[0])):
            string += "\n"
            for col in range(len(self.matrix)):
                cell = self.matrix[col][row]
                if self.matrix[col][row] != None:
                    string += "1 "
                else:
                    string += "0 "
        return string

    def __str__(self):
        string = ""
        string += "width = " + str(len(self.matrix))
        string += "\n"
        string += "height = " + str(len(self.matrix[0]))
        string += "\n"
        n_live = 0
        for col in range(len(self.matrix)):
            for row in range(len(self.matrix[0])):
                elmt = self.matrix[col][row]
                if elmt != None:
                    n_live += 1
                    #string += str(col) + "," + str(row) + "\n"
        string += "n_tumor cells = " + str(n_live)

        ## where are the tumor cells? ##
        return string
            
class cell:
    def __init__(self,
                P_Divide,
                P_SymDiv, 
                P_Mutation,
                Migration_Potential, 
                P_Death,
                Prolif_capacity):

        self.p_div = P_Divide
        self.p_divCSC = P_SymDiv
        self.p_mutate = P_Mutation
        self.p_move = Migration_Potential
        self.p_die = P_Death
        self.cc_pot = Prolif_capacity
        self.day = 0                    # track moves per day
        self.moves = self.p_move        # moves per day
        self.alive = True

    def where_space(self, host, col, row):
        # check 8 adjacent spaces
        space = []
        #print(str(col) + "," + str(row))
        if host.matrix[col-1][row-1] == None:
            space.append((col-1,row-1))

        if host.matrix[col-1][row] == None:
            space.append((col-1,row))

        if host.matrix[col-1][row+1] == None:
            space.append((col-1,row+1))

        if host.matrix[col][row-1] == None:
            space.append((col,row-1))

        if host.matrix[col][row+1] == None:
            space.append((col,row+1))

        if host.matrix[col+1][row-1] == None:
            space.append((col+1,row-1))

        if host.matrix[col+1][row] == None:
            space.append((col+1,row))

        if host.matrix[col+1][row+1] == None:
            space.append((col+1,row+1))

        return space
    
    def time_step(self, space, date):
        # choose between temporally exclusive move, grow, and nothing
        if rand.random() < self.p_div: # divide (grow)
            return self.divide()

        elif rand.random() < 1/24 * self.p_move: # migrate according to movement potential.
            if date > self.day:
                self.day = date
                self.moves = self.p_move
            if self.moves > 0:
                return self.move()
        else:
            return (None, None)
        
    
    def divide(self):
        if rand.random() < self.p_die:
            #spontaneous death
            return self.die()
        elif rand.random() < self.p_divCSC:
            #produce CSC
            if rand.random() < self.p_mutate:
                if not self.mutate(): # dies during mutation
                    return ("dead", None) 
            newCell = cell(self.p_div, self.p_divCSC, self.p_mutate, self.p_move, self.p_die, self.cc_pot)
        else:
            #produce ordinary CC
            newCell = nonstem(self.p_div, self.p_divCSC, self.p_mutate, self.p_move, self.p_die, self.cc_pot)
        return ("grow", newCell)
        
    def move(self):
        return ("move", None)

    def die(self):
        return ("dead", None)

    def mutate(self):
        coinflip = rand.choice([0,1,2,3])
        valence = rand.choice([True, False])
        if coinflip == 0:
            # mutate symdiv
            if valence:
                self.p_divCSC += 0.01 
            else:
                self.p_divCSC -= 0.01
                if self.p_div < 0:
                    return False
        elif coinflip == 1:
            # mutate proliferative capacity of descendents
            if valence:
                self.cc_pot += 1
            else:
                self.cc_pot -= 1
                if self.cc_pot < 0:
                    return False
        elif coinflip == 2:
            # mutate motility
            if valence:
                self.p_move += 1
            else:
                self.p_move -= 1
                if self.p_move < 0:
                    return False
        else:
            # mutate death chance
            if valence:
                self.p_die += 0.001
            else:
                self.p_die -= 0.001
                if self.p_die < 0:          # any trait negative means death
                    return False
        return True                         # successful mutation

class nonstem(cell):
    def __init__(self, p_div, p_divCSC, p_mutate, p_move, p_die, Prolif_capacity):
       super().__init__(p_div, p_divCSC, p_mutate, p_move, p_die, Prolif_capacity)
       self.max_grow = Prolif_capacity

    def divide(self):
        if self.max_grow > 0:
            # divide
            self.max_grow -= 1
            return ("grow", nonstem(self.p_div, self.p_divCSC, self.p_mutate, self.p_move, self.p_die, self.max_grow))
        else:
            return ("dead", None)


'''
The model is realized as an asynchronous cellular automaton in which cell events are stochastically driven. A cell, either cancer stem cell (CSC) or non-stem cancer cell (CC), occupies a single grid point of (10μm)2 on a two-dimensional square lattice. Each CSC is characterized by its specific trait vector [ps, ρmax, μ, α] denoting probability of symmetric division, proliferation capacity, migration potential and spontaneous death probability, respectively. According to the cancer stem cell hypothesis, CSCs have unlimited proliferation potential and thus their proliferative capacity ρmax does not exhaust. At each division CSCs produce either another CSC with probability ps (symmetric division) or a CC with probability 1-ps (asymmetric division). CCs that are direct offspring of a CSC inherit the initial proliferation capacity ρ that decreases with each cell division (Fig. 5A). At ρ = 0, CCs die and are removed from the simulation. At each proliferation attempt, cells may undergo spontaneous death with probability α and then be removed from the system. Both tumor subpopulations are equipped with migration potential μ representing number of potential cell displacements into neighboring lattice sites per day. We assume that cells need adjacent space for migration and proliferation, and cells that are completely surrounded by other cells (eight on a two-dimensional lattice) become quiescent (Fig. 5B). In unsaturated environments, cells proliferate and migrate into vacant adjacent space at random. To avoid artifacts caused by computational domain boundaries we introduce a dynamically growing domain.

--
We assume that a single mutation affects at most one trait and induces a stochastic positive or negative unit change of the trait parameter value, i.e. ps±0.01, ρmax±1, μ±1, or α±0.001. The trait to be mutated is chosen at random from a discrete uniform distribution. The modified trait vector is inherited by both CSCs and then further propagated to their respective CC populations. If a trait becomes negative the cell is considered unviable and removed from the simulation
--

Simulation time is advanced at discrete time intervals Δt = 1/24 day (i.e., 1 hour), that is 24 simulation steps equal one day. At each simulation time step, cells are considered in random order and the behavior of each cell is updated. Cell proliferation, migration and death are random events with the respective probabilities scaled to simulation time. Cell proliferation and migration are temporally mutually exclusive events, and cell death only occurs when cell actively attempts to proliferate. We assume that cells proliferate on average once per day (proliferation probability pd = 1×Δt), migrate with probability (1-pd)pm and die with probability pdα. Let pm = μ×Δt, where the parameter μ denote motility of cancer cells. Due to the stochastic nature of the model we perform at least 100 independent simulations for each discussed case and report average values and standard deviations.
'''

## expect death 20%
def runSimulation(N_CSCs,
                  N_Days,
                  Steps_Per_Day,
                  P_Divide,
                  P_SymDiv,
                  P_Mutation,
                  Proliferative_Capacity,
                  Migration_Potential,
                  P_Death):

    tumor = cell(P_Divide, P_SymDiv, P_Mutation, Migration_Potential, P_Death, Proliferative_Capacity)
    patient =  host(tumor)
    for i in range(N_Days * Steps_Per_Day):
        patient.time_step()

    ## summarize simulation ##
    print(patient)
    return patient


### Main ###
if __name__ == "__main__":

    start = time.perf_counter()
    runSimulation(N_CSCs,
                  N_Days,
                  Steps_Per_Day,
                  P_Divide,
                  P_SymDiv,
                  P_Mutation,
                  Proliferative_Capacity,
                  Migration_Potential,
                  P_Death)
    end = time.perf_count()
    print('time: ' + str(end-start))
