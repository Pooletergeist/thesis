#
#
## Mar. 13
#
#

# Tests: init, create, distribute, deplete, get & display

from Density_Resource import Resource
from Body import Body

import random as rand
import numpy as np

rand.seed(123)
np.random.seed(123)

print("Init?")
b = Body(5,5)
obj = Resource(5,5)
obj.body=b
print(obj)

print("add resources?")
obj.update()
print(obj)

print("remove 1 from 4,0?")
obj.deplete_resources(1,4,0)
print(obj)

print("final value at 4,0: ")
print(obj.get_resource_amount(4,0))

