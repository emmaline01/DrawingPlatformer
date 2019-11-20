'''
CHANGES SINCE TP1 MEETING/LAST AUTOLAB SUBMISSION:
instead of trying to stand on the platform, the character jumps as soon as 
    it lands
character's platform detection is functional
'''

#Character class that keeps track of the main character's position and actions

import cv2
import numpy as np
import copy

class Character(object):

    #initializes the character's position, vertical velocity, and size
    def __init__(self, x, y):
        #everything in self.frame coordinates
        self.x = x
        self.y = y
        self.dy = 0
        self.width = 20
        self.height = 20
    
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

            #check if both points are in the same list - 
            # not over an intentional gap
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

    #draws the character on the given frame
    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), 
            (self.x + self.width, self.y + self.height), 
            (0,0,255), thickness = -1)

    #checks if the character is touching a given rectangle of points
    #TODO: return what side of the character is touching if it is touching
    #TODO: incomplete
    def isTouching(self, pos):
        x,y,w,h = pos
        if ((abs(self.x - x) < 40 and abs(self.y - y) < 40)
            or (abs(self.x - x - w) < 40 and abs(self.y - y - h) < 40)):
            return True
        return False
