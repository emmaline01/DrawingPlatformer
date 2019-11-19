import cv2
import numpy as np

class Character(object):
    def __init__(self, x, y):
        #everything in self.frame coordinates
        self.x = x
        self.y = y
        self.dy = 0
        self.width = 20
        self.height = 20
    
    #there's a problem where it balances on the highest point no necessarily near it x-direction wise
    def getNearestGroundPts(self, ground):
        nearestPtLeft = (-1, -1, -1, -1)
        nearestPtRight = (-1, -1, -1, -1)
        for i in range(len(ground)):
            xL, yL, wL, hL = nearestPtLeft
            xR, yR, wR, hR = nearestPtRight

            x1,y1,w1,h1 = ground[i]
                    
            if (abs(self.x - x1) < abs(self.x - xL) and 
                abs(self.y -y1) < abs(self.y - yL) and
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
        for i in range(len(ground)):
            nL, nR = self.getNearestGroundPts(ground[i])
            nearestPts += [nL, nR]
        nL, nR = self.getNearestGroundPts(currGround)
        nearestPts += [nL, nR]

        nearestPtLeft, nearestPtRight = self.getNearestGroundPts(nearestPts)


        '''
        for i in range(len(currGround)):
            xL, yL, _, _ = nearestPtLeft
            xR, yR, _, _ = nearestPtRight

            #find the two points nearest to it
            x1,y1,w1,h1 = currGround[i]

            if (abs(self.x - x1) < abs(self.x - xL) and 
                abs(self.y -y1) < abs(self.y - yL) and
                x1 < self.x):
                nearestPtLeft = currGround[i]
            elif (abs(self.x - x1) < abs(self.x - xR) and 
                abs(self.y - y1) < abs(self.y - yR) and
                x1 > self.x):
                nearestPtRight = currGround[i]
        '''
        xL, yL, _, _ = nearestPtLeft
        xR, yR, _, _ = nearestPtRight
        if (xL > -1 and xR > -1):
            self.dy = 0
            self.y = int(yR / xR * xL)

    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), 
            (self.x + self.width, self.y + self.height), 
            (0,0,255), thickness = -1)

    #return what side of the character is touching if it is touching
    def isTouching(self, pos):
        x,y,w,h = pos
        if ((abs(self.x - x) < 40 and abs(self.y - y) < 40)
            or (abs(self.x - x - w) < 40 and abs(self.y - y - h) < 40)):
            return True
        return False
