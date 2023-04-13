#
## Apr 13
#

# NOTE: pickles are saved as a triple (state, originator_nodes, originator_ids)
# for stats-ease from loading

# ALLCAPS means CONSTANT in current frame: locally immutable 

import random as rand
import numpy as np
import time
import datetime # time-stamp result titles

from UTILS import (stretch_seed, place_cells, make_new_nodes,
    make_file_path, write_colnames_to_file, append_str_to_file, 
    string_join, comma_join,
    save_pickle)

from energy_experiment_utils import (make_untracked_energy_cells,
    connect_cells_and_roots)

from mutate_utils import mutate_model
    

from Visualizer import Visualizer # for debug
import copy # to copy cells
import sys # to adjust recursion limit

CELL_LIST, CLONE_ID_LIST, NODE_LIST = make_untracked_energy_cells(N=1) 
assert len(CLONE_ID_LIST) == len(CELL_LIST) # sanity-check for user code

def write_pop_counts_and_div_rates_to_file(
                            FILENAME,  
                            NODE_LIST, 
                            CLONE_ID_LIST,
                            R_AMT, H_AMT,
                            GENS, SEED,
                            N_INIT_CELL,
                            W, H, 
                            DIRECTORY=None):
    '''writes 1 line per clone to file, and 1 summary line'''
    shared_suffix = comma_join([R_AMT, H_AMT, GENS, SEED, 
                        N_INIT_CELL, W, H]) + "\n"

    total_live_pop = 0
    total_historic_pop = 0
    total_sum_divRt = 0
    total_sum_variation_divRt = 0
    for clone_ix in range(len(NODE_LIST)):
        clone = NODE_LIST[clone_ix]
        # get clone population
        live_pop = clone.count_living_subtree()
        historic_pop = clone.count_subtree()
       # identify clone
        clone_name = CLONE_ID_LIST[clone_ix][0] + "_" + str(clone_ix)
        mutRt = CLONE_ID_LIST[clone_ix][3]
        # compute div rate stats
        sum_divRt = clone.sum_subtree_div_rate()
        mean_divRt = sum_divRt / live_pop
        sum_variation_divRt = clone.sum_variation_subtree_divRt(mean_divRt)
        variance_divRt = sum_variation_divRt / live_pop
       # UNUSED: movRt = CLONE_ID_LIST[clone_ix][2]
        # make table line
        line = (comma_join([clone_name, mut_Rt, mean_divRt, variance_divRt, 
                live_pop, historic_pop]) + shared_suffix)
        # write line
        append_str_to_file(FILENAME, line, DIRECTORY)

        # add to total tally
        total_live_pop += live_pop
        total_historic_pop += historic_pop
        total_sum_divRt += sum_divRt
        total_sum_variation_divRt += sum_variation_divRt
 
    # compute total stats
    total_mean_divRt = total_sum_divRt / total_live_pop
    total_variance_divRt = total_sum_variation_divRt / total_live_pop

    # write totals
    totals_line = (comma_join(["all", -1,
                    total_mean_divRt, total_variance_divRt,
                    total_live_pop, total_historic_pop]) + 
                    shared_suffix)

    append_str_to_file(FILENAME, totals_line, DIRECTORY)


def run_and_record_simulation(W, H, RSRC_AMT, RSRC_IV, HZRD_AMT, 
                             N_INIT_CELL, SEED, # already used, now just flags
                             CELL_LIST, node_list, CLONE_ID_LIST,
                             GENERATIONS, N_SNAPSHOTS,
                             FNAME, DIRECTORY, PICKLE_TITLE,
                             VISUALIZE):

    assert(len(CELL_LIST) == len(node_list) == N_INIT_CELL)

    # build sim model
    sim_state = mutate_model(W=W, H=H, RSRC_AMT = RSRC_AMT, 
        HZRD_AMT = HZRD_AMT, IV = RSRC_IV)

    place_cells(sim_state, CELL_LIST, node_list)

    if VISUALIZE:
        v = Visualizer(W, H, sim_state)
        v.display("start")

    # update GENERATIONS-many times in snapshot-many intervals
    for i in range(1, N_SNAPSHOTS+1):
        # run partway, save pop_counts
        generations_run = 0
        while generations_run < (i * GENERATIONS)//N_SNAPSHOTS:
            sim_state.update()
            generations_run += 1

        if VISUALIZE:
            v.display("after " + str(generations_run) + " generations")

        try:
            # save pickle triple: (sim_state, originator_nodes, originator_ids)
            save_pickle((PICKLE_TITLE + str(generations_run)), 
                        (sim_state, node_list, CLONE_ID_LIST),
                        DIRECTORY)
        except:
            print('pickle not saved', " r=", RSRC_AMT, " h=", HZRD_AMT)
            save_pickle(("error-pickling_" + PICKLE_TITLE + 
                        str(generations_run)), "no pickle",
                        DIRECTORY)

        # write summary
        write_pop_counts_to_file(FILENAME = FNAME, 
                        NODE_LIST = node_list,
                        CLONE_ID_LIST = CLONE_ID_LIST,
                        R_AMT = RSRC_AMT, H_AMT = HZRD_AMT,
                        GENS = generations_run, SEED=SEED,
                        N_INIT_CELL=N_INIT_CELL,
                        W=W, H=H, 
                        DIRECTORY=DIRECTORY)

    return sim_state



