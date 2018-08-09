# initialise

import cv2
import vision
import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

from calibrationSettings import *

import web

from hardware.phobot.sensors import *
import hardware.phobot.motors as motors

from ai_fns import *
from ai_defend import *
from ai_attack import *

compassInitial = 0

# end initialise

# CV
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

readSerial()
compassInitial = dataCompass

mode = 0 #0=atk, 1=def

# per frame loop
while runBot():

	for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		frame = vision.getFrame(_frame.array)

		# check if frame exists
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

		rawCapture.truncate(0)
		# Stop program on ESC
		key = cv2.waitKey(1)
		if key == 27:
			break

	readSerial()

	if mode == 1:
		defend()
	else: 
		attack()

cv2.destroyAllWindows()
