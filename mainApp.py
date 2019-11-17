import cv2
import numpy as np
import copy

class mainApp(object):
    def __init__(self):
        self.dots = []
        self.isDrawing = False
        self.currLine = []
        self.cap = cv2.VideoCapture("random_vid.mp4")
        self.gameLoop()

    def gameLoop(self):
        while (self.cap.isOpened()):
            _, self.frame = self.cap.read()
            
            self.cameraFired()
            self.redrawAll()

            cv2.imshow('Drawing Platformer', self.frame)

            self.checkKeyPressed()
            
    def redrawAll(self):
        self.drawDots()
        
    def cameraFired(self):
        if (self.isDrawing):
            self.findBlue()

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
        lower_red = np.array([110,50,50]) 
        upper_red = np.array([130,255,255])

    
        mask = cv2.inRange(hsv, lower_red, upper_red) 

        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
        contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            self.currLine.insert(0, (x,y,w,h))

            #check that it isn't a stray errant detection
            if (len(self.currLine) > 1):
                x1,y1,w1,h1 = self.currLine[1]
                if (not (abs(x1-x) < 20 and abs(y1-y) < 20)):
                    self.currLine.pop(0)
                

    def drawDots(self):
        for j in range(len(self.dots)):
            for i in range(len(self.dots[j]) - 1):
                x1,y1,w1,h1 = self.dots[j][i]
                x2,y2,w2,h2 = self.dots[j][i+1]
                
                cv2.line(self.frame, (x1, y1), (x2, y2), (0,0,255))

        for i in range(len(self.currLine) - 1):
                x1,y1,w1,h1 = self.currLine[i]
                x2,y2,w2,h2 = self.currLine[i+1]
                
                cv2.line(self.frame, (x1, y1), (x2, y2), (0,0,255))
                #cv2.circle(self.frame, (x1, y1), 5, (0,0,255), thickness = -1)
            
    def endGame(self):
        cv2.destroyAllWindows() 
        self.cap.release() 

m = mainApp()