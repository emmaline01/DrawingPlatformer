import cv2
import numpy as np
import copy

from monster import *

class mainApp(object):
    def __init__(self):
        self.dots = []
        self.isDrawing = False
        self.currLine = []
        
        self.scrollX = 5

        self.initMonsters()

        self.cap = cv2.VideoCapture(0)

        self.gameLoop()

    def initMonsters(self):
        self.monsters = set()
        self.monsters.add(Monster(0, 0))
    
    def gameLoop(self):
        #2 lines edited from https://stackoverflow.com/questions/39953263/
        # get-video-dimension-in-python-opencv
        width =  int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while (self.cap.isOpened()):

            self.blank = np.zeros((height, width, 3), np.uint8)
            _, self.frame = self.cap.read()

            self.cameraFired()
            self.redrawAll()

            actualDisplay = cv2.resize(self.frame, 
                    (width*3//4, height*3//4), 
                    interpolation=cv2.INTER_AREA)
            self.blank = cv2.resize(self.blank, 
                    (width*3//4, height*3//4), 
                    interpolation=cv2.INTER_AREA)
            self.blank = cv2.GaussianBlur(self.blank, (21,21), 0)

            combined = cv2.addWeighted(self.blank, 0.7, 
                actualDisplay, 0.3, 0)
            
            cv2.imshow('Drawing Platformer', combined)
            cv2.imshow('blank', self.blank)

            #this is here for a reason don't move it dammit
            self.checkKeyPressed()
            
    def redrawAll(self):
        self.drawDots()
        for monster in self.monsters:
            monster.draw(self.frame)

    def scrollListPts(self, lst):
        j = 0
        while (j < len(lst)):
            x,y,w,h = lst[j]
            lst[j] = (x-self.scrollX, y, w, h)

            if (x <= 0):
                lst.pop(j)
                continue
            j += 1

    def cameraFired(self):
        if (self.isDrawing):
            self.findBlue()
        
        i = 0
        while (i < len(self.dots)):
            self.scrollListPts(self.dots[i])
            if (len(self.dots[i]) == 0):
                self.dots.pop(i)
                continue
            i += 1
        self.scrollListPts(self.currLine)

    def checkKeyPressed(self):
        key = cv2.waitKey(25) & 0xFF
        if (key == ord('q')):
            self.endGame()
        elif (key == ord(' ')):
            if (self.isDrawing == True):
                self.isDrawing = False
                self.dots += [self.currLine]
                self.currLine = []
            else:
                self.isDrawing = True
            
    def findBlue(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV) 
        lower_b = np.array([100,130,130]) 
        upper_b = np.array([130,255,255])

    
        mask = cv2.inRange(hsv, lower_b, upper_b) 

        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
        contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, 
            cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if (y > 10 and h > 10):
                self.currLine.insert(0, (x,y,w,h))
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),2)

                #check that it isn't a stray errant detection
                
                if (len(self.currLine) > 1):
                    x1,y1,w1,h1 = self.currLine[1]
                    if (not (abs(x1-x) < 40 and abs(y1-y) < 40)):
                        self.currLine.pop(0)

    def drawDots(self):

        for j in range(len(self.dots)):
            for i in range(len(self.dots[j]) - 1):
                x1,y1,w1,h1 = self.dots[j][i]
                x2,y2,w2,h2 = self.dots[j][i+1]

                #draws anti-aliased line
                cv2.line(self.blank, (x1, y1), (x2, y2), (255,255,255), 
                    thickness = 20, lineType=cv2.LINE_AA)

        for i in range(len(self.currLine) - 1):
                x1,y1,w1,h1 = self.currLine[i]
                x2,y2,w2,h2 = self.currLine[i+1]

                cv2.line(self.blank, (x1, y1), (x2, y2), (255,255,255), 
                    thickness = 20, lineType=cv2.LINE_AA)
            
    def endGame(self):
        cv2.destroyAllWindows() 
        self.cap.release() 

m = mainApp()
