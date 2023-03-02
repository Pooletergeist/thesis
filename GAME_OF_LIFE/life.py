from Grid import Grid, GREYS, COLORS
from rules import *

print('Hit [DELETE] to reset.')
print('Hit [SPACE] to step.')
print('Hit [RETURN] to run.')
print('Hit \'q\' to quit.')

Grid(conway)
# Grid(conway,pattern='patterns/rpentamino.pat')
# Grid(generational,pattern='patterns/rpentamino.pat')
# Grid(negative,pattern='images/reed-square.pgm')
# Grid(blur,pattern='images/reed.pgm')

# Below is an example of a demo of the given rules
# Uncomment and modify the demo to show your rules

"""

Grid(conway,
     '1. This runs a SE-traveling glider in Conway. The simulation runs long\
 enough to have the glider traverse the world.',
     pattern='patterns/glider.pat', generations=64)

Grid(generational,
     '2. This runs the R pentamino in generational Conway. Later cells will\
 be of advanced generations, and so will be colored further in the spectrum.',
     pattern='patterns/rpentamino.pat', generations=98)

Grid(blur,'3. This will blur an image.',
     pattern='images/reed.pgm')

Grid(negative,'4. This will form the negative of an image.',
     pattern='images/reed-square.pgm')

"""



