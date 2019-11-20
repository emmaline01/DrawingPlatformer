'''
CHANGES SINCE TP1 MEETING/LAST AUTOLAB SUBMISSION:
basic algorithm for monster movement added
'''

#Monster class that keeps track of a monster's position and actions
import cv2
import numpy as np

class Monster(object):
    #initializes the monster with a position
    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        self.character = character
        #40 calls to cameraFired per character jump

    #TODO: calculates target position and moves the monster towards it
    def move(self):
        dx = int(abs(self.character.x - self.x)/40)
        dy = int(-1*(self.y - self.character.y)/40)
        self.x += dx
        self.y += dy
        #if there will be ground at center screen when the monster gets there, target it
        #if you don't know yet just target center screen
        #if there will not be ground at center screen target middle of jump height from last platform?

        #alternatively
        #calculate where the character is likely to be when the monster reaches center screen
        #know how many frames it'll take to get from where you start to where you want to go

        #straight path to half the jump height above where the character is in the time it takes for the character to jump halfway
        #if character velocity is up, it's jumping up so yay
        #if character velocity is down, go to half the jump height below

        #OR just freaking go for wherever the character is at that point
        #a trash algorithm honeslty
        #also should move at constant speed, this sets the direction! TODO

    #draws the monster at its position on a given frame
    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), 10, (0,0,255), thickness = -1)

    #a hash function for the monster that depends on the monster's position
    def __hash__(self):
        return hash((self.x, self.y))
