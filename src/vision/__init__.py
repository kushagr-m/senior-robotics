import cv2
import numpy as np
import math

# Calibration
ballLower = (0, 233, 128)
ballUpper = (0, 255, 231)

def getFrame(video):
    (grabbed, frame) = video.read()
    if grabbed:
        return frame
    return None

def getHSVFrame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    return hsv

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

        cv2.circle(mask, center, radius, (255, 255, 255), 5)
        cv2.imshow('ballmask', mask)

        if (area / (math.pi * (radius ** 2))) > 0.75:
            return center, radius
    else:
        cv2.imshow('ballmask', mask)
    
    return None, None

cv2.namedWindow('goalmask', cv2.WINDOW_NORMAL)
def findGoal(hsvFrame):
    