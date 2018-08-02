import cv2
import vision
import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

import hardware.phobot.motors as motors
import hardware.phobot.compass as compass

from calibrationSettings import *

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

video = cv2.VideoCapture(0)
#video = cv2.VideoCapture(os.path.dirname(os.path.abspath(__file__)) + '/../goaliepov.mp4')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

#define functions
def ballDirection():
    if ((frameDimensions[0]-ballCenterPadding)/2 < ballCenter[0] < (frameDimensions[0]+ballCenterPadding)/2):
        return "center"
    elif (ballCenter[0] > (frameDimensions[0]/2)):
        return "right"
    elif (ballCenter[0] < (frameDimensions[0]/2)):
        return "left"
    else: 
        pass
        
#per frame 
#loop
for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = vision.getFrame(_frame.array)

    #check if frame exists
    if frame is None:
        continue
    
    overlayedFrame = frame.copy()
    hsv = vision.getHSVFrame(frame)

    # Identify the ball
    ballCenter, ballRadius = vision.findBall(hsv)
    if ballCenter:
        cv2.circle(overlayedFrame, ballCenter, ballRadius, (0, 255, 0), 2)

    goalCenter, goalDimensions = vision.findGoal(hsv)
    if goalCenter:
        cv2.circle(overlayedFrame, goalCenter, 5, (0, 0, 255), 5)
    
    cv2.imshow('image', overlayedFrame)

    print("ballCenter: ", ballCenter)
    print("ballRadius: ", ballRadius)
    print("goalCenter: ", goalCenter)
    print("goalDimens: ", goalDimensions)
    if ballCenter:
        print(ballDirection())

    rawCapture.truncate(0)
    # Stop program on ESC
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()