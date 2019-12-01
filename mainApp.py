#Drawing Platformer (Square Jumper)
#by Emmaline Mai (emai, Section B)

#This file contains the mainApp class, begins the game, and runs it

from monster import *
from character import *
from obstacle import *
from LessEnemiesPowerup import *
from slowerEnemiesPowerup import *

class MainApp(object):

    #initializes everything for one time and begins the game
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.margin = 30
        self.width =  int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.player = Character(self.width//2, 0)

        self.startGame()

    #sets all game elements up for the game to begin
    def startGame(self):
        self.scrollX = 5
        self.distance = 0
        self.inkMax = 30
        self.triesLeft = 3

        self.obstacleChances = 50
        self.monsterChances = 80

        self.startFromCheckpoint()
        self.initScreens()
        self.gameLoop()

    #initializes the game by keeping parts of model that stay when 
    # restarting from a checkpoint and initializing others
    def startFromCheckpoint(self):
        self.dots = []
        self.isDrawing = False
        self.lastDist = -10
        self.currLine = []
        self.ink = self.inkMax
        self.health = 5

        self.player.x = self.width//2
        self.player.y = 0
        self.player.dy = 0

        self.numMonsters = 0
        self.numObstacles = 0
        self.monsters = set()
        self.obstacles = set()

        self.lessEnemiesPowerup = LessEnemiesPowerup(-1, 0, self)
        self.slowerEnemiesPowerup = SlowerEnemiesPowerup(-1, 0, self)

        self.checkpointTimer = 0

        #starting from checkpoint
        self.distance = 150 * (self.distance // 150)        

    #calls functions to initialize the start, end, and help screens
    def initScreens(self):
        self.isStartScreen = True
        self.isEndScreen = False
        self.isHelpScreen = False

        self.initStartScreen()
        self.initHelpScreen()

    #sets up the starting screen
    def initStartScreen(self):
        self.startScreen = np.zeros((self.height, self.width, 3), 
            np.uint8)
        cv2.rectangle(self.startScreen, (0,0), 
            (self.width, self.height), (203,164,229), thickness = -1)
        cv2.putText(self.startScreen, 'SQUARE JUMPER', 
            (10, self.height//2 - 40), 
            cv2.FONT_HERSHEY_DUPLEX, 2, (46,6,69), 2, cv2.LINE_AA)
        cv2.putText(self.startScreen, 'Press space to play!', 
            (10, self.height//2 + 100), cv2.FONT_HERSHEY_DUPLEX, 1, 
            (46,6,69), 2, cv2.LINE_AA)
        cv2.putText(self.startScreen, 'Press h for help', 
            (10, self.height//2 + 150), cv2.FONT_HERSHEY_DUPLEX, 1, 
            (46,6,69), 2, cv2.LINE_AA)

    #sets up the ending screen
    def initEndScreen(self):
        self.endScreen = np.zeros((self.height, self.width, 3), 
            np.uint8)
        cv2.rectangle(self.endScreen, (0,0), 
            (self.width, self.height), (46,6,69), thickness = -1)
        cv2.putText(self.endScreen, 
            'Better luck next time.', 
            (10, self.height//2 - 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, 
            (203,164,229), 2, cv2.LINE_AA)
        cv2.putText(self.endScreen, 
            f'Total distance bounced: {self.distance}m', 
            (10, self.height//2), cv2.FONT_HERSHEY_DUPLEX, 1.2, 
            (203,164,229), 2, cv2.LINE_AA)
        if (self.triesLeft > 0):
            cv2.putText(self.endScreen, 
            f'{self.triesLeft} tries left. Press c to retry from checkpoint', 
            (10, self.height//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 
            (190,210,235), 2, cv2.LINE_AA)
        else:
            cv2.putText(self.endScreen, 
            'Sorry, you have no tries left.', 
            (10, self.height//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 
            (190,210,235), 2, cv2.LINE_AA)

        cv2.putText(self.endScreen, 
            'Press r to restart entirely', 
            (10, self.height//2 + 120), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 
            (190,210,235), 2, cv2.LINE_AA)

    #sets up the help screen
    def initHelpScreen(self):
        helpText = """
Help Screen

Press space to draw in the air with a blue pointer, 
and the drawings will appear on the screen as ground 
for the character. Lose by falling off the screen or by 
getting caught by an enemy, and get score based on 
total distance run. Gather power ups to temporarily
reduce the chances of obstacles/monsters appearing. 
Every 150m a checkpoint is reached, and a death 
afterward can return you to a checkpoint as long 
as you have tries left. You start with 3 tries.

Troubleshooting:
If the blue color detection of your pointer isn't 
working, move to a brighter area with a darker background.

Press h to return!"""
        self.helpScreen = np.zeros((self.height, self.width, 3), 
            np.uint8)
        cv2.rectangle(self.helpScreen, (0,0), 
            (self.width, self.height), (203,164,229), thickness = -1)
        lineHeight = 20
        i = 0
        for line in helpText.split('\n'):
            cv2.putText(self.helpScreen, line, (10, 10 + 25 * i), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (46,6,69), 1, cv2.LINE_AA)
            i += 1
            
    #the main game loop, which runs for as long as the camera is on, calls
    #  the various functions that make gameplay possible, and displays the 
    # screen
    def gameLoop(self):        
        while (self.cap.isOpened()):
            self.blank = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            _, self.frame = self.cap.read()
            
            if (self.isHelpScreen):
                toShow = self.helpScreen
            elif (self.isStartScreen):
                toShow = self.startScreen
            elif (self.isEndScreen):
                self.initEndScreen()
                toShow = self.endScreen
            else:
                self.frame = cv2.flip(self.frame, 1)

                self.cameraFired()
                self.redrawAll()
                
                self.blurDrawing()
                toShow = cv2.addWeighted(self.blank, 1, 
                    self.frame, 0.7, 0)
            
            cv2.imshow('Square Jumper', toShow)

            self.checkKeyPressed()

    #blurs and smooths out the drawing done by the player by 
    # resizing it multiple times
    def blurDrawing(self):
        for i in range(80):
            if (i % 2 == 0):
                self.blank = cv2.resize(self.blank, 
                    (self.width//4, self.height//4))
            else:
                self.blank = cv2.resize(self.blank, 
                    (self.width, self.height))

    #called with every new new frame captured by the camera, updates the 
    # positions of all game elements
    def cameraFired(self):
        self.distance += 1
        #game gets harder
        self.checkCheckpointReached()
        self.checkIncreaseScrollX()

        if (self.isDrawing):
            self.findBlue()
            self.ink -= 1
            if (self.ink <= 0):
                self.isDrawing = False
        elif (self.ink < self.inkMax):
            self.ink += 1
        
        i = 0
        while (i < len(self.dots)):
            self.scrollListPts(self.dots[i])
            if (len(self.dots[i]) == 0):
                self.dots.pop(i)
                continue
            i += 1
        self.scrollListPts(self.currLine)
        self.player.fall(self.dots, self.currLine)
        if (self.player.checkFellOff(self.height)):
            self.isEndScreen = True

        self.lessEnemiesPowerup.update()
        self.slowerEnemiesPowerup.update()
        self.updateMonsters()
        self.updateObstacles()
    
    def checkCheckpointReached(self):
        if (self.checkpointTimer > 0):
            cv2.putText(self.frame, 'Checkpoint reached!', 
                (self.width//2 - 150, self.height//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (171,239,81), 2, cv2.LINE_AA)
            self.checkpointTimer -= 1

        if (self.distance % 150 == 0):
            if (self.monsterChances > 20): 
                self.monsterChances -= 10
            if (self.obstacleChances > 20): 
                self.obstacleChances -= 10
            if (self.inkMax > 10): 
                self.inkMax -= 5
            self.lastDist = self.distance
            self.checkpointTimer = 20

    #increments scrollX more gradually than all at once
    def checkIncreaseScrollX(self):
        if (self.lastDist + 20 > self.distance and self.distance % 10 == 0):
            self.scrollX += 1
        else:
            self.lastDist = -10

    #updates all of the monsters' movements
    def updateMonsters(self):
        toRemove = None
        for monster in self.monsters:
            monster.move(self.obstacles)
            if (monster.isOffScreen(self.height)):
                toRemove = monster
            x1 = monster.x - monster.r
            y1 = monster.y - monster.r
            x2 = monster.x + monster.r
            y2 = monster.y + monster.r
            if (self.player.isTouching((x1, y1, x2, y2)) == 'right' or 
                self.player.isTouching((x1, y1, x2, y2)) == 'left'):
                self.health -= 1
                toRemove = monster
                if (self.health == 0):
                    self.isEndScreen = True
        if (toRemove != None):
            self.monsters.remove(toRemove)

        if (random.randint(1, self.monsterChances) == 1):
            self.numMonsters += 1
            self.monsters.add(Monster(self.width, 
                random.randint(0, self.height), self.player,
                self.numMonsters))

    #updates all of the obstacles' movements 
    def updateObstacles(self):
        toRemove = None
        for obstacle in self.obstacles:
            obstacle.x -= self.scrollX
            if (obstacle.isOffScreen()):
                toRemove = obstacle
            if (self.player.isTouching(
                (obstacle.x, obstacle.y, obstacle.width, obstacle.height))
                == 'right'):
                self.player.x -= self.scrollX
        if (toRemove != None):
            self.obstacles.remove(toRemove)

        if (random.randint(1,self.obstacleChances) == 1):
            self.numObstacles += 1
            randomHeight = random.randint(20, 80)
            self.obstacles.add(Obstacle(self.width, 
                random.randint(0, self.height - randomHeight), 
                randomHeight, self.numObstacles))

    #scrolls the ground list across the screen
    def scrollListPts(self, lst):
        j = 0
        while (j < len(lst)):
            x,y,w,h = lst[j]
            lst[j] = (x - self.scrollX, y, w, h)

            if (x <= 0):
                lst.pop(j)
                continue
            j += 1

    #checks keys to see if the player wants to close the window, or draw
    def checkKeyPressed(self):
        key = cv2.waitKey(25) & 0xFF
        #universal keys
        if (key == ord('q')):
            self.endGame()
        elif (key == ord('r')):
            self.startGame()
        elif (key == ord('h')):
            self.isHelpScreen = not self.isHelpScreen

        if (self.isStartScreen): 
            if (key == ord(' ')):
                self.isStartScreen = False
        elif (self.isEndScreen):
            if (self.triesLeft > 0 and key == ord('c')):
                self.startFromCheckpoint()
                self.isEndScreen = False
                self.triesLeft -= 1
        elif (not self.isEndScreen and not self.isHelpScreen):
            if (key == ord(' ')):
                if (self.isDrawing == True):
                    self.isDrawing = False
                    self.dots += [self.currLine]
                    self.currLine = []
                else:
                    self.isDrawing = True

    #uses vision to identify the blue pointer and store its current position 
    # as the newest point in the list of point forming a line currently being 
    # drawn, if the blue identified isn't a stray point from the background    
    #credit to https://www.geeksforgeeks.org/detection-specific-colorblue-
    # using-opencv-python/ for opencv color detection tutorials and inspiration
    def findBlue(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV) 
        lower_b = np.array([100,130,130]) 
        upper_b = np.array([130,255,255])
    
        mask = cv2.inRange(hsv, lower_b, upper_b) 

        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
        contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, 
            cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if (y > 10 and h > 10):
                self.currLine.insert(0, (x,y,w,h))
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(190,210,235),2)

                #check that it isn't a stray errant detection
                if (len(self.currLine) > 1):
                    x1,y1,w1,h1 = self.currLine[1]
                    if (not (abs(x1-x) < 60 and abs(y1-y) < 60)):
                        self.currLine.pop(0)

    #main function that draws all of the game elements
    def redrawAll(self):
        #draw labels
        cv2.rectangle(self.frame, (0, self.height - self.margin), 
            (self.width, self.height), (190,210,235), thickness = -1)
        cv2.rectangle(self.frame, (0, 0), 
            (self.width, self.margin), (190,210,235), thickness = -1)

        cv2.putText(self.frame, 'Press h for help', (10, self.height - 10), 
            cv2.FONT_HERSHEY_DUPLEX, 0.65, (46,6,69), 1, cv2.LINE_AA)
        text=f'Distance:{self.distance}m Ink:{self.ink} Health:{self.health}'
        cv2.putText(self.frame, text, (10, 20), 
            cv2.FONT_HERSHEY_DUPLEX, 0.65, (46,6,69), 1, cv2.LINE_AA)

        #draw game elements
        self.drawMountains()
        self.drawDots()
        for monster in self.monsters:
            monster.draw(self.frame)
        for obstacle in self.obstacles:
            obstacle.draw(self.frame)
        self.player.draw(self.frame)
        self.lessEnemiesPowerup.draw(self.frame)
        self.slowerEnemiesPowerup.draw(self.frame)

    #parallax drawing of mountains in the background   
    def drawMountains(self):
        backG = self.frame.copy()

        mountainWidth = self.width // 5

        #back set
        for i in range(-1 * (self.scrollX + 2) * self.distance, 
            self.width, mountainWidth):
            if (i + mountainWidth >= 0):
                trianglePts = np.array([(i, self.height - self.margin), 
                    (i+mountainWidth, self.height - self.margin), 
                    ((i+i+mountainWidth)//2, 
                    self.height - 150 - self.margin)])
                cv2.drawContours(backG, [trianglePts], -1, (203,164,229), -1)
        
        #front set
        for i in range(-1 * self.scrollX * self.distance, self.width, 
            mountainWidth):
            if (i + mountainWidth >= 0):
                trianglePts = np.array([(i, self.height - self.margin), 
                    (i+mountainWidth, self.height - self.margin), 
                    ((i+i+mountainWidth)//2, 
                    self.height - 75 - self.margin)])
                cv2.drawContours(backG, [trianglePts], -1, (190,210,235), -1)

        self.frame = cv2.addWeighted(backG, 0.5, self.frame, 0.5, 0)
    
    #draws the lines on the screen that the player is drawing
    def drawDots(self):
        for j in range(len(self.dots)):
            for i in range(len(self.dots[j]) - 1):
                x1,y1,w1,h1 = self.dots[j][i]
                x2,y2,w2,h2 = self.dots[j][i+1]

                #draws anti-aliased line
                cv2.line(self.blank, (x1, y1), (x2, y2), (190,210,235), 
                    thickness = 20, lineType=cv2.LINE_AA)

        for i in range(len(self.currLine) - 1):
                x1,y1,w1,h1 = self.currLine[i]
                x2,y2,w2,h2 = self.currLine[i+1]

                cv2.line(self.blank, (x1, y1), (x2, y2), (190,210,235), 
                    thickness = 20, lineType=cv2.LINE_AA)

    # closes the windows when the player wants to quit the game        
    def endGame(self):
        cv2.destroyAllWindows() 
        self.cap.release() 

m = MainApp()
