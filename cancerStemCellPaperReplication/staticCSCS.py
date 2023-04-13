#
# Nov 9:
#

# https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004025#sec008
#

## With optimizations: 
## 1. Pre-allocated non-growing domain. (Need flag for growing off the edge)
## 2. List of Live Cells (must know location)
## 3. Stem inherits from nonstem? (unimplemented)

import random as rand
import time

#### Constants ####
# Body
N_CSCs = 1
N_DAYs = 730
STEPS_PER_DAY = 24

WIDTH = 5000 # FLAG: what are good values here?
HEIGHT = 5000 

# Cell
P_DIVIDE = 1/24
P_SYMDIV = 0.05
P_MUTATION = 0.5
PROLIFERATIVE_CAPACITY = 10
MIGRATION_POTENTIAL = 15
P_DEATH = 0.01

rand.seed(123) # set seed

class host:

    def __init__(self, Width, Height, Tumor, Random_Start=True, Verbose=False):
        '''Builds Host with Cellular Matrix & list of live cells'''
        # Build the Tumor Microenvironment — a 2D matrix of empty cells
        matrix = [] # 2-Dim. Lattice
        for i in range(Width):
            matrix.append([None]*Height) # Outer List: Col. Inner: row 

        if Random_Start:
            starting_x = rand.randint(0,Width-1)
            starting_y = rand.randint(0,Height-1)
        else:
            starting_x = Width//2
            starting_y = Height//2

        matrix[starting_x][starting_y] = Tumor   # Put in the cancer cell
        Tumor.setLocation(starting_x, starting_y) # tell tumor where it is

        self.matrix = matrix     # save matrix in attribute
        self.liveCells = [Tumor] # maintain a list of live cells to update each time step

        self.width = Width
        self.height = Height

        self.day = 0         # attribute for tracking day. Cells can only move so many times per day.
        self.hour = 0

        self.verbose = Verbose

    def time_step(self):
        ## update time
        self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1
            print("day = " + str(self.day))     # debug
            print(self)
        ## Cells considered in random order...
        cell_indices = list(range(len(self.liveCells)))
        rand.shuffle(cell_indices)
        for ix in cell_indices:
            cell = self.liveCells[ix]
            space = cell.where_space(self)
            if space != []:                               # check quiescence
                action,obj = cell.time_step(space, self.day)            # activate cell
                self.do(action, obj, space)

    def do(self, action, obj, space):
        if action != None:
            place = rand.choice(space) 
            col,row = obj.getLocation() # either move, grow, or dead. obj will be a cell. If growing new cell, col&row r None
            if self.verbose:
                self.pretty_print(action, obj, place)
            if action == "dead":
                self.matrix[col][row] = None
                self.liveCells.remove(self)
            else:
                if place[0] > self.width or place[1] >= self.height:
                    raise Exception("growing or moving off edge!")
                else:
                    obj.setLocation(place[0],place[1])                      # tell newCell or moved cell where it will be
                    if action == "move":
                        #print(col)
                        self.matrix[place[0]][place[1]] = self.matrix[col][row] # copy cell to new place 
                        self.matrix[col][row] = None                            # remove cell from old spot
                    elif action == "grow":
                        self.matrix[place[0]][place[1]] = obj                   # put newCell into place 
                        self.liveCells.append(obj)
                    else:
                        raise Exception("Unexpected action passed from time_step")

    def pretty_print(self, action, obj, place):
        # if moving, must insert _ and new cell into place
        # if growing, must insert + and new cell into place
        # if dead, must insert X
        print(action)
        string = ""
        for row in range(len(self.matrix[0])):
            string += "\n"
            for col in range(len(self.matrix)):
                cell = self.matrix[col][row]
                x,y = obj.getLocation()
                if col == place[0] and row == place[1]: # new cell position. birth or movement
                    if action == "grow":
                        string += "o "
                    elif action == "move":
                        string += "> "
                    else:
                        raise Exception ("Unimplemented")
                elif col == x and row == y:
                    if action == "dead":
                        string += "X " 
                    elif action == "move":
                        string += "- "
                    elif action == "grow":
                        string += "+ "
                elif self.matrix[col][row] != None:
                    string += "1 "
                else:
                    string += "0 "
        print(string)

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
                P_DIVIDE,
                P_SYMDIV, 
                P_MUTATION,
                MIGRATION_POTENTIAL, 
                P_DEATH,
                Prolif_capacity):

        self.p_div = P_DIVIDE
        self.p_divCSC = P_SYMDIV
        self.p_mutate = P_MUTATION
        self.p_move = MIGRATION_POTENTIAL
        self.p_die = P_DEATH
        self.cc_pot = Prolif_capacity
        self.day = 0                    # track moves per day
        self.moves = self.p_move        # moves per day
        self.alive = True
        self.location = (None,None)

    def setLocation(self,x,y):
        self.location = (x,y)

    def getLocation(self):
        return self.location

    def where_space(self, host):
        # check 8 adjacent spaces
        col,row = self.getLocation()
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
                    return ("dead", self) 
            newCell = cell(self.p_div, self.p_divCSC, self.p_mutate, self.p_move, self.p_die, self.cc_pot)
        else:
            #produce ordinary CC
            newCell = nonstem(self.p_div, self.p_divCSC, self.p_mutate, self.p_move, self.p_die, self.cc_pot)
        return ("grow", newCell)
        
    def move(self):
        return ("move", self)

    def die(self):
        return ("dead", self)

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
            return ("dead", self)


