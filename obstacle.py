#Obstacle class that keeps track of an obstacle's position and actions

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
    
    #a hash function for an obstacle that depends on that obstacle's ID
    def __hash__(self):
        return hash(self.id)

    #checks if the obstacle is offscreen
    def isOffScreen(self):
        return (self.x < 0)

    #draws the obstacle on a given frame
    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), 
            (self.x + self.width, self.y + self.height), 
            (0,0,255), thickness = -1)
