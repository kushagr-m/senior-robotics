import cv2
import numpy as np
import math

# Calibration
from calibrationSettings import *

def getFrame(_frame):
    frame = cv2.resize(_frame, frameDimensions)
    return frame

def getHSVFrame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    return hsv

"""
findBall()

Inputs:  hsvFrame - a frame in the HSV colour space
Outputs: center   - A (x, y) tuple representing the pixel coordinate of the center of the ball
         radius   - An integer representing the pixel radius of the ball from the center

         Output is 'None, None' if a ball is not detected
"""
cv2.namedWindow('ballmask', cv2.WINDOW_NORMAL)
def findBall(hsvFrame):
    mask = cv2.inRange(hsvFrame, ballLower, ballUpper)
    mask = cv2.dilate(mask, None, iterations=3)

    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        
        area = cv2.contourArea(c)
        (x, y), radius = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        radius = int(radius)

        cv2.circle(mask, center, radius, (255, 255, 255), 1)
        cv2.imshow('ballmask', mask)

        if (area / (math.pi * (radius ** 2))) > 0.75:
            return center, radius
    else:
        cv2.imshow('ballmask', mask)
    
    return None, None

"""
findGoal()

Inputs:  hsvFrame   - a frame in the HSV colour space
Outputs: center     - A (x, y) tuple representing the pixel coordinate of the center of the goal
         dimensions - A (width, height) tuple representing the pixel size of the goal

         Output is 'None, None' if a goal is not detected
"""
cv2.namedWindow('goalmask', cv2.WINDOW_NORMAL)
def findGoal(hsvFrame):
    mask = cv2.inRange(hsvFrame, goalLower, goalUpper)

    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)

        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

        (x, y, w, h) = cv2.boundingRect(approx)
        ratio = w / h
        center = (int(x + w / 2), int(y + h / 2))

        cv2.imshow('goalmask', mask)
        #print(ratio)
        if w > goalMinSize[0] and h > goalMinSize[1] and ratio > goalWidthHeightRatio - 0.5 and ratio < goalWidthHeightRatio + 0.5:
            return center, (w, h)

    return None, None
    #cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    