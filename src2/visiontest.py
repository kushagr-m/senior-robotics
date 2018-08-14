import cv2
import numpy as np
import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

goalCalibration = False

mins = [0,0,0]
maxs = [0,0,0]

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

cv2.namedWindow('original', cv2.WINDOW_NORMAL)

for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = _frame.array

    hsv = cv2.resize(frame, (320, 240))
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 5)
    
    cv2.imshow('original', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

    rawCapture.truncate(0)

cv2.destroyAllWindows()