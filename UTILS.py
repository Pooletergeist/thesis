#
## Apr. 6
# 
# the goal of this module is to collect model-indifferent useful functions 
# for initializing a simulation into 1 maintainable version.
# it contains functions from TUNING_UTILS, experiment_utils, and build_null

############################
## Constructing Simulation #
############################

import random as rand
def stretch_seed(seed, n_seeds):
    '''returns list of n_seeds-many random integers to use as seeds'''
    rand.seed(seed)
    seeds = []
    for i in range(n_seeds):
        seeds.append(rand.randint(0,10**6))
    return seeds

from Tree import Node
def make_new_nodes(number):
    '''returns list of number-many new tree nodes'''
    nodes = []
    for i in range(number):
        nodes.append(Node(parent=None, born_location=(None,None), cell=None))
    return nodes

import math
def place_cells(body, cells, nodes, frac_of_grid=0.4):
    '''place cells in square, spaced, so they take ~ frac_of_grid'''
    assert(len(cells) == len(nodes))

    n_cells_in_line = math.sqrt(len(cells))
    spacing_intra_line = round((frac_of_grid * body.height) // n_cells_in_line)
    midX = body.width//2
    midY = body.height//2

    initX = midX - round(spacing_intra_line * (n_cells_in_line//2))
    initY = midY - round(spacing_intra_line * (n_cells_in_line//2))

    x = initX
    y = initY
    placed_in_line = 0
    for i in range(len(cells)):
        # print("placing: ", x,",",y)
        cell = cells[i]
        # update position
        cell.set_location(x,y)
        # update tree node position
        cell.tree_node.set_born_location((x,y))

        # place
        body.place_cell(cell, x, y)
        placed_in_line += 1
       
        # set-up next spacing
        x += spacing_intra_line
        # new row after n_cells_in_line
        if placed_in_line >= n_cells_in_line:
            x = initX
            y += spacing_intra_line
            placed_in_line = 0
 
        # ensure nodes correspond to cells properly
        assert(cells[i].tree_node == nodes[i]) 
        assert(nodes[i].cell_reference == cells[i])

#####################
## Analyzing Result #
#####################

def almost_cbrt(x):
    '''rtrns smallest integer such that integer^3 < x'''
    guess = 1
    while guess ** 3 < x:
        guess += 1
    return guess

def count_cells(matrix):
    '''returns number of none-None elements in list of lists'''
    n_cells = 0
    for col in range(len(matrix)):
        for row in range(len(matrix[0])):
            if matrix[row][col] != None:
               n_cells += 1 
    return n_cells

def more_than_x(matrix, fraction):
    '''returns (n, bool): n is # non-None elements. bool is whether that 
        number is greater than fraction of total elements in square matrix'''
    n = count_cells(matrix)
    if n / (len(matrix) * len(matrix)) >= fraction:
        return (n, True)
    else:
        return (n, False)

def color_subtrees(cell_list, debug=False):
    '''given a list of cell nodes to color, assign different rgb's sensibly'''
    # how-to break/sanitize this?
    n_cells = len(cell_list)
    gap = 150 // almost_cbrt(n_cells)
    red = 50
    blue = 50
    green = 50
    # color with colors
    for cell_node in cell_list:
        if debug:
            print(red,blue,green, "exp-util coloring_subtrees")
        cell_node.color_subtree((red,blue,green))
        red += gap
        if green >= 200:
            raise Exception("green too high")
        if blue >= 200 and red >= 200:
            green += gap
            red = 50
            blue = 50
        elif red >= 200:
            blue += gap
            red = 50

def uncolor_subtrees(cells):
    '''turns cells and descendants black'''
    for cell in cells:
        cell.color_subtree(0,0,0)

def count_living_subtrees(cell_node_list):
    '''given a list of cell nodes, return list of counts of still-live cells'''
    counts = [0] * len(cell_node_list)
    i = 0
    for cell_node in cell_node_list:
        counts[i] = cell_node.count_living_subtree()
        i += 1 
    return counts

##################################
## Summarizing Result As String ##
##################################

def gather_trial_data(matrix, threshold, colnames_list, variable_dict, 
                        tree_node_list = []):
    '''records cell_count and variables from dict into comma-separated str'''
    ## analyze final matrix state, add to dict
        # => enables 'n_cells' and 'moreThan0.y' as colnames
    n_cells, bigger_than_fraction = more_than_x(matrix, threshold)
    variable_dict["nCells"] = n_cells
    variable_dict["moreThan" + str(threshold)] = bigger_than_fraction
    if tree_node_list != []:
        ## add multicell info!
        for i in range(len(tree_node_list)):
            progenitor = tree_node_list[i]
            p = progenitor.count_living_subtree()
            variable_dict["clone"+str(i)+"Pop"] = p
    ## write to string from dict according to colnames
    trial_data = ""
    for colname in colnames_list:
        try:
            assert(colname in variable_dict)
            trial_data += str(variable_dict[colname]) + ", "
        except:
            trial_data += "data-for-colname-not-present" + ", "
    return trial_data + "\n" # end the line!

#############################
## Writing Result to Files ##
#############################

import os
def make_file_path(filename, directory):
    '''requires os, makes & returns path to file through directory'''
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    return file_path

def append_str_to_file(filename, string, directory=None):
    '''procedure appending string string to file'''
    if directory != None:
        file_path = make_file_path(filename, directory)
    else:
        file_path = filename
    # write to file
    with open(file_path, "a") as f:
        f.write(string)

def write_colnames_to_file(filename, colnames_list, directory=None):
    '''csv firstline as colnames'''
    if directory != None:
        file_path = make_file_path(filename, directory)
    else:
        file_path = filename
    # write to file
    line = ""
    for colname in colnames_list:
        line += colname + ", "
    line += "\n"
    with open(file_path, "w") as f:
        f.write(line) 

import pickle
def save_pickle(filename, data, directory=None):
    '''pickle wrapper with optional directory'''
    if directory != None:
        file_path = make_file_path(filename, directory+"/pickles")
    else:
        file_path = filename
    with open(file_path + ".pkl", "wb") as f:
        pickle.dump(data, f)

def string_join(string_list, splicer):
    '''join a list of stuff by "splicer", with str() conversions'''
    new = ""
    for s in string_list:
        new += str(s) + splicer
    return new 

def comma_join(string_list):
    '''join a list of stuff by ", ", with str() conversions'''
    return string_join(string_list, ", ")
