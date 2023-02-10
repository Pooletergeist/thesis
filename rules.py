from random import random 

# * * * * * * * * * * * conway * * * * * * * * * * *
#
# Example of a grid rule. This rule gets applied to
# each grid cell, inspecting its state and the states
# of its eight neighbor cells, and is used to determine
# its next state.
#
# This particular rule encodes the behavior of Conway's 
# game of life simulation.  It takes two parameters:
#
#   cntr: the state of the grid cell being inspected
#
#   nbrs: collection of states of the 8 grid neighbors 
#         that sit around the cell being inspected
#
# This rule interprets states of 0 as "dead" and
# states of 1 and above as being "alive". 
#
# Live cells die if they have too many or too many
# living neighbors.
#
# Dead cells come alive if they have just the 
# right number of live neighbors.
#
# See the if/else below for details.
#
def conway(cntr,nbrs):

  # live
  #
  # Helper function that returns 1/0 if live/dead.
  def life(cell_value):
    if cell_value > 0:
      return 1
    else:
      return 0

  #
  # count the number of living neighbors  
  #
  living = life(nbrs.NW) + life(nbrs.N) + life(nbrs.NE) \
           + life(nbrs.W) + life(nbrs.E) \
           + life(nbrs.SW) + life(nbrs.S) + life(nbrs.SE)

  #
  # determine next state
  #
  # if alive...
  if life(cntr) == 1:
    # and there are two or three live neighbors...
    if living == 2 or living == 3:
      # survive
      return cntr
    else:
      # otherwise, die.
      return 0
  #
  # if dead...
  else:
    # but there are three live neighbors...
    if living == 3:
      # come alive.
      return 100
    else:
      return 0
#
#
# * * * * * * * * * * * conway * * * * * * * * * * *



# * * * * * * * * * generational * * * * * * * * * * *
#
# This performs Conway's game of life except, when a
# cell is alive (1-100), its value is interpreted as
# its "generation".  This means that, when a live cell
# is born, it takes on the value that's one more than 
# the max value of its live neighbors.
#
def generational(cntr,nbrs):

  # live
  #
  # Helper function that returns 1/0 if live/dead.
  def life(cell_value):
    if cell_value > 0:
      return 1
    else:
      return 0

  #
  # count the number of living neighbors  
  #
  living = life(nbrs.NW) + life(nbrs.N) + life(nbrs.NE) \
           + life(nbrs.W) + life(nbrs.E) \
           + life(nbrs.SW) + life(nbrs.S) + life(nbrs.SE)

  largest = max(nbrs.NW,nbrs.N,nbrs.NE,nbrs.W,
                nbrs.SE,nbrs.S,nbrs.SW,nbrs.E)
  #
  # determine next state
  #
  # if alive...
  if life(cntr) == 1:
    # and there are two or three live neighbors...
    if living == 2 or living == 3:
      # survive
      return cntr
    else:
      # otherwise, die.
      return 0
  #
  # if dead...
  else:
    # but there are three live neighbors...
    if living == 3:
      # come alive, marking your new generation
      return 1+largest
    else:
      return 0
#
#
# * * * * * * * * * generational * * * * * * * * * * *

# * * * * * * * * * * * blur * * * * * * * * * * * * * 
#
# Example of an image processing rule.  This blurs an
# image.  A cell becomes the average of itself with
# the average value of its neighbors.  This "blends"
# greys and "smooths" out sharp transitions.  The 
# effect of a bright pixel is spread over an area
# of the image, centered at that pixel.

def blur(cntr,nbrs):

  # compute the average value of my neighbors
  avg = (nbrs.N + nbrs.E + nbrs.S + nbrs.W)//4

  # change state so that I'm closer to their average
  return (cntr + avg) // 2

#
#              
# * * * * * * * * * * * blur * * * * * * * * * * * * * 

# * * * * * * * * * * negative * * * * * * * * * * * * 
#
# This inverts brightness to darkness, and vice versa,
# in an image.  The effect makes the image look like 
# a photographic negative.
#
def negative(cntr,nbrs):
   return 255 - cntr
#
#
# * * * * * * * * * * negative * * * * * * * * * * * * 



'''
============================================================
'''
# * * * * * * * * * * * Age * * * * * * * * * * * 

def age(cntr,nbrs):
    # age with every step
    if cntr == 100:
        return 0
    else:
        return cntr + 1

# * * * * * * * * * * * decay * * * * * * * * * * * 

