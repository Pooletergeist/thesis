#
#
## Mar. 13
#
#

# Tests: init, create, distribute, deplete, get & display

from Density_Hazard import Hazard
from Body import Body

import random as rand
import numpy as np

rand.seed(123)
np.random.seed(123)

print("Init?")
b = Body(5,5)
obj = Hazard(5,5)
obj.body=b
print(obj)

print("add hazards?")
obj.update()
print(obj)

print("remove 1 from 4,0?")
obj.deplete_hazards(1,4,0)
print(obj)

print("final value at 4,0: ")
print(obj.get_hazard_amount(4,0))

