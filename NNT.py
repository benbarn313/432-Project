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

# The origin is in the top-left, but I'm going to manipulate it so that doesn't matter
scale = 50
imageWidth = gridWidth * scale
imageHeight = gridHeight * scale

drawBefore = True
drawLines = False
drawNonSites = True


# More draws to be added later


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
        final_colours.append(color_rgb(tuple(temp_c)[0], tuple(temp_c)[1], tuple(temp_c)[2]))
    return final_colours


# Insertion sort, from https://www.geeksforgeeks.org/insertion-sort/
# Sorts by X value (S[i][0]), with Y value as tiebreaker (S[i][1]).
def sort(S):
    for i in range(1, len(S)):
        key = S[i]
        j = i - 1
        while j >= 0 and (key[0] < S[j][0] or (key[0] == S[j][0] and key[1] < S[j][1])):
            S[j + 1] = S[j]
            j -= 1
        S[j + 1] = key


def NNTrans_max(p, Y):
    return generateLines(p, Y)


# For parallel lines only take the one with the highest intercept
# O(2n) time, could make it O(n), but eh don't want to
def removeDuplicateSlopes(lines):
    i = 0
    deletes = []
    # Runs in O(n) time
    while i < len(lines):
        j = i + 1
        # largest = lines[i]
        while j < len(lines):
            if lines[i][0] == lines[j][0]:
                if lines[j][1] > lines[i][1]:
                    deletes.append(i)
                else:
                    deletes.append(j)
                j += 1
            else:
                break
        i = j

    # Probably could do this in the last loop, but python's dynamic arrays can be weird on deletes
    # Again O(n) time
    for k in reversed(deletes):
        lines.pop(k)

    return lines


def generateLines(p, Y):
    # A line is defined as a two-tuple, (m,b), where m is the slope and b is the y-intercept
    # slope is 2x_i and intercept is 2y_i*Y - x_i^2 - y_i^2.
    # Y is our current row we are checking
    i = 1
    linesY = []
    for pix in p:
        x = pix.x
        y = pix.y
        m = 2 * x
        b = 2 * y * Y - (x * x) - (y * y)
        # The third element may not be necessary, but it keeps the lines with memory
        linesY.append((m, b, i))
        i += 1

    return removeDuplicateSlopes(linesY)


# ##-------------Discrete Upper Envelope Algorithms-------------###

# O(U) degree 3
# This takes the set of lines of form y = mx + b and creates a set of points (m, -b), then finds
# the convex hull of that set, then finds the lower hull from that. The lower point is equivalent
# to the DUE.