def decay(cntr,nbrs):
  # live cells white
  #
  # Helper function that returns 1/0 if live/dead.
  def life(cell_value):
    if cell_value == 100:
      return 1
    else:
      return 0

  #
  # count the number of living neighbors  
  #
  living = life(nbrs.NW) + life(nbrs.N) + life(nbrs.NE) \
           + life(nbrs.W) + life(nbrs.E) \
           + life(nbrs.SW) + life(nbrs.S) + life(nbrs.SE)

  #
  # determine next state
  #
  # if alive...
  if life(cntr) == 1:
    # and there are two or three live neighbors...
    if living == 2 or living == 3:
      # survive
      return cntr
    else:
      # otherwise, die (starting decay)
      return cntr - 1
  #
  # if dead...
  else:
    # but there are three live neighbors...
    if living == 3:
      # come alive.
      return 100
    elif cntr >= 1:
      # decay
        return cntr-20
    else:
      # already decayed
      return 0

# * * * * * * * * * * sandpile * * * * * * * * * * * * 

def sandpile(cntr,nbrs):

    def willFire(cell_value):
        if cell_value >= 4:
            return True
        else:
            return False
    
    if willFire(cntr):
    # firing self
        cntr -= 4

    # increasing?
    if willFire(nbrs.N):
        cntr += 1
    if willFire(nbrs.W):
        cntr += 1
    if willFire(nbrs.S):
        cntr += 1
    if willFire(nbrs.E):
        cntr += 1 

    return cntr
'''
# with class stuff
    # helper Fire
    def fire(cntr, nbrs):
        nbrs.N += 1
        nbrs.W += 1
        nbrs.E += 1
        nbrs.S += 1

    if cntr >= 4:
        fire(cntr,nbrs)
        return cntr - 4
'''



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

# * * * * * * * * * * contrast * * * * * * * * * * * * 

def contrast(cntr, nbrs):
    if cntr > 126:
        return cntr+30
    elif cntr < 126:
        return cntr-30
    else:
        return cntr

# * * * * * * * * * * sharpen * * * * * * * * * * * * 

def sharpen(cntr, nbrs):
  # compute the average value of my neighbors
  avg = (nbrs.N + nbrs.E + nbrs.S + nbrs.W)//4

  # change state so that I'm farther from their average
  if cntr > avg:
    cntr = cntr+20
  elif cntr < avg:
    cntr = cntr-20
  return cntr

# * * * * * * * * * * edges * * * * * * * * * * * * 

def edges(cntr, nbrs):
    # if nbrs are on either side of grey, go white.
    # else turn black.

    # Or, turn color based on difference side-side.
            # more advanced would be pairwise.
            # simpler would be cntr vs average around it.

    def difference(nbr1, nbr2):
        return abs(nbr1-nbr2)

    color = 0
    # calculate opposing pixel differences
    color += difference(nbrs.N, nbrs.S)
    color += difference(nbrs.E, nbrs.W)
    color += difference(nbrs.NE, nbrs.SW)
    color += difference(nbrs.NE, nbrs.SW)
    return color


#######################################################

# * * * * * * * * * * fill-in * * * * * * * * * * * * 

def fill(cntr, nbrs):
    # can I do with fewer ifs?
    if cntr == 100:
        if nbrs.N != 0 and nbrs.N != 100:
            cntr = nbrs.N
        if nbrs.S != 0 and nbrs.S != 100:
            cntr = nbrs.S
        if nbrs.E != 0 and nbrs.E != 100:
            cntr = nbrs.E
        if nbrs.W != 0 and nbrs.W != 100:
            cntr = nbrs.W
        if nbrs.NE != 0 and nbrs.NE != 100:
            cntr = nbrs.NE
        if nbrs.NW != 0 and nbrs.NW != 100:
            cntr = nbrs.NW
        if nbrs.SE != 0 and nbrs.SE != 100:
            cntr = nbrs.SE
        if nbrs.SW != 0 and nbrs.SW != 100:
            cntr = nbrs.SW
    return cntr

# * * * * * * * * * * enshadow * * * * * * * * * * * * 

def enshadow(cntr,nbrs):
    
    if cntr == 0:
        if nbrs.NW == 100:
            cntr = 50

    return cntr

# * * * * * * * * * * rectange * * * * * * * * * * * * 

def rectangle(cntr, nbrs):
    
    if nbrs.SE == 100 or nbrs.SW == 100 or nbrs.NW == 100 or nbrs.NE == 100:
        cntr += 50
    return cntr



