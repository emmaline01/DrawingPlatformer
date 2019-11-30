#Drawing Platformer (Square Jumper)
#by Emmaline Mai (emai, Section B)

#Obstacle class that keeps track of an obstacle's position and actions

#credit to https://opencv-python-tutroals.readthedocs.io/en/latest/
# py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html for 
# tutorials about importing opencv and numpy
import cv2
import numpy as np

class Obstacle(object):

    #initializes the obstacle with position, size, and ID
    def __init__(self, x, y, height, id):
        self.x = x
        self.y = y
        self.width = 10
        self.height = height
        self.id = id
    
    #checks if the obstacle is offscreen
    def isOffScreen(self):
        return (self.x < 0)

    #draws the obstacle on a given frame
    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), 
            (self.x + self.width, self.y + self.height), 
            (63,48,164), thickness = -1)

    #a hash function for an obstacle that depends on that obstacle's ID
    def __hash__(self):
        return hash(self.id)