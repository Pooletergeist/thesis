#
#
## Jan. 30
#
#

from Resource import *

rand.seed(123)

obj = Resource(5,5)
obj
obj.distribute_few_resources(5,4)
print(obj)

bobj = Resource(3,3)
bobj.distribute_resources(2,1)
print(bobj)
bobj.deplete_resources(1,2,2)
print(bobj)

print(bobj.get_resource_amount(2,2))

## seems to work!