def D3_DUE(lines):

    ## #-----------DEFINITIONS-----------# ##
    
    # orientation takes the determinant of a 3x3 matrix whose left column is all 1s,
    # whose middle column is ax, bx, cx, and whose right column is ay, by, cy.
    # Return changes depending on position of c in relation to directed line from a to b:
    # If c is to the right, returns positive.
    # If c to the left, returns negative.
    # If c is colinear, returns 0.
    def orientation(a, b, c):
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        cx = c[0]
        cy = c[1]
        return (by-ay)*(cx-bx)-(bx-ax)*(cy-by)
    
    # From https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaDequeinPython.html
    class Deque:
        def __init__(self):
            self.items = []
        def isEmpty(self):
            return self.items == []
        def addFront(self, item):
            self.items.append(item)
        def addRear(self, item):
            self.items.insert(0,item)
        def removeFront(self):
            return self.items.pop()
        def removeRear(self):
            return self.items.pop(0)
        def size(self):
            return len(self.items)
        # I added these methods; peekFront2() returns the item below the top,
        # and peekBottom2 returns the item above the bottom.
        def peekFront(self):
            return self.items[len(self.items)-1]
        def peekRear(self):
            return self.items[0]
        def peekFront2(self):
            return self.items[len(self.items)-2]
        def peekRear2(self):
            return self.items[1]

    # This sorts a list of 2-tuples by their first entry, and is used here to sort the points
    # generated from the list of lines by their slopes (which are now the x coordinates).
    def sortBySlope(points):
        for i in range(1, len(points)):
            key = points[i]
            j = i - 1
            while j >= 0 and key[0] < points[j][0]:
                points[j + 1] = points[j]
                j -= 1
            points[j + 1] = key

    # This formats the lines from the form (m, b, id) to ((m, b), id)
    # Because I messed up the formatting and don't want to go through and redo all of it
    def formatLines(lines):
        newLines = []
        for line in lines:
            newLines.append([(line[0], -1*line[1]), line[2]])
        return newLines

    # Finds the convex hull of a set of points (the polygon with the fewest vertices where all points in the set are within the polygon)       
    def convexHull(points):
        #is the list of points enough to make a polygon?
        if (len(points) < 3):
            return points
        deque = Deque()
        #is the third point to the left of the line from the first to the second?
        if (orientation(points[0][0], points[1][0], points[2][0]) > 0):
            #left
            deque.addFront(points[0])
            deque.addFront(points[1])
        else:
            #right
            deque.addFront(points[1])
            deque.addFront(points[0])
        deque.addFront(points[2])
        deque.addRear(points[2])
        
        for i in range(2, len(points)):
            if ((orientation(points[i][0], deque.peekRear()[0], deque.peekRear2()[0]) < 0) or (orientation(deque.peekFront2()[0], deque.peekFront()[0], points[i][0]) < 0)):
                while orientation(deque.peekFront2()[0], deque.peekFront()[0], points[i][0]) <= 0:
                    deque.removeFront()
                deque.addFront(points[i])
                while orientation(points[i][0], deque.peekRear()[0], deque.peekRear2()[0]) <= 0:
                    deque.removeRear()
                deque.addRear(points[i])        
        
        hull = []
        while (not deque.isEmpty()):
            hull.append(deque.removeRear())
        hull.pop() #due to how hull is constructed, the first and last elements will be duplicates.
        return hull

    # Finds the lower hull of a convex hull (all points in the hull lower than the line from the left extreme to the right extreme)
    def lowerConvexHull(hull):
        lowerHull = []
        leftmost = ((float('inf'), None), None)
        rightmost = ((float('-inf'), None), None)
        for point in hull:
            if point[0][0] < leftmost[0][0] or (point[0][0] == leftmost[0][0] and point[0][1] < leftmost[0][1]):
                leftmost = point
            if point[0][0] > rightmost[0][0] or (point[0][0] == rightmost[0][0] and point[0][1] < rightmost[0][1]):
                rightmost = point
        for point in hull:
            if orientation(leftmost[0], rightmost[0], point[0]) >= 0:
                lowerHull.append(point)
        return lowerHull

    ## #-----------IMPLEMENTATION-----------# ##
    lines = formatLines(lines)
    sortBySlope(lines)
    print("Lines:", lines)
    hull = convexHull(lines)
    print("hull", hull)
    lowerHull = lowerConvexHull(hull)
    return lowerHull

    #TODO: this needs to return in the same format as UlgU_DUE.
    #TODO: don't know how to transition from this format to UglU's.
    #TODO: this seems to work in the way described by the paper, but output is not identical to UglU's.

    
# O(UlogU) degree 2
def UlgU_DUE(lines):
    def IntersectCol(l, h):
        x = (h[1] - l[1]) / (l[0] - h[0])
        # y = (l[0] * h[1] - l[1] * h[0]) / (l[0] - h[0])
        return x

    def Above(l, h, x):
        a = l[0] * x + l[1]
        b = h[0] * x + h[1]
        return a > b

    computedTuples = []

    # For the first x-coord, get the highest line:
    currentTop = lines[0][2]
    for line in lines[1:]:

        if Above(line, lines[currentTop - 1], 1):
            currentTop = line[2]

    # Create the DUE
    startingIntersect = 1
    while startingIntersect < gridWidth:
        currentIntersect = gridWidth
        newTop = None
        for line in lines[currentTop:]:
            intersection = IntersectCol(lines[currentTop - 1], line)
            if intersection <= gridWidth and intersection <= currentIntersect:
                currentIntersect = intersection
                newTop = line[2]
        computedTuples.append((currentTop, startingIntersect, currentIntersect))
        currentTop = newTop
        startingIntersect = currentIntersect

    return computedTuples

# ##-------------VISUALIZING METHODS---------------###
gridLineColor = 'gray50'


