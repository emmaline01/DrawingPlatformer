import cv2
import numpy as np

# Python program for Detection of a  
# specific color(blue here) using OpenCV with Python 
#from https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/

# Webcamera no 0 is used to capture the frames 
#cap = cv2.VideoCapture(0)  
cap = cv2.VideoCapture("random_vid.mp4")
#https://www.youtube.com/watch?v=gJgXsaj_gR0&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=10

# This drives the program into an infinite loop. 
while(cap.isOpened()):        
    # Captures the live stream frame-by-frame 
    _, frame = cap.read()  
    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    lower_red = np.array([110,50,50]) 
    upper_red = np.array([130,255,255]) 
    
# Here we are defining range of bluecolor in HSV 
# This creates a mask of blue coloured  
# objects found in the frame. 
    mask = cv2.inRange(hsv, lower_red, upper_red) 
    res = cv2.bitwise_and(frame,frame, mask= mask)

    ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
    contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        print(x,y,w,h)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

# The bitwise and of the frame and mask is done so  
# that only the blue coloured objects are highlighted  
# and stored in res 
    
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
