#
#
## Feb. 4
#
#

## tests: init, create, deplete, get & display

# untested: update (which is just create)

from Hazard import *

rand.seed(123)

print("Init?")
obj = Hazard(5,5)
print(obj)

print("add hazards?")
obj.create_hazards()
print(obj)

print("remove 1 from 4,0?")
obj.deplete_hazards(1,4,0)
print(obj)

print("final value at 4,0: ")
print(obj.get_hazard_amount(4,0))

## seems to work!
