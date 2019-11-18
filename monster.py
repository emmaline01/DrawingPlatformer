import cv2
import numpy as np

class Monster(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        print('not implemented')
        pass

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), 10, (0,0,255), thickness = -1)

    def __hash__(self):
        return hash((self.x, self.y))
