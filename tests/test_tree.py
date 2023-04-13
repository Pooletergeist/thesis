#
#
# Feb. 7 
#

from Tree import *

## init ##
print("init?")
progenitor = Node(parent = None, born_location = (0,0))
t = Tree(None)
print("display?")
print(t)
t = Tree(progenitor)
print(t)

## divide & display ##
print("divide?")
#leftchild = Node(parent = progenitor, born_location = (0,0))
#midchild = Node(parent = progenitor, born_location = (1,0))
#rightchild = Node(parent = progenitor, born_location = (2,0))
leftchild, prog = progenitor.track_division((0,0),(0,1))
midchild, prog = progenitor.track_division((0,0),(1,0))
rightchild, prog = progenitor.track_division((1,1),(2,0))
print(t)
#newmidkid = Node(parent=midchild, born_location = (3,3))
baby, prog = midchild.track_division((2,2),(3,3))
print(t)
print(midchild.children)

## move ##
print("move 1,0 to 1,1")
midchild.track_move((1,1))
print(t)

## die ## 
print("have 1,1 die at 1,2")
midchild.track_death((1,2))
print(midchild.dead_location)

## list ancestors ##
print("list ancestors for 3,3 -> (1,0/1,1) and (0,0)")
print(baby.list_ancestors())
