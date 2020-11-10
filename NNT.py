"""
I'm (Michael) using the PyCharm IDE to load in all the imports
I'm running it in debug mode in order to keep the image window open. Using breakpoints
Will need to add some wait for user input at some point
"""

import math
import random
from colorsys import hsv_to_rgb
from graphics import *
import numpy as np

gridWidth = 10
gridHeight = 10

#The origin is in the top-left, but I'm going to manipulate it so that doesn't matter
scale = 50
imageWidth = gridWidth*scale
imageHeight = gridHeight*scale


drawBefore = True
drawLines = True
#More draws to be added later


class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# Pulled from https://gist.github.com/Mause/4266179
def pretty_colors(how_many):
    """uses golden ratio to create pleasant/pretty colours
    returns in rgb form"""
    golden_ratio_conjugate = (1 + math.sqrt(5)) / 2
    hue = random.random()  # use random start value
    final_colours = []
    for tmp in range(how_many):
        hue += golden_ratio_conjugate * (tmp / (5 * random.random()))
        hue = hue % 1
        temp_c = [round(x * 256) for x in hsv_to_rgb(hue, 0.5, 0.95)]
        final_colours.append(color_rgb(tuple(temp_c)[0],tuple(temp_c)[1],tuple(temp_c)[2]))
    return final_colours

def sort(S):
    #S1 = np.zeros(len(S),2)
    for i in range(1,len(S)):
        j = i
        while S[j][0] < S[j-1][0] or (S[j][0] == S[j-1][0] and S[j][1] < S[j-1][1]):
            temp = S[j][0]
            S[j][0] = S[j-1][0]
            S[j-1][0] = temp
            j -= 1
            if j == 0:
                break
    return S

def NNTrans_min():
    #TODO maybe?
    return

def NNTrans_max():
    #TODO
    return

def generateLines(p, Y):
    #A line is defined as a two-tuple, (m,b), where m is the slope and b is the y-intercept
    #slope is 2x_i and intercept is 2y_i*Y - x_i^2 - y_i^2.
    #Y is our current row we are checking
    #TODO, creates input for DUE_Y
    linesY = []
    for pix in p:
        x = pix.x
        y = pix.y
        m = 2*x
        b = 2*y*Y - (x*x) - (y*y)
        linesY.append((m,b))

    return linesY

def DUE_Y(lines):
    upperTuplesArray = []
    for line in lines:
        break
    #TODO
    return upperTuplesArray

###-------------VISUALIZING METHODS---------------###
gridLineColor = 'gray50'

#Just makes the gridlines
def drawGridMethod():
    for i in range(1, gridWidth):
        gridLine = Line(Point(i*scale, 0), Point(i*scale, imageHeight))
        gridLine.setOutline(gridLineColor)
        gridLine.draw(win)
    for j in range(1, gridHeight):
        gridLine = Line(Point(0, j * scale), Point(imageWidth, j * scale))
        gridLine.setOutline(gridLineColor)
        gridLine.draw(win)

def clear():
    #win.delete("all")
    itemCount = reversed(range(len(win.items)))
    for item in itemCount:
        win.items[item].undraw()
    win.update()


def drawBeforeMethod(p):
    for pix in p:
        x = pix.x-1
        y = gridHeight-pix.y
        color = pix.color
        #print(color)
        pixelRectangle = Rectangle(Point(x*scale,y*scale), Point((x+1)*scale,(y+1)*scale))
        pixelRectangle.setOutline(gridLineColor)
        pixelRectangle.setFill(color)
        pixelRectangle.draw(win)


def drawLinesMethod(linesY):
    i = 0
    for line in linesY:
        m = line[0]
        b = line[1]
        color = pixels[i].color
        i += 1
        start = Point(0, (gridHeight-b)*scale)
        end = Point(imageWidth, ((gridHeight-b)*scale)+m*gridWidth)
        l = Line(start, end)
        l.setOutline(color)
        l.setWidth(scale/10)
        l.draw(win)




if __name__ == "__main__":

    #starting coords and sort them if the need it
    #We could add a check to make sure the pixels fit in our grid size (defined above), but this is just a POC so it'll be fine

    #TODO: THIS NEEDS FIXING, make sure that if x is the same then it is sorted by its y
    #coords = [[1,1],[2,1],[5,3],[4,7],[7,6],[4,6],[9,4]]
    #print(coords)
    #print(sort(coords))

    #Already sorted coords
    coords = [[1,1],[2,1],[4,6],[4,7],[5,3],[7,6],[9,4]]

    #Generate random colors (size of coords)
    colors = pretty_colors(len(coords))

    #Make each pixel with a color
    pixels = []
    for i in range(len(coords)):
        pixels.append(Pixel(coords[i][0], coords[i][1], colors[i]))

    #Create visual window
    win = GraphWin(width=imageWidth, height=imageHeight)
    drawGridMethod()
    if(drawBefore):
        drawBeforeMethod(pixels);



    for row in reversed(range(gridHeight)):
        linesY = generateLines(pixels, row)
        print(linesY)

        if(drawLines):
            clear()
            drawGridMethod()
            drawLinesMethod(linesY)

    print("Breakpoint here for now to stop the window from closing")
        
