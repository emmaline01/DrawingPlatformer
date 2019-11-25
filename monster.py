#Monster class that keeps track of a monster's position and actions
import cv2
import numpy as np
import math

class Monster(object):
    #initializes the monster with a position
    def __init__(self, x, y, character, id):
        self.id = id
        self.r = 10
        self.x = x
        self.y = y
        self.speed = 10
        self.character = character
        self.targetNode = (self.character.x, self.character.y)
        #40 calls to cameraFired per character jump

    #moves the monster and adjusts its target node coordinates
    def move(self, obstacles):
        if (self.x - self.r > self.character.x):
            if (self.hasDirectPathToCharacter(obstacles)):
                self.targetNode = (self.character.x, self.character.y)
            else:
                self.newTargetNode(obstacles)
            self.moveTowardsTargetNode()
        else:
            self.x -= self.speed
    
    #finds a new target node by choosing the most optimal of possible nodes
    def newTargetNode(self, obstacles):
        nodes = self.getNodes(obstacles)

        newTarget = (self.x, self.y)
        targetX, targetY = newTarget
        for nodeX, nodeY in nodes:
            #choose the node with the closest x-value to the player
            if (abs(nodeX - self.character.x) > 
                abs(targetX - self.character.x)):
                newTarget = (nodeX, nodeY)
                targetX, targetY = newTarget
            #if there are two nodes with closest x-values, then choose the
            #  one with the closest y-value
            elif (abs(nodeX - self.character.x) == 
                abs(targetX - self.character.x)):
                if (abs(nodeY - self.character.y) < 
                    abs(targetY - self.character.y)):
                    newTarget = (nodeX, nodeY)
                    targetX, targetY = newTarget

        self.targetNode = newTarget

    #get all possible nodes the monster could travel to between itself and 
    # the player
    def getNodes(self, obstacles):
        nodes = []
        for obstacle in obstacles:
            if (obstacle.x > self.character.x and obstacle.x < self.x):
                x = obstacle.x + obstacle.width // 2
                y1 = obstacle.y
                y2 = obstacle.y + obstacle.height
                
                slope = (y1 - self.y) / (x - self.character.x)
                if (not self.goesThroughObstacles(slope, obstacles)):
                    nodes += [(x, y1)]
                
                slope = (y2 - self.y) / (x - self.character.x)
                if (not self.goesThroughObstacles(slope, obstacles)):
                    nodes += [(x, y2)]

        return nodes

    #move the monster toward its target coordinates at a set speed, and if 
    # it reaches the target just move forward
    def moveTowardsTargetNode(self):
        targetX, targetY = self.targetNode
        if (targetX != self.x):
            slope = (targetY - self.y) / (targetX - self.x)
            theta = math.atan(slope)
            self.y -= int(self.speed*math.sin(theta))
            self.x = self.x - int(self.speed*math.cos(theta)) - 3
            #overshoot a little bit
        else:
            self.x -= self.speed

    #checks if the monster has a direct path towards the character
    def hasDirectPathToCharacter(self, obstacles):
        slope = (self.character.y - self.y) / (self.x - self.character.x)
        if (self.goesThroughObstacles(slope, obstacles)):
            return False
        return True

    #checks if a given straight line path for the monster goes through obstacles
    def goesThroughObstacles(self, slope, obstacles):
        for obstacle in obstacles:
            x = obstacle.x + obstacle.width//2
            y = slope*(x - self.x) + self.y
            if (y > obstacle.y and y < obstacle.y + obstacle.height):
                return True
        return False

    #checks if the monster has gone off the edge of the screen
    def isOffScreen(self):
        return (self.x < 0)

    #draws the monster at its position on a given frame
    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), self.r, (0,0,255), thickness = -1)

    #a hash function for the monster that depends on the monster's ID
    def __hash__(self):
        return hash((self.id))
