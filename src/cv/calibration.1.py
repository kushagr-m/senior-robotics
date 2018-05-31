import cv2
import numpy as np
import logging
import sys

mins = [0,0,0]
maxs = [0,0,0]

#frame = cv2.imread('callibyellow.png')
video = cv2.VideoCapture(1)

def nothing(x): #callback function
    pass

# Create a black image, a window
cv2.namedWindow('image',cv2.WINDOW_NORMAL)

# create trackbars for color change
#createTrackbar : label, window, min,max, callback function
cv2.createTrackbar('Hmin','image',0,255,nothing)
cv2.createTrackbar('Smin','image',0,255,nothing)
cv2.createTrackbar('Vmin','image',0,255,nothing)

cv2.createTrackbar('Hmax','image',0,255,nothing)
cv2.createTrackbar('Smax','image',0,255,nothing)
cv2.createTrackbar('Vmax','image',0,255,nothing)

while(1):
    (grabbed,frame) = video.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #hsv frame
        # get current positions of four trackbars
    hmin = cv2.getTrackbarPos('Hmin','image')
    smin = cv2.getTrackbarPos('Smin','image')
    vmin = cv2.getTrackbarPos('Vmin','image')

    hmax = cv2.getTrackbarPos('Hmax','image')
    smax = cv2.getTrackbarPos('Smax','image')
    vmax = cv2.getTrackbarPos('Vmax','image')
    lower = (hmin,smin,vmin)
    upper = (hmax,smax,vmax)
    print(lower)
    print(upper)
    #hsv = cv2.GaussianBlur(hsv,(5,5),10)
    #hsv = cv2.blur(hsv,(5,5))
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('image',mask)
    cv2.imshow('original',frame)


    cv2.waitKey(10)