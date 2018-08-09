import cv2
import vision
import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

from calibrationSettings import *
import hardware.phobot.motors as motors

import web

# serial_read -----------------

import serial
ser = serial.Serial('/dev/ttyACM0',115200) # change to ACM1 if that is the USB port

while True:
    readSerial=ser.readline() # reads from serial until EOL character received - i.e. \n
    
    if ':' in readSerial:
        dataTOF = readSerial
    else:
        dataCompass = readSerial

# -----------------------------


# empty variables for functions

compassInitial = 0

# -----------------------------

# CV
if True:
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    video = cv2.VideoCapture(0)
    #video = cv2.VideoCapture(os.path.dirname(os.path.abspath(__file__)) + '/../goaliepov.mp4')
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)

web.start()

def runBot():
    if web.is_running():
        return True
    else:
        return False
    return
        
#per frame 
#loop
for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = vision.getFrame(_frame.array)

    #check if frame exists
    if frame is None:
        continue
    
    overlayedFrame = frame.copy()
    hsv = vision.getHSVFrame(frame)

    if runBot():
        # Identify the ball
        ballCenter, ballRadius = vision.findBall(hsv)
        if ballCenter:
            cv2.circle(overlayedFrame, ballCenter, ballRadius, (0, 255, 0), 2)

        goalCenter, goalDimensions = vision.findGoal(hsv)
        if goalCenter:
            cv2.circle(overlayedFrame, goalCenter, 5, (0, 0, 255), 5)
        
        cv2.imshow('image', overlayedFrame)

        # Print Ball Statistics
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


# calibrate

def calibrateAI():

    compassInitial = dataCompass

    return


# DIRECTION HELPER FUNCTIONS

from ai_fns import *
from ai_defend import *
from ai_attack import *


"""
    # track the ball at all times
    if ballDirection() == "left":
        motors.rotate(-100)
    elif ballDirection() == "right":
        motors.rotate(100)

    if (ballDirection() == "center" && goalComDir() == "center"):
        motors.direction(0)
    
    if (goalComDir() == "left"):
        motors.direction(45)
    elif (goalComDir() == "right"):
        motors.direction(315)


facing: FORWARDS AT ALL TIMES WITHIN 180deg of the goal

always face the ball (while facing forward)

never face our own goal

if there is a straight shot


if ball is going towards our goal
    goto our goal
"""

cv2.destroyAllWindows()