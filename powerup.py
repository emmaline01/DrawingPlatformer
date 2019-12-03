#Drawing Platformer (Square Jumper)
#by Emmaline Mai (emai, Section B)

#Powerup class that keeps track of a power up's position and actions

#credit to https://opencv-python-tutroals.readthedocs.io/en/latest/
# py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html for 
# tutorials about importing opencv and numpy
import cv2
import numpy as np
import random

class Powerup(object):

    #initializes the powerup with position and size
    def __init__(self, x, y, app):
        self.x = x
        self.y = y
        self.r = 15
        self.app = app
        self.timer = 0
    
    #checks if the powerup is offscreen
    def isOffScreen(self):
        return (self.x < 0)

    #updates the movement of the powerup
    def update(self):
        if (self.timer >= 0):
            self.timer -= 1
            if (self.timer == 0):
                self.reversePower()
        self.x -= self.app.scrollX
        if (self.isOffScreen() and random.randint(1,20) == 1
            and self.timer < 0):
            self.x = self.app.width
            self.y = random.randint(self.r*2, self.app.height-self.r*2)

        x1 = self.x - self.r
        y1 = self.y - self.r
        x2 = self.x + self.r
        y2 = self.y + self.r

        if (self.app.player.isTouching((x1, x2, y1, y2)) == 'right' or
            self.app.player.isTouching((x1, y1, x2, y2)) == 'left'):
            self.x = -10
            self.timer = 80
            self.doPower()

    #a setup for a method that all subclasses of powerup should have 
    # implements the power
    def doPower(self):
        pass
    
    #a setup for a method that all subclasses of powerup should have 
    # undoes the power
    def reversePower(self):
        pass

    #draws the powerup on a given frame
    def draw(self, frame):
        pass