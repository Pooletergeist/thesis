#
## Feb 7.
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

    def add_child(self, cell): # only used in test rn
        self.children.append(cell)

    def color_subtree(self, color_rgb):
        self.cell_reference.set_color(color_rgb)
        if self.children != []:
            for child in self.children:
                child.color_subtree(color_rgb)

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
            
    def __repr__(self): 
        return str(self.visited_locations)
