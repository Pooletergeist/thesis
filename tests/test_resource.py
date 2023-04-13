#
#
## Feb. 4
#
#

# Tests: init, create, distribute, deplete, get & display

from Resource import *

rand.seed(123)

print("Init?")
obj = Resource(5,5)
print(obj)

print("add resources?")
obj.create_resources()
print(obj)

print("remove 1 from 4,0?")
obj.deplete_resources(1,4,0)
print(obj)

print("final value at 4,0: ")
print(obj.get_resource_amount(4,0))

## seems to work!
