#Drawing Platformer (Square Jumper)
#by Emmaline Mai (emai, Section B)

#LessEnemiesPowerup class that keeps track of a less-enemies-powerup's 
# position and actions

#credit to https://opencv-python-tutroals.readthedocs.io/en/latest/
# py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html for 
# tutorials about importing opencv and numpy
import cv2
import numpy as np
import random

from powerup import *

class LessEnemiesPowerup(Powerup):

    #initializes the powerup with position and size
    def __init__(self, x, y, app):
        super().__init__(x, y, app)

    #implements the powerup's power of reducing the chances that 
    # monsters and obstacles appear
    def doPower(self):
        self.app.obstacleChances += 10
        self.app.monsterChances += 10
    
    #reverses the powerup's power and increases the monster's and obstacle's 
    # chances of appearing back to normal
    def reversePower(self):
        self.app.obstacleChances -= 10
        self.app.monsterChances -= 10

    #draws the powerup on a given frame
    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), self.r, 
            (171,239,81), thickness = 2)
        cv2.circle(frame, (self.x, self.y), self.r // 2, 
            (171,239,81), thickness = -1)