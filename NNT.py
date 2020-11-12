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

gridWidth = 5
gridHeight = 7

#The origin is in the top-left, but I'm going to manipulate it so that doesn't matter
scale = 50
imageWidth = gridWidth*scale
imageHeight = gridHeight*scale


drawBefore = True
drawLines = False
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

#Insertion sort, from https://www.geeksforgeeks.org/insertion-sort/
#Sorts by X value (S[i][0]), with Y value as tiebreaker (S[i][1]).
def sort(S):
    for i in range(1, len(S)):
        key = S[i]
        j = i - 1
        while j >= 0 and (key[0] < S[j][0] or (key[0] == S[j][0] and key[1] < S[j][1])):
            S[j+1] = S[j]
            j -= 1
        S[j+1] = key


def NNTrans_max(p, Y):
    return generateLines(p, Y)

#For parallel lines only take the one with the highest intercept
#O(2n) time, could make it O(n), but eh don't want to
def removeDuplicateSlopes(lines):
    i = 0
    deletes = []
    #Runs in O(n) time
    while i < len(lines):
        j = i+1
        largest = lines[i]
        while j < len(lines):
            if lines[i][0] == lines[j][0]:
                if lines[j][1]>lines[i][1]:
                    deletes.append(i)
                else:
                    deletes.append(j)
                j += 1
            else:
                break
        i=j

    #Probably could do this in the last loop, but python's dynamic arrays can be weird on deletes
    #Again O(n) time
    for k in reversed(deletes):
        lines.pop(k)

    return lines

def generateLines(p, Y):
    #A line is defined as a two-tuple, (m,b), where m is the slope and b is the y-intercept
    #slope is 2x_i and intercept is 2y_i*Y - x_i^2 - y_i^2.
    #Y is our current row we are checking
    i=1
    linesY = []
    for pix in p:
        x = pix.x
        y = pix.y
        m = 2*x
        b = 2*y*Y - (x*x) - (y*y)
        #The third element may not be necessary, but it keeps the lines with memory
        linesY.append((m,b,i))
        i += 1

    return removeDuplicateSlopes(linesY)

###-------------Discrete Upper Envelope Algorithms-------------###
#Not sure if implementing them all is necessary. We'll see

#O(U) degree 3
#I think I need to implement Orientation and not Intersect, but I do not understand orientation
def D3_DUE():
    def Intersect(l, h):
        x = (h[1]-l[1])/(l[0]-h[0])
        y = (l[0]*h[1]-l[1]*h[0])/(l[0]-h[0])
        return (x, y)
    def Orientation(a, b, c):
        #TODO
        pass
    #TODO
    pass

#O(UlogU) degree 2
def UlgU_DUE():
    def IntersectCol(l, h):
        x = (h[1] - l[1]) / (l[0] - h[0])
        #y = (l[0] * h[1] - l[1] * h[0]) / (l[0] - h[0])
        return x
    #TODO
    pass

#O(U) degree 2, slower average time than D3_DUE
def U_DUE():
    #TODO
    pass

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


#Currently do not know how to make this work, asking the author
def drawLinesMethod(linesY):

    for line in linesY:
        m = line[0]
        b = line[1]
        color = pixels[line[3]].color

        start = Point(0, ((gridHeight-b)*scale))
        end = Point(imageWidth, (((gridHeight-b)*scale)+m*gridWidth))
        l = Line(start, end)
        l.setOutline(color)
        l.setWidth(scale/10)
        l.draw(win)




if __name__ == "__main__":

    #starting coords and sort them if the need it
    #We could add a check to make sure the pixels fit in our grid size (defined above), but this is just a POC so it'll be fine

    coords = [[1,1],[2,1],[5,3],[4,7],[7,6],[4,6],[9,4]]
    #print("Coords: (orig)")
    #print(coords)
    #print("Coords: (sorted)")
    sort(coords)
    #print(coords)

    #Already sorted coords
    #coords = [[1,7],[2,4],[3,7],[4,5]]

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



    for row in reversed(range(1,gridHeight+1)):
        linesY = generateLines(pixels, row)
        print(linesY)

        if(drawLines):
            clear()
            drawGridMethod()
            drawLinesMethod(linesY)

    print("Breakpoint here for now to stop the window from closing")

    for i in range(1,6):
        print("s1: " + (str)(2*i+48) + " s2: " + (str)(4*i+36) + " s3 : " + (str)(6*i+40) + " s4: " + (str)(8*i+29))
