#
## Apr. 4 TEST ME!!!
#

# search for equilibria?
## after some number of generations, get cells filling some proportion of 
## screen?

## for some number of seeds?

def count_cells(matrix):
    n_cells = 0
    for col in range(len(matrix)):
        for row in range(len(matrix[0])):
            if matrix[row][col] != None:
               n_cells += 1 
    return n_cells

def more_than_x(matrix, fraction):
    n = count_cells(matrix)
    if n / (len(matrix) * len(matrix)) >= fraction:
        return (n, True)
    else:
        return (n, False)

def write_trial_to_file(filename, trial_data):
    '''procedure appending trial_data string to file'''
    with open(filename, "a") as f:
        f.write(trial_data) 

def write_colnames_to_file(filename, colnames_list):
    '''csv firstline as colnames'''
    line = ""
    for colname in colnames_list:
        line += colname + ", "
    line += "\n"
    with open(filename, "w") as f:
        f.write(line)

def gather_trial_data(matrix, threshold, colnames_list, variable_dict):
    '''records cell_count and variables from dict into comma-separated str'''
    ## analyze final matrix state, add to dict
        # => enables 'n_cells' and 'moreThan0.y' as colnames
    n_cells, bigger_than_fraction = more_than_x(matrix, threshold)
    variable_dict["nCells"] = n_cells
    variable_dict["moreThan" + str(threshold)] = bigger_than_fraction
    ## write to string from dict according to colnames
    trial_data = ""
    for colname in colnames_list:
        try:
            assert(colname in variable_dict)
            trial_data += str(variable_dict[colname]) + ", "
        except:
            trial_data += "colname-not-present" + ", "
    return trial_data + "\n" # end the line!

def save_pickle(filename, data):
    '''simple pickle wrapper'''
    with open(filename + ".pkl", "wb") as f:
        pickle.dump(data, f)

## track successes & failures in CSV

# File_Writing:
# 1. run simulation
# 2. record column list
# 3. use gather_trial_data with matrix output, column list 
# 4. run write_trial_to_file on output of gather_trial_data

'''
RSRC_INIT
RSRC_RANGE # tuple (min, max)
HZRD_RANGE # tuple (min, max
N_CELLS

H_INCREMENT
R_INCREMENT
'''

import pickle
def grid_search(
                SIM_FUNC, 
                RSRC_RANGE, HZRD_RANGE, H_INCREMENT, R_INCREMENT, 
                W=50, H=50, INIT_X=25, INIT_Y=25, GENERATION_INTERVAL=100, 
                MUT_RATE=0, DIV_RATE=0.1, HAZ_RES=1, MOV_RATE=0.2, N_CELLS=1,
                THRESHOLD=0.5, COLNAMES_LIST=["rAmt", "hAmt", "nInitCell",
                                        "w", "h", "divRt", "movRt", "gens"], 
                 TITLE_PREFIX = ""
                ):
    # assumes you import the experiment util to run a simulation correctly
    # and that it returns the final grid state
    output_filename = (TITLE_PREFIX + "rRange=" +  str(RSRC_RANGE) +
                "_hRange=" + str(HZRD_RANGE) + "_nCell=" + str(N_CELLS) +
                "_hInc=" + str(H_INCREMENT) + "_rInc" + str(R_INCREMENT) + 
                "_w=" + str(W) + "_h=" + str(H) + "_divRt=" + str(DIV_RATE) + 
                "_movRt" + str(MOV_RATE) + ".csv")

    if "moreThan" + str(THRESHOLD) not in COLNAMES_LIST:
        COLNAMES_LIST.append("moreThan" + str(THRESHOLD))
    if "nCells" not in COLNAMES_LIST:
        COLNAMES_LIST.append("nCells")
    write_colnames_to_file(output_filename, COLNAMES_LIST)
    
    # prepare data dictionary for sim
    summary_dict = {}
    summary_dict["nInitCell"] = N_CELLS
    summary_dict["w"] = W
    summary_dict["h"] = H
    summary_dict["divRt"] = DIV_RATE
    summary_dict["movRt"] = MOV_RATE
    summary_dict["gens"] = GENERATION_INTERVAL

 
    rsrc_amt = RSRC_RANGE[0]
    hzrd_amt = HZRD_RANGE[0]
    while rsrc_amt < RSRC_RANGE[1]:
        while hzrd_amt < HZRD_RANGE[1]:
            #
            pickle_title = (TITLE_PREFIX + "rAmt=" +  str(rsrc_amt) +
                "_hAmt=" + str(hzrd_amt) + "_nCell=" + str(N_CELLS) +
                "_hInc=" + str(H_INCREMENT) + "_rInc" + str(R_INCREMENT) + 
                "_w=" + str(W) + "_h=" + str(H) + "_divRt=" + str(DIV_RATE) + 
                "_movRt" + str(MOV_RATE))
            
            # update summary with current trial values
            summary_dict["rAmt"] = rsrc_amt
            summary_dict["hAmt"] = hzrd_amt

            # run sim
            sim_state = SIM_FUNC(
                            W=W, H=H, INIT_X=INIT_X, INIT_Y = INIT_Y,
                            GENERATIONS = GENERATION_INTERVAL, 
                            MUT_RATE = MUT_RATE, DIV_RATE = DIV_RATE, 
                            HAZ_RES = HAZ_RES, MOV_RATE = MOV_RATE,
                            RSRC_AMT = rsrc_amt,
                            HZRD_AMT = hzrd_amt,
                            VISUALIZE=False # maybe not in running-mode
                            )

            # save pickle
            save_pickle((pickle_title + str(GENERATION_INTERVAL)), sim_state)

            # write summary
            s1 = gather_trial_data(matrix=sim_state.grid, threshold = THRESHOLD,
                    colnames_list = COLNAMES_LIST, variable_dict = summary_dict)
            write_trial_to_file(filename = output_filename, trial_data = s1)

            # run second generation interval
            for i in range(GENERATION_INTERVAL):
                sim_state.update()
            summary_dict["gens"] = 2*GENERATION_INTERVAL

            # save pickle2
            save_pickle((pickle_title + str(2*GENERATION_INTERVAL)), sim_state)

            # write summary
            s2 = gather_trial_data(matrix=sim_state.grid, threshold = THRESHOLD,
                    colnames_list = COLNAMES_LIST, variable_dict = summary_dict)
            write_trial_to_file(filename = output_filename, trial_data = s2)

            # update hzrd amt for next sim
            hzrd_amt += H_INCREMENT

        # update rsrc amt, reset hzrd amt for next round of sims
        rsrc_amt += R_INCREMENT
        hzrd_amt = HZRD_RANGE[0]

    print("done!")
    return output_filename
