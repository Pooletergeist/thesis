#
## Apr. 12: meanDivRate
#

# WANT: Cells report to Tree, tracks every division, location etc.

class Tree:

    def __init__(self, root):
        self.root = root

    def __repr__(self):
        if self.root != None:
            string = "----TREE----\n"
            string += self.root.print_tree()
        else:
            string = "Empty"
        return string

class Node:
    
    def __init__(self, parent, born_location, cell=None):
        self.parent = parent
        self.born_location = born_location
        # filled later
        self.dead_location = None
        self.visited_locations = [born_location]
        self.children = []
        # dangerous pointer to cell
        self.cell_reference = cell

    def __eq__(self, other):
        '''two nodes are equal if all their fields are equal'''
        if isinstance(other, Node):
            return (self.parent == other.parent 
                    and self.born_location == other.born_location 
                    and self.dead_location == other.dead_location 
                    and self.visited_locations == other.visited_locations 
                    and self.children == other.children 
                    and self.cell_reference == other.cell_reference) 
        return False

    ### When things happen on the Grid: ###
    def track_division(self, my_location, child_location):
        '''make 2 nodes corresponding to the daughters of this division'''
        # make nodes for both children
        child0_node = Node(parent=self, born_location=child_location)
        child1_node = Node(parent=self, born_location=my_location)
        # add them to the tree
        self.children.append(child0_node)
        self.children.append(child1_node)
        return child0_node, child1_node

    def track_death(self, dead_location):
        # QUESTION? should this show up in visited locations?
        self.dead_location = dead_location

    def track_move(self, location):
        self.visited_locations.append(location)

    def set_cell_reference(self, cell):
        self.cell_reference = cell

    def set_born_location(self, location):
        self.born_location = location
        self.visited_locations[0] = location

    def add_child(self, cell): # only used in test rn
        self.children.append(cell)

    def color_subtree(self, color_rgb):
        if self.cell_reference != None:
            self.cell_reference.set_color(color_rgb)
        if self.children != []:
            for child in self.children:
                child.color_subtree(color_rgb)

    def count_subtree(self):
        if self.children == []:
            return 1
        else:
            # since only 2 children,
            return (1 + self.children[0].count_subtree() + 
                    self.children[1].count_subtree() - 1) # -1 since parent cell
            # disappears (becomes a daughter)

    def count_living_subtree(self):
        # is this cell living?
        if self.cell_reference != None and not self.cell_reference.dead:
            count_me_living = 1
        else:
            count_me_living = 0
        # then, how big is the subtree?
        if self.children == []:
            return count_me_living
        else:
            return (count_me_living + self.children[0].count_living_subtree() + 
                    self.children[1].count_living_subtree())

#######
# Mutation Stats 
#######

    def sum_subtree_div_rate(self):
        # is this cell living?
        if self.cell_reference != None and not self.cell_reference.dead:
            div_rate = self.div_rate
        else:
            div_rate = 0 # don't count if you're dead
        # then, how big is the subtree?
        if self.children == []:
            return div_rate
        else:
            return (div_rate + self.children[0].sum_subtree_div_rate() + 
                    self.children[1].sum_subtree_div_rate())

    def mean_subtree_div_rate(self, n_liveCells):
        return self.sum_subtree_div_rate() / n_liveCells
        
    def sum_variation_subtree_div_rate(self, mean):
        # calculate squared sum of differences with mean
        if self.cell_reference != None and not self.cell_reference.dead:
            diff = (self.div_rate - mean) ** 2
        else:
            diff = 0 # don't count if you're dead
        # then, how big is the subtree?
        if self.children == []:
            return diff 
        else:
            return (diff + self.children[0].sum_variance_subtree_div_rate() + 
                    self.children[1].sum_variance_subtree_div_rate())

    def subtree_div_rate_variance(self, n_liveCells):
        return self.sum_variance_subtree_div_rate() / n_liveCells
 

    ## display ##
    ## pretty print: vertical 
    # take the root, check all your children on same line, 
    # but they need to build subtrees...

    ## less pretty print: horizontal
    # level of indent indicates depth in tree
    # Given, indent. add self. if children, add them. return substring.
    def print_tree(self, indent = ""):
        print("called: " + str(self))
        string = indent + "0" + "\n" 
        if self.children == []:
            print("emptych : " + str(self))
            return string 
        else:
            print("haskids: " + str(self))
            indent += "\t"
            for child in self.children:
                string += child.print_tree(indent)
        return string 


    def list_ancestors(self, string = ""):
        ''' messy recursive ll traversal '''
        if self.parent == None:
            return string + str(self)
        else:
            # add parent
            string += self.parent.list_ancestors(string)
            # add self
            string += str(self)
            return string

    def check_living_children(self):
        '''helpful for debug'''
        if self.cell_reference != None:
            # we've got a cell on grid.
            return self.cell_reference.is_alive()
        else: 
            # we've got a parent.
            return (self.children[0].check_living_children() or self.children[1].check_living_children())
            
    def __repr__(self): 
        return str(self.visited_locations)
