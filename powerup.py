#Drawing Platformer (Square Jumper)
#by Emmaline Mai (emai, Section B)

#Powerup class that keeps track of a power up's position and actions

#credit to https://opencv-python-tutroals.readthedocs.io/en/latest/
# py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html for 
# tutorials about importing opencv and numpy
import cv2
import numpy as np

class Powerup(object):

    #initializes the powerup with position and size
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 15
    
    #checks if the powerup is offscreen
    def isOffScreen(self):
        return (self.x < 0)

    #draws the powerup on a given frame
    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), self.r, 
            (171,239,81), thickness = 2)
        cv2.circle(frame, (self.x, self.y), self.r // 2, 
            (171,239,81), thickness = -1)