# Just makes the gridlines
def drawGridMethod():
    for i in range(1, gridWidth):
        gridLine = Line(Point(i * scale, 0), Point(i * scale, imageHeight))
        gridLine.setOutline(gridLineColor)
        gridLine.draw(win)
    for j in range(1, gridHeight):
        gridLine = Line(Point(0, j * scale), Point(imageWidth, j * scale))
        gridLine.setOutline(gridLineColor)
        gridLine.draw(win)


def clear():
    # win.delete("all")
    itemCount = reversed(range(len(win.items)))
    for item in itemCount:
        win.items[item].undraw()
    win.update()


# Draw in our sites
def drawBeforeMethod(p):
    for pix in p:
        x = pix.x - 1
        y = gridHeight - pix.y
        color = pix.color
        # print(color)
        pixelRectangle = Rectangle(Point(x * scale, y * scale), Point((x + 1) * scale, (y + 1) * scale))
        pixelRectangle.setOutline(gridLineColor)
        pixelRectangle.setFill(color)
        pixelRectangle.draw(win)


# Currently do not know how to make this work, asking the author
def drawLinesMethod(linesY):
    for line in linesY:
        m = line[0]
        b = line[1]
        color = pixels[line[2] - 1].color

        start = Point(0, (int)(b))
        end = Point(imageWidth, (int)((b) + m * (gridWidth * scale)))
        l = Line(start, end)
        l.setOutline(color)
        l.setWidth(scale / 10)
        l.draw(win)


# Draw in the nearest neighbors
def drawNonSitesMethod(due, row):
    # To differentiate between sites and nonsites
    offset = scale / 5
    y = gridHeight-row
    for section in due:
        color = pixels[section[0]-1].color
        for i in range(round(section[1]),round(section[2])+1):
            x = i-1
            topLeft = Point(x * scale + offset, y * scale + offset)
            bottomRight = Point((x + 1) * scale - offset, (y + 1) * scale - offset)
            pixelRectangle = Rectangle(topLeft, bottomRight)
            pixelRectangle.setOutline(color)
            pixelRectangle.setFill(color)
            pixelRectangle.draw(win)


if __name__ == "__main__":

    # starting coords and sort them if the need it
    # We could add a check to make sure the pixels fit in our grid size (defined above), but this is just a POC so it'll be fine

    coords = [[1, 1], [2, 1], [5, 3], [4, 7], [7, 6], [4, 6], [9, 4]]
    # print("Coords: (orig)")
    # print(coords)
    # print("Coords: (sorted)")
    sort(coords)
    # print(coords)

    # Already sorted coords
    coords = [[1, 7], [2, 4], [3, 7], [4, 5]]

    # Generate random colors (size of coords)
    colors = pretty_colors(len(coords))

    # Make each pixel with a color
    pixels = []
    for i in range(len(coords)):
        pixels.append(Pixel(coords[i][0], coords[i][1], colors[i]))

    # Create visual window
    win = GraphWin(width=imageWidth, height=imageHeight)
    drawGridMethod()
    if (drawBefore):
        drawBeforeMethod(pixels);
    print()

    #D3_DUE--------------------
##    for row in reversed(range(1, gridHeight + 1)):
##        linesY = generateLines(pixels, row)
##        print(linesY)
##        due = D3_DUE(linesY)
##        print(due)
##        if (drawLines):
##            clear()
##            drawGridMethod()
##            drawLinesMethod(linesY)
##
##        # This breaks if drawLines is true, but I'm not going to bother implementing it
##        if drawNonSites:
##            drawNonSitesMethod(due, row)
            
    #UlgU_DUE------------------
    for row in reversed(range(1, gridHeight + 1)):
        linesY = generateLines(pixels, row)
        print(linesY)
        due = UlgU_DUE(linesY)
        print(due)     
        print()
        if (drawLines):
            clear()
            drawGridMethod()
            drawLinesMethod(linesY)

        # This breaks if drawLines is true, but I'm not going to bother implementing it
        if drawNonSites:
            drawNonSitesMethod(due, row)

    print("Breakpoint here for now to stop the window from closing")

#    for i in range(1,6):
#        print("s1: " + (str)(2*i+48) + " s2: " + (str)(4*i+36) + " s3 : " + (str)(6*i+40) + " s4: " + (str)(8*i+29))
