#
# Feb. 7
#
## Tests:
# init, set_loc, update-die, update-move, update-move&die
#
# Mar 2: it takes a second...

from Cells import *
import random as rand

rand.seed(123)

## test init ##
print("Can we build it?")
c = Cell(0, 1, 0.9, 0.8, 0, 0, None)
print(c)

## test set_loc ##
print("Can we location-fiddle it?")
c.set_location(4,4)
print(c)

## test update die ##
print("Die?")
d = Cell(0,0,0,0,0,0,None)
print(d)
print(d.update([], 0, 1))
print(d)
print("===")

## test update move ##
print("Move?")
m = Cell(0,0,0,1,0,0,None)
print(m)
print(m.update([(1,1), (2,2)], resources = 0, hazards = 0))
print("---")

## test update divide ##
print("Divide?")
dv = Cell(0,1,0,0,0,0,None)
print(dv.update([(0,5)], resources = 1, hazards = 0))
print("+++")

## test update move & divide ##
print("Mov&Div?")
dv = Cell(0,1,0,1,0,0)
print(dv.update([(3,3)], resources = 1, hazards = 0))


