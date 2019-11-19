import cv2
import numpy as np

# Python program for Detection of a  
# specific color(blue here) using OpenCV with Python 
#from https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/

# Webcamera no 0 is used to capture the frames 
#cap = cv2.VideoCapture(0)  
cap = cv2.VideoCapture(0)
#https://www.youtube.com/watch?v=gJgXsaj_gR0&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=10

while(cap.isOpened()):
    
    _, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    lower_red = np.array([100,100,100]) 
    upper_red = np.array([130,255,255])
    
    #choosing colors to track
    #https://docs.opencv.org/trunk/df/d9d/tutorial_py_colorspaces.html
    #green = np.uint8([[[0,255,0 ]]])
    #hsv_green = cv.cvtColor(green,cv.COLOR_BGR2HSV)
    #print( hsv_green )

    
    mask = cv2.inRange(hsv, lower_red, upper_red) 
    res = cv2.bitwise_and(frame,frame, mask= mask)

    ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
    contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        #print(x,y,w,h)
        if (w > 10 and h > 10):
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    
    cv2.imshow('frame',frame) 
    cv2.imshow('mask',mask) 
    cv2.imshow('res',res)
    
    if (cv2.waitKey(25) & 0xFF== ord('q')):
        break
  
cv2.destroyAllWindows() 
  
cap.release() 
