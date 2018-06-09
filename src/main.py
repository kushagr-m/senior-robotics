import cv2
import vision
import os

import hardware.phobot.motors as motors

from calibrationSettings import *

video = cv2.VideoCapture(1)
#video = cv2.VideoCapture(os.path.dirname(os.path.abspath(__file__)) + '/../goaliepov.mp4')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# loop
while(True):
    frame = vision.getFrame(video)

    if frame is not None:
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
    
    def ballDirection():
        if ((frameDimensions[0]-ballCenterPadding)/2 < ballCenter[0] < (frameDimensions[0]+ballCenterPadding)/2):
            return "center"
        elif (ballCenter[0] > (frameDimensions[0]/2)):
            return "right"
        elif (ballCenter[0] < (frameDimensions[0]/2)):
            return "left"
        else: 
            pass

    print("ballCenter: ", ballCenter)
    print("ballRadius: ", ballRadius)
    print("goalCenter: ", goalCenter)
    print("goalDimens: ", goalDimensions)
    if ballCenter:
        print(ballDirection())

    # Stop program on ESC
    key = cv2.waitKey(10)
    if key == 27:
        break

cv2.destroyAllWindows()