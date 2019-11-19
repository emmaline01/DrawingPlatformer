#Monster class that keeps track of a monster's position and actions
import cv2
import numpy as np

class Monster(object):
    #initializes the monster with a position
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #TODO: calculates target position and moves the monster towards it
    def move(self):
        print('not implemented')
        pass

    #draws the monster at its position on a given frame
    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), 10, (0,0,255), thickness = -1)

    #a hash function for the monster that depends on the monster's position
    def __hash__(self):
        return hash((self.x, self.y))
