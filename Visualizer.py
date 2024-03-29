#
# Mar. 9: default to no gridlines, min cell size 1 pixel
# 

from tkinter import *

GRIDLINE_COLOR = "grey"
MIN_PIXEL_SIZE = 1

class Visualizer(Frame):
    LEFT = 8 # window margin, used to locate pixel corners in squareAt
    TOP = 8 # window margin "^"

    def __init__(self, columns=16, rows=16, body=None):
        # constants to play nice
        self.columns = columns
        self.rows = rows
        self.body = body
        self.set_dimensions() # sets self.width, self.height for window size

    def display(self, title, mode="Cell", verbose=False, gridlines=False):
        self.root = Tk() # tk object. toplevel/root window
        self.root.title(title) # title the pop-up window
        Frame.__init__(self, self.root) # some tk object?
        # canvas is some tk object
        self.canvas = Canvas(self.root, width=self.width+10, 
            height=self.height+10)
        self.canvas.pack() # critical for displaying
        self.root.bind('<Key>', self.keypress) # allows key-interactivity
        self.pack() # unsure what this does.
        
        # try to get it to display
        self.render(mode, verbose, gridlines)
        # self.after(10,self.tick) implement tick method
        self.mainloop()


    def set_dimensions(self):
        '''jimcopy. establishes self.size, which determines the size of pixels 
        as square boxes such that they can evenly fill the width and height 
        of the grid, within maxwidth and maxheight'''
        ## Note: max grid dimensions on my machine:
        ## minsize=4: window sizes to about 435 in width, 263 in height.
        ## minsize=1: window sizes to 1730 width, 1050 height max.
        minsize = MIN_PIXEL_SIZE
        maxsize = 32
        maxwidth = 1024 
        maxheight = 512
        # set pixelsize relative to windowsize/#pixels
        xsize = maxwidth // self.columns
        ysize = maxheight // self.rows
        size = min(xsize,ysize)
        # keep pixelsize in bounds
        if size < minsize:
          self.scrolls = True
          self.size = minsize
        elif size > maxsize:
          self.size = maxsize
          self.scrolls = False
        else:
          self.scrolls = False
          self.size = size
        self.width = self.columns * self.size
        self.height = self.rows * self.size

    def squareAt(self,row,column):
      """ Determines the coordinates of the corners of the given 
          cell's pixel.
      """

      # (upper left x, upper left y, 
      #  lower right x, lower right y)
      
      return (self.LEFT+column*self.size, self.TOP+row*self.size, \
              self.LEFT+(column+1)*self.size, self.TOP+(row+1)*self.size)

    def render(self, mode, verbose, gridlines):
        self.canvas.delete('all')
        if verbose:
            print("vis rows:" + str(self.rows))
            print("vis cols", self.columns)
        for r in range(self.rows):
            for c in range(self.columns):
                self.drawPixelAt(r,c, mode, gridlines=gridlines)


    def drawPixelAt(self,r,c, mode, edge=GRIDLINE_COLOR, gridlines=True):
        rect = self.squareAt(r,c)
        #value = self.get(r,c)
        value = (255,255,255) # default rgb to white
        if self.body != None:
            value = self.body.get_cell_color(c,r, mode)
        shade = self.shadeOf(value)
        if gridlines:
            self.canvas.create_rectangle(rect, fill=shade, outline=edge)
        else:
            self.canvas.create_rectangle(rect, fill=shade, outline=shade)

    def shadeOf(self,value_rgb):
        #if value == 0:
        #    return 'white'
        #else:
        #    return 'blue'
        return '#%02x%02x%02x' % value_rgb # Formats value_rgb as hexdigits

    #
    # keypress - react to a keypress
    #
    def keypress(self,event):
        """ Handles tkinter keyboard events. """

        # 'q' key exits this simulation
        if event.char == 'q':
            self.quit() # ends mainloop
            self.kill() # closes window
          

    def kill(self):
        #unsure if necessary
        self.root.destroy()
