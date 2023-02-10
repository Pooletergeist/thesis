# This module contains the class structure decompositon for the energy-budget
# simulation.
#
## JMP. 2023/01/22
#
#

'''
The "world" class defines a grid.
Within the world, cells move and reproduce probabilistically, dying if energy
expenditure exceeds available resources.

Each time step, a cell expends energy. If a cell expends all its energy,
it dies.

Otherwise,

Energy expenditure is ??constant?? ??inversely related to p(spontaneous death)??
'''

## PARAMETERS ## - cell attributes? Mutable?
C_REPRODUCE
C_SURVIVE
C_MOVE

class world :
    def __init__():
        self.width = 
        self.height = 
        self.grid

        self.liveCells = 
        self.deadCells =

class newCell : 
    def __init__():
        self.p_reproduce
        self.p_move
