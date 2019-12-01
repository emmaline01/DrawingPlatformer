#Drawing Platformer (Square Jumper)
#by Emmaline Mai (emai, Section B)

#slowerEnemiesPowerup class that keeps track of a slower-enemies-powerup's 
# position and actions

#credit to https://opencv-python-tutroals.readthedocs.io/en/latest/
# py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html for 
# tutorials about importing opencv and numpy
import cv2
import numpy as np
import random

from powerup import *

class SlowerEnemiesPowerup(Powerup):

    #initializes the powerup with position and size
    def __init__(self, x, y, app):
        super().__init__(x, y, app)

    #implements the powerup's power of slowing down all enemies
    def doPower(self):
        for monster in self.app.monsters:
            monster.speed -= 5
    
    #reverses the powerup's power and brings enemies back to normal speed
    def reversePower(self):
        for monster in self.app.monsters:
            monster.speed += 5

    #draws the powerup on a given frame
    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), self.r, 
            (203,164,229), thickness = 2)
        cv2.circle(frame, (self.x, self.y), self.r // 2, 
            (46,6,69), thickness = -1)