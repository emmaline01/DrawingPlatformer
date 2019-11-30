#Drawing Platformer (Square Jumper)
#by Emmaline Mai (emai, Section B)

#Character class that keeps track of the main character's position and actions

#credit to https://opencv-python-tutroals.readthedocs.io/en/latest/
# py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html for 
# tutorials about importing opencv and numpy
import cv2
import numpy as np
import copy

class Character(object):

    #initializes the character's position, vertical velocity, and size
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.width = 20
        self.height = 20
    
    #the character continuously falls unless it touches a platform
    def fall(self, ground, currGround):
        self.y += self.dy
        nearestPtLeft = (-1, -1, -1, -1)
        nearestPtRight = (-1, -1, -1, -1)

        nearestPts = []
        newList = copy.copy(currGround)
        for i in range(len(ground)):
            newList += ground[i]
        nearestPtLeft, nearestPtRight = self.getNearestGroundPts(newList)
        xL, yL, _, _ = nearestPtLeft
        xR, yR, _, _ = nearestPtRight

        if (xL > -1 and xR > -1):
            #check if both points are in the same list
            inSameList = False
            if (nearestPtLeft in currGround and nearestPtRight in currGround):
                inSameList = True
            for i in range(len(ground)):
                if (nearestPtLeft in ground[i] and 
                    nearestPtRight in ground[i]):
                    inSameList = True
                    break
            
            #get the y coordinate on the line under the character
            yOnLine = yL - ((yL - yR)/(xR - xL))*(xL- self.x) 
            if (inSameList and abs(yOnLine - self.y) < self.height * 3):
                self.dy = -20

    #given a list of points, returns the two points nearest to the character 
    # on the left and right
    def getNearestGroundPts(self, ground):
        nearestPtLeft = (-1, -1, -1, -1)
        nearestPtRight = (-1, -1, -1, -1)
        for i in range(len(ground)):
            xL, yL, wL, hL = nearestPtLeft
            xR, yR, wR, hR = nearestPtRight

            x1,y1,w1,h1 = ground[i]
                    
            if (abs(self.x - x1) < abs(self.x - xL) and 
                abs(self.y - y1) < abs(self.y - yL) and
                x1 < self.x and self.y < y1):
                nearestPtLeft = ground[i]
            elif (abs(self.x - x1) < abs(self.x - xR) and 
                abs(self.y - y1) < abs(self.y - yR) and
                x1 > self.x and self.y < y1):
                nearestPtRight = ground[i]

        return nearestPtLeft, nearestPtRight

    #checks if the character fell off the bottom of the screen
    def checkFellOff(self, screenHeight):
        return (self.y > screenHeight) or (self.x < 0)

    #checks if the character is touching a given rectangle of points and
    #  returns the side of the character being touched
    def isTouching(self, pos):
        x,y,w,h = pos
        if ((abs(self.x - x) < self.width*2 and abs(self.y - y) < self.height*2)
            or (abs(self.x - x - w) < self.width*2 and 
            abs(self.y - y - h) < self.height*2)):
            if (self.x > x):
                return 'left'
            else:
                return 'right'
        return 'neither'

    #draws the character on the given frame
    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), 
            (self.x + self.width, self.y + self.height), 
            (171,239,81), thickness = -1)