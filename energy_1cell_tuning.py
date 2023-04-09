#
## Apr 7.
#

# NOTE: pickles are saved as a triple (state, originator_nodes, originator_ids)
# for stats-ease from loading

import random as rand
import numpy as np

from UTILS import (stretch_seed, place_cells, make_new_nodes,
    make_file_path, write_colnames_to_file, append_str_to_file, 
    string_join, comma_join,
    save_pickle)

from energy_experiment_utils import (energy_model, make_untracked_energy_cells,
    connect_cells_and_roots)
    

from Visualizer import Visualizer # for debug
import copy # to copy cells

CELL_LIST, CLONE_ID_LIST, NODE_LIST = make_untracked_energy_cells(N=1) 

assert len(CLONE_ID_LIST) == len(CELL_LIST) # sanity-check for user code

def write_pop_counts_to_file(filename, sim_state, 
                            node_list, 
                            clone_id_list,
                            rAmt, hAmt,
                            gen, seed,
                            nInitCell,
                            W, H, 
                            directory=None):
    '''writes 1 line per clone to file, and 1 summary line'''
    shared_suffix = comma_join([rAmt, hAmt, gen, seed, nInitCell, W, H]) + "\n"

    total_live_pop = 0
    total_historic_pop = 0
    for clone_ix in range(len(node_list)):
        # get clone population
        live_pop = node_list[clone_ix].count_living_subtree()
        historic_pop = node_list[clone_ix].count_subtree()
        # add to totals
        total_live_pop += live_pop
        total_historic_pop += historic_pop
        # identify clone
        clone_name = clone_id_list[clone_ix][0]
        divRt = clone_id_list[clone_ix][1]
        movRt = clone_id_list[clone_ix][2]
        # make table line
        line = (comma_join([clone_name, live_pop, historic_pop, divRt, movRt]) +                 shared_suffix)
        # write line
        append_str_to_file(filename, line, directory)
    # write totals
    totals_line = (comma_join(["all", total_live_pop, total_historic_pop,
                                -1, -1]) + shared_suffix)
    append_str_to_file(filename, line, directory)


def run_and_record_simulation(W, H, rsrc_amt, hzrd_amt, 
                             nInitCell, seed, # already used, now just flags
                             this_cell_list, this_node_list, CLONE_ID_LIST,
                             GENERATIONS, N_SNAPSHOTS,
                             fname, DIRECTORY, pickle_title,
                             VISUALIZE):

    assert(len(this_cell_list) == len(this_node_list) == nInitCell)

    # build sim model
    sim_state = energy_model(W, H, rsrc_amt, hzrd_amt)
    place_cells(sim_state, this_cell_list, this_node_list)

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

        # save pickle triple: (sim_state, originator_nodes, originator_ids)
        save_pickle((pickle_title + str(generations_run)), 
                    (sim_state, this_node_list, CLONE_ID_LIST),
                    DIRECTORY)

        # write summary
        write_pop_counts_to_file(filename = fname, 
                        sim_state = sim_state, 
                        node_list = this_node_list, 
                        clone_id_list = CLONE_ID_LIST,
                        rAmt = rsrc_amt, hAmt = hzrd_amt,
                        gen = generations_run, seed=seed,
                        nInitCell=nInitCell,
                        W=W, H=H, 
                        directory=DIRECTORY)

    return sim_state



