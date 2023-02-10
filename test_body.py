#
## Tests: 
# init, display, place, remove, move, and adjacent_space calculations
#

## untested: update, is_empty

from Body import *

## init & display ##
b = Body(5,4)
print(b)

## place Xs ##
b.place_cell("x", 2,2)
print(b)
b.place_cell("x", 1,3)
print(b)

## remove Ys ##
b.remove_cell(1,3)
print(b)

## move Xs ##
b.move_cell(2,2,0,0)
print(b)

## adjacent spaces ##
print("next to 0,0: ", sep="")
print(b.adjacent_spaces(0,0))

print("next to 2,2: ", sep="")
print(b.adjacent_spaces(2,2))

print("next to 4,3: ", sep="")
print(b.adjacent_spaces(4,3))