'''
The model is realized as an asynchronous cellular automaton in which cell events are stochastically driven. A cell, either cancer stem cell (CSC) or non-stem cancer cell (CC), occupies a single grid point of (10μm)2 on a two-dimensional square lattice. Each CSC is characterized by its specific trait vector [ps, ρmax, μ, α] denoting probability of symmetric division, proliferation capacity, migration potential and spontaneous death probability, respectively. According to the cancer stem cell hypothesis, CSCs have unlimited proliferation potential and thus their proliferative capacity ρmax does not exhaust. At each division CSCs produce either another CSC with probability ps (symmetric division) or a CC with probability 1-ps (asymmetric division). CCs that are direct offspring of a CSC inherit the initial proliferation capacity ρ that decreases with each cell division (Fig. 5A). At ρ = 0, CCs die and are removed from the simulation. At each proliferation attempt, cells may undergo spontaneous death with probability α and then be removed from the system. Both tumor subpopulations are equipped with migration potential μ representing number of potential cell displacements into neighboring lattice sites per day. We assume that cells need adjacent space for migration and proliferation, and cells that are completely surrounded by other cells (eight on a two-dimensional lattice) become quiescent (Fig. 5B). In unsaturated environments, cells proliferate and migrate into vacant adjacent space at random. To avoid artifacts caused by computational domain boundaries we introduce a dynamically growing domain.

--
We assume that a single mutation affects at most one trait and induces a stochastic positive or negative unit change of the trait parameter value, i.e. ps±0.01, ρmax±1, μ±1, or α±0.001. The trait to be mutated is chosen at random from a discrete uniform distribution. The modified trait vector is inherited by both CSCs and then further propagated to their respective CC populations. If a trait becomes negative the cell is considered unviable and removed from the simulation
--

Simulation time is advanced at discrete time intervals Δt = 1/24 day (i.e., 1 hour), that is 24 simulation steps equal one day. At each simulation time step, cells are considered in random order and the behavior of each cell is updated. Cell proliferation, migration and death are random events with the respective probabilities scaled to simulation time. Cell proliferation and migration are temporally mutually exclusive events, and cell death only occurs when cell actively attempts to proliferate. We assume that cells proliferate on average once per day (proliferation probability pd = 1×Δt), migrate with probability (1-pd)pm and die with probability pdα. Let pm = μ×Δt, where the parameter μ denote motility of cancer cells. Due to the stochastic nature of the model we perform at least 100 independent simulations for each discussed case and report average values and standard deviations.
'''

## expect death 20%
def runSimulation(N_CSCs,
                  N_DAYs,
                  STEPS_PER_DAY,
                  P_DIVIDE,
                  P_SYMDIV,
                  P_MUTATION,
                  PROLIFERATIVE_CAPACITY,
                  MIGRATION_POTENTIAL,
                  P_DEATH):

    tumor = cell(P_DIVIDE, P_SYMDIV, P_MUTATION, MIGRATION_POTENTIAL, P_DEATH, PROLIFERATIVE_CAPACITY)
    patient =  host(WIDTH, HEIGHT, tumor)
    for i in range(N_DAYs * STEPS_PER_DAY):
        patient.time_step()

    ## summarize simulation ##
    print(patient)
    return patient


### Main ###
if __name__ == "__main__":

    start = time.perf_counter()
    runSimulation(N_CSCs,
                  N_DAYs,
                  STEPS_PER_DAY,
                  P_DIVIDE,
                  P_SYMDIV,
                  P_MUTATION,
                  PROLIFERATIVE_CAPACITY,
                  MIGRATION_POTENTIAL,
                  P_DEATH)
    end = time.perf_count()
    print('time: ' + str(end-start))