def grid_search(SEED, fname, # passsed
               RSRC_RANGE,  # used here
               R_INCREMENT, # used here
               HZRD_RANGE,  # used here
               H_INCREMENT, # used here
               CELL_LIST, # passed
               NODE_LIST, # passed
               CLONE_ID_LIST, # passed
               nInitCell, # passed
               W, H,
               GENERATIONS,
               N_SNAPSHOTS,
               TITLE_PREFIX, DIRECTORY,
               VISUALIZE): 

    assert(nInitCell == len(CELL_LIST)) 

    # grid search over rsrcs and hazards
    rsrc_amt = RSRC_RANGE[0]
    hzrd_amt = HZRD_RANGE[0]
    while rsrc_amt < RSRC_RANGE[1]:
        while hzrd_amt < HZRD_RANGE[1]:
        #
            pickle_title = (TITLE_PREFIX + "rAmt=" +  str(round(rsrc_amt,2)) +
                "_hAmt=" + str(round(hzrd_amt,2)) + 
                "_nInitCell=" + str(nInitCell) +
                "_hInc=" + str(H_INCREMENT) + "_rInc" + str(R_INCREMENT) +
                "_w=" + str(W) + "_h=" + str(H))  

            # copy fresh cell_list and make new empty nodes to track, 
            # so one sim does not affect the next
            this_cell_list = copy.deepcopy(CELL_LIST)
            this_node_list = make_new_nodes(len(CELL_LIST))
            # link together
            connect_cells_and_roots(this_cell_list, this_node_list)
    
            # Run Simulation
            run_and_record_simulation(W, H, rsrc_amt, hzrd_amt, 
                             nInitCell, SEED, # already used, now just flags
                             this_cell_list, this_node_list, CLONE_ID_LIST,
                             GENERATIONS, N_SNAPSHOTS,
                             fname, DIRECTORY, pickle_title,
                             VISUALIZE)        

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
                       NODE_LIST,
                       CLONE_ID_LIST,
                       W, H,
                       GENERATIONS,
                       N_SNAPSHOTS,
                       TITLE_PREFIX, # used here, and later
                       DIRECTORY,
                       PROGRESS_BAR=True,
                       VISUALIZE=False):
    '''wrapper around grid_search that puts-together a file-name,
        writes colnames to an output file, and runs grid_search for
        each seed'''
    
    # constant colnames: changing requires new code calculating & file writing
    COLNAMES = ["clone", "livePop", "historicPop", "divRt", "movRt", 
                "rA", "hA", "generations", "seed", "nInitCell", "w", "h"]

    # create output file wih column names
    nInitCell = len(CELL_LIST)
    output_filename = (TITLE_PREFIX + str(N_SEEDS) + "-seeds_" + 
        "rRange=" +  str(RSRC_RANGE) + "_hRange=" + str(HZRD_RANGE) + 
        "_hInc=" + str(H_INCREMENT) + "_rInc" + str(R_INCREMENT) + 
        "_nInitCell=" + str(nInitCell) + "_w=" + str(W) + "_h=" + str(H) + 
        ".csv")
    write_colnames_to_file(output_filename, COLNAMES, DIRECTORY)
    
    # prepare to run many-times
    seed_list = stretch_seed(SEED, N_SEEDS)

    for i in range(len(seed_list)):
        seed = seed_list[i]

        # report progress
        if PROGRESS_BAR:
            print("Progress: [" + ("=" * i) + ("." * (len(seed_list)-i)) + "]")
            print(("Now running grid search for seed ", 
                    i+1, " out of ", len(seed_list+1)))

        # set seeds
        np.random.seed(seed)
        rand.seed(seed)

        # run grid-search
        grid_search(SEED = seed, fname = output_filename,
                   RSRC_RANGE = RSRC_RANGE,
                   R_INCREMENT=R_INCREMENT,
                   HZRD_RANGE=HZRD_RANGE,
                   H_INCREMENT=H_INCREMENT,
                   CELL_LIST=CELL_LIST,
                   NODE_LIST=NODE_LIST,
                   CLONE_ID_LIST=CLONE_ID_LIST,
                   nInitCell=nInitCell,
                   W=W, H=H,
                   GENERATIONS=GENERATIONS,
                   N_SNAPSHOTS=N_SNAPSHOTS,
                   TITLE_PREFIX=TITLE_PREFIX,
                   DIRECTORY=DIRECTORY,
                   VISUALIZE=VISUALIZE)

    print("done!")
