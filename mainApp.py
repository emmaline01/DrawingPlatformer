#This file contains the mainApp class, begins the game, and runs it

import cv2
import numpy as np
import copy

from monster import *
from character import *

class mainApp(object):

    #initializes all the game elements and enters the game loop
    def __init__(self):
        self.dots = []
        self.isDrawing = False
        self.currLine = []
        
        self.scrollX = 5

        self.initMonsters()

        self.cap = cv2.VideoCapture(0)

        #2 lines edited from https://stackoverflow.com/questions/39953263/
        # get-video-dimension-in-python-opencv
        self.width =  int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.player = Character(self.width//2, self.height//2)

        self.gameLoop()

    #initializes all of the monsters
    def initMonsters(self):
        self.monsters = set()
        self.monsters.add(Monster(0, 0))
    
    #the main game loop, which runs for as long as the camera is on, calls
    #  the various functions that make gameplay possible, and displays the 
    # screen
    def gameLoop(self):

        while (self.cap.isOpened()):

            self.blank = np.zeros((self.height, self.width, 3), np.uint8)
            _, self.frame = self.cap.read()

            self.cameraFired()
            self.redrawAll()
            
            self.blurDrawing()
            combined = cv2.addWeighted(self.blank, 0.5, 
                self.frame, 0.5, 0)
            
            cv2.imshow('Drawing Platformer', combined)
            cv2.imshow('blank', self.blank)

            #this is here for a reason don't move it dammit
            self.checkKeyPressed()

    #blurs and smooths out the drawing done by the player by 
    # resizing it multiple times
    def blurDrawing(self):
        #resizing this many times already just blurs it 
        #self.blank = cv2.GaussianBlur(self.blank, (21,21), 0)
        for i in range(80):
            if (i % 2 == 0):
                self.blank = cv2.resize(self.blank, 
                    (self.width//4, self.height//4))
            else:
                self.blank = cv2.resize(self.blank, 
                    (self.width, self.height))

    #credit to https://stackoverflow.com/questions/14063070/overlay-a-smaller-
    # image-on-a-larger-image-python-opencv/14102014
    #places a smaller image on a larger image
    def placeOn(smallImg, bigImg, yOffset, xOffset):
        bigImg[yOffset:yOffset+smallImg.shape[0], xOffset:xOffset+smallImg.shape[1]] = smallImg

    #main function that draws all of the game elements
    def redrawAll(self):
        self.drawDots()
        for monster in self.monsters:
            monster.draw(self.frame)
        self.player.draw(self.frame)

    #scrolls the ground list across the screen
    def scrollListPts(self, lst):
        j = 0
        while (j < len(lst)):
            x,y,w,h = lst[j]
            lst[j] = (x-self.scrollX, y, w, h)

            if (x <= 0):
                lst.pop(j)
                continue
            j += 1

    #called with every new new frame captured by the camera, updates the 
    # positions of all game elements
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

        self.player.dy += 1
        self.player.fall(self.dots, self.currLine)

    #checks keys to see if the player wants to close the window, or draw
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
        elif (key == ord('g')):
            self.player.y = 0
            self.player.dy = 0

    #uses vision to identify the blue pointer and store its current position 
    # as the newest point in the list of point forming a line currently being 
    # drawn, if the blue identified isn't a stray point from the background    
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
                    if (not (abs(x1-x) < 60 and abs(y1-y) < 60)):
                        self.currLine.pop(0)

    #draws the lines on the screen that the player is drawing
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

    # closes the windows when the player wants to quit the game        
    def endGame(self):
        cv2.destroyAllWindows() 
        self.cap.release() 

m = mainApp()
