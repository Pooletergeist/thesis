#
# Nov. 8: Given a Host object, ASCII print the tumor cells in their grid?
# Then run a toy small simulation

from cscs import *
import time

N_DAYS = 1
STEPS_PER_DAY = 12
P_DIVIDE = 1/12
P_SYMDIV = 0.05
P_MUTATION = 0.5
PROLIFERATIVE_CAPACITY = 10
MIGRATION_POTENTIAL = 15
P_DEATH = 0.01

def toyVisualize(N_Days, Steps_Per_Day, P_Div, P_SymDiv, P_Mut, Pro_Cap,
                Mig_Pot, P_Dea): 

    tumor = cell(P_Div, P_SymDiv, P_Mut, Mig_Pot, P_Dea, Pro_Cap)
    patient =  host(tumor)

    for i in range(N_Days):
        print("Day: " + str(i)) 
        for j in range(Steps_Per_Day):
            time.sleep(0.1)
            patient.time_step()
            print(repr(patient))

    ## summarize simulation ##
    return patient


if __name__ == "__main__":
    toyVisualize(
        N_DAYS,
        STEPS_PER_DAY,
        P_DIVIDE,
        P_SYMDIV,
        P_MUTATION,
        PROLIFERATIVE_CAPACITY,
        MIGRATION_POTENTIAL,
        P_DEATH
        )
    # step through 24 steps
    # go next?
