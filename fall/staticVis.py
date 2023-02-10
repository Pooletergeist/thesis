#
# Nov. 8: Given a Host object, ASCII print the tumor cells in their grid?
# Then run a toy small simulation

from staticCSCS import *
import time

WIDTH = 20 # FLAG: what are good values here?
HEIGHT = 20 

N_DAYS = 10
STEPS_PER_DAY = 2
P_DIVIDE = 0.5
P_SYMDIV = 0.05
P_MUTATION = 0.5
PROLIFERATIVE_CAPACITY = 10
MIGRATION_POTENTIAL = 0.5
P_DEATH = 0.01

def longVisualize(N_Days, Steps_Per_Day, P_Div, P_SymDiv, P_Mut, Pro_Cap,
                Mig_Pot, P_Dea, Width, Height): 

    tumor = cell(P_Div, P_SymDiv, P_Mut, Mig_Pot, P_Dea, Pro_Cap)
    patient = host(Width, Height, tumor, Random_Start=False, Verbose=True)

    for i in range(N_Days):
        print("Day: " + str(i)) 
        print(repr(patient))
        for j in range(Steps_Per_Day):
            patient.time_step()

    ## summarize simulation ##
    return patient

def stepVisualize(N_Days, Steps_Per_Day, P_Div, P_SymDiv, P_Mut, Pro_Cap,
                Mig_Pot, P_Dea, Width, Height): 

    tumor = cell(P_Div, P_SymDiv, P_Mut, Mig_Pot, P_Dea, Pro_Cap)
    patient = host(Width, Height, tumor, Random_Start=False, Verbose=True)

    count = 0
    print(repr(patient))
    while input() != None:
        patient.time_step()
        count += 1
        if count % Steps_Per_Day == 0:
            print("New Day")

    ## summarize simulation ##
    return patient


if __name__ == "__main__":
    stepVisualize(
        N_DAYS,
        STEPS_PER_DAY,
        P_DIVIDE,
        P_SYMDIV,
        P_MUTATION,
        PROLIFERATIVE_CAPACITY,
        MIGRATION_POTENTIAL,
        P_DEATH,
        WIDTH,
        HEIGHT
        )
    # step through 24 steps
    # go next?
