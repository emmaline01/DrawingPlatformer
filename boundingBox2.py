import cv2
import numpy as np

# Python program for Detection of a  
# specific color(blue here) using OpenCV with Python 
#from https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/

# Webcamera no 0 is used to capture the frames 
#cap = cv2.VideoCapture(0)  
cap = cv2.VideoCapture("random_vid.mp4")
#https://www.youtube.com/watch?v=gJgXsaj_gR0&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=10

if (cap.isOpened() == False):
    print("gdi")


# This drives the program into an infinite loop. 
while(cap.isOpened()):        
    # Captures the live stream frame-by-frame 
    _, frame = cap.read()  
    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    lower_red = np.array([110,50,50]) 
    upper_red = np.array([130,255,255]) 

    #there's an issue here somewhere
    blackWhite = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(blackWhite, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv2.boundingRect(c)
        if rect[2] < 100 or rect[3] < 100: continue
        x,y,w,h = rect
        print(x,y,w,h)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    
# Here we are defining range of bluecolor in HSV 
# This creates a mask of blue coloured  
# objects found in the frame. 
    mask = cv2.inRange(hsv, lower_red, upper_red) 

# The bitwise and of the frame and mask is done so  
# that only the blue coloured objects are highlighted  
# and stored in res 
    res = cv2.bitwise_and(frame,frame, mask= mask) 
    cv2.imshow('frame',frame) 
    cv2.imshow('mask',mask) 
    cv2.imshow('res',res) 
  
# This displays the frame, mask  
# and res which we created in 3 separate windows. 
    if (cv2.waitKey(25) & 0xFF== ord('q')):
        break
  
# Destroys all of the HighGUI windows. 
cv2.destroyAllWindows() 
  
# release the captured frame 
cap.release() 
