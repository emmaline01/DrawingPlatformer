from cmu_112_graphics import *
from tkinter import *
import cv2
import time
import numpy as np


def appStarted(app):
    pass
    
def cameraFired(app):
    """
    -In cameraFired, you can use app.frame 
    -app.frame is a numpy array
    -openCV images are all numpy arrays
    """
    #Example: You can blur the Camera!
    app.frame = cv2.GaussianBlur(app.frame, (15,15), 0)
    
def keyPressed(app, event):
    if event.key == "q":
        App._theRoot.app.quit()

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width/2, app.height/2)

def timerFired(app):
    print("timer firing!")
        
if __name__ == "__main__":
    runApp(width=1080, height=720)
    os._exit(0)
