# initialise

import cv2
import vision
import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

from calibrationSettings import *

from ai_fns import *

#import web

import motors

import serial
ser = serial.Serial('/dev/ttyACM0',115200) # change to ACM1 if that is the USB port

def readSerial():

	# vv UNCOMMENT WHEN TOF vv
	#global data1TOF
	#global data2TOF
	#global data3TOF
	#global data4TOF

	global dataSwitch
	global dataCompass

	readSerial=ser.readline() # reads from serial until EOL character received - i.e. \n
	
	#if '1:' in readSerial: # Time of Flight sensors VV
	#    data1TOF = readSerial
	#elif '2:' in readSerial:
	#    data2TOF = readSerial
	#elif '3:' in readSerial:
	#    data3TOF = readSerial
	#elif '4:' in readSerial:
	#    data4TOF = readSerial
	# 
		
	if 'HIGH' in readSerial: # Momentary switch to detect ball VV
		dataSwitch = True
	elif 'LOW' in readSerial:
		dataSwitch = False
	else: # The only thing else that readSerial can be
		dataCompass = int(readSerial)

	return

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

#web.start()

def runBot():
	if True:
		return True
	else:
		return False
	return

readSerial()

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
