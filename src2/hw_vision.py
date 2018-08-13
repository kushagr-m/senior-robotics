import cv2
import numpy as np
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import threading

# Calibration
from calibration import *

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('ballmask', cv2.WINDOW_NORMAL)
cv2.namedWindow('goalymask', cv2.WINDOW_NORMAL)
cv2.namedWindow('goalgmask', cv2.WINDOW_NORMAL)

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

def start_cv():
    try:
        for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		    frame = getFrame(_frame.array)

            if frame is None:
			    continue

            overlayedFrame = frame.copy()
		    hsv = getHSVFrame(frame)

            ballCenter, ballRadius = findBall(hsv)
            if ballCenter:
                cv2.circle(overlayedFrame, ballCenter, ballRadius, (0, 255, 0), 2)

            goalCenter, goalDimensions = findGoal(hsv)
            if goalCenter:
                cv2.circle(overlayedFrame, goalCenter, 5, (0, 0, 255), 5)

            cv2.imshow('image', overlayedFrame)

		    rawCapture.truncate(0)

    except KeyboardInterrupt:
        print('Stopping CV')
        cv2.destroyAllWindows()

t = threading.Thread(target=start_cv)
t.daemon = True
t.start()