def grid_search(SEED, FNAME, # passed as flags
               RSRC_RANGE,  # used here
               R_INCREMENT, # used here
               HZRD_RANGE,  # used here
               H_INCREMENT, # used here
               RSRC_IV,     # passed
               CELL_LIST, # passed
               CLONE_ID_LIST, # passed
               N_INIT_CELL, # passed
               W, H,
               GENERATIONS,
               N_SNAPSHOTS,
               TITLE_PREFIX, DIRECTORY,
               VISUALIZE): 

    assert(N_INIT_CELL == len(CELL_LIST)) 

    # grid search over rsrcs and hazards
    rsrc_amt = RSRC_RANGE[0]
    hzrd_amt = HZRD_RANGE[0]
    while rsrc_amt < RSRC_RANGE[1]:
        while hzrd_amt < HZRD_RANGE[1]:
        #
            pickle_title = (TITLE_PREFIX + "rAmt=" +  str(round(rsrc_amt,2)) +
                "_hAmt=" + str(round(hzrd_amt,2)) + 
                "_nInitCell=" + str(N_INIT_CELL) +
                "_hInc=" + str(H_INCREMENT) + "_rInc" + str(R_INCREMENT) +
                "_w=" + str(W) + "_h=" + str(H))  

            # copy fresh cell_list and make new empty nodes to track, 
            # so one sim does not affect the next
            this_cell_list = copy.deepcopy(CELL_LIST)
            this_node_list = make_new_nodes(len(CELL_LIST))
            # link together
            connect_cells_and_roots(this_cell_list, this_node_list)
    
            # Run Simulation
            run_and_record_simulation(W=W, H=H, 
                            RSRC_AMT = rsrc_amt, RSRC_IV = RSRC_IV,
                            HZRD_AMT = hzrd_amt, 
                             N_INIT_CELL = N_INIT_CELL, SEED=SEED, # flags
                             CELL_LIST = this_cell_list, 
                            node_list = this_node_list, 
                            CLONE_ID_LIST = CLONE_ID_LIST,
                             GENERATIONS = GENERATIONS, 
                            N_SNAPSHOTS = N_SNAPSHOTS,
                             FNAME = FNAME, DIRECTORY = DIRECTORY, 
                            PICKLE_TITLE = pickle_title,
                             VISUALIZE = VISUALIZE)        

            # update hzrd amt for next sim
            hzrd_amt += H_INCREMENT

        # update rsrc amt, reset hzrd amt for next round of sims
        rsrc_amt += R_INCREMENT
        hzrd_amt = HZRD_RANGE[0]
        
def seeded_grid_search(SEED, N_SEEDS, # only these used here, rest are passed
                       RSRC_RANGE,
                       R_INCREMENT,
                       HZRD_RANGE,
                       H_INCREMENT,
                       CELL_LIST,
                       CLONE_ID_LIST,
                       W, H,
                       GENERATIONS,
                       N_SNAPSHOTS,
                       TITLE_PREFIX, # used here, and later
                       DIRECTORY,
                       PROGRESS_BAR=True,
                       VISUALIZE=False,
                       RSRC_IV=0,
                        NODE_LIST=[] # deprecated. unused argument
                        ): 
    '''wrapper around grid_search that puts-together a file-name,
        writes colnames to an output file, and runs grid_search for
        each seed'''
    sys.setrecursionlimit(10 * W * H)
    
    # constant colnames: changing requires new code calculating & file writing
    COLNAMES = ["clone", "mutRt", "meanDivRt", "varianceDivRt", "livePop", 
                "historicPop", "rA", "hA", "generations", "seed", 
                "nInitCell", "w", "h"]

    # create output file wih column names
    n_init_cell = len(CELL_LIST)
    output_filename = (TITLE_PREFIX + str(N_SEEDS) + "-seeds_" + 
        "rRange=" +  str(RSRC_RANGE) + "_hRange=" + str(HZRD_RANGE) + 
        "_hInc=" + str(H_INCREMENT) + "_rInc" + str(R_INCREMENT) + 
        "_nInitCell=" + str(n_init_cell) + "_w=" + str(W) + "_h=" + str(H) + 
        "_t=" + str(int(datetime.datetime.now().timestamp() / 60)) + 
        ".csv")
    write_colnames_to_file(filename = output_filename, 
                        colnames_list = COLNAMES, 
                        directory = DIRECTORY)
    
    # prepare to run many-times
    seed_list = stretch_seed(SEED, N_SEEDS)

    if PROGRESS_BAR:
        start_time = time.time()
        prev_time = time.time()

    for i in range(len(seed_list)):
        seed = seed_list[i]

        # report progress
        if PROGRESS_BAR:
            print("Progress: [" + ("=" * i) + ("." * (len(seed_list)-i)) + "]")
            print("Now running grid search for seed ", 
                    i+1, " out of ", len(seed_list))
            curr_time = time.time()
            print("Last search took ", curr_time - prev_time, " seconds.")
            prev_time = curr_time # update for next timing

        # set seeds
        np.random.seed(seed)
        rand.seed(seed)

        # run grid-search
        grid_search(SEED = seed, FNAME = output_filename,
                   RSRC_RANGE = RSRC_RANGE,
                   R_INCREMENT = R_INCREMENT,
                   HZRD_RANGE = HZRD_RANGE,
                   H_INCREMENT = H_INCREMENT,
                   CELL_LIST = CELL_LIST,
                   CLONE_ID_LIST = CLONE_ID_LIST,
                   N_INIT_CELL = n_init_cell,
                   W = W, H = H,
                   GENERATIONS = GENERATIONS,
                   N_SNAPSHOTS = N_SNAPSHOTS,
                   TITLE_PREFIX = TITLE_PREFIX,
                   DIRECTORY = DIRECTORY,
                   VISUALIZE = VISUALIZE,
                    RSRC_IV = RSRC_IV)

    print("done!")
    if PROGRESS_BAR:
        print("Total time: ", time.time() - start_time, " seconds.")
