#import hw_motors as motors
import hw_motors2 as motors
#from hw_read import *

# import hw_compass as compass

import hw_momentary as momentary
#from hw_vision import *
from calibration import *

from ai_attack import *
from ai_defend import *


import cv2
import numpy as np
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

botMode = 0
# 0 = attack
# 1 = defend

#compass.initialise()
#compassInitial = compass.readAngle()

def goalComDir():
	global compassInitial

	compassAngle = compass.readAngle()
	relativeDir = compassAngle-compassInitial
	
	if relativeDir<=-180:
		relativeDir+=360
	
	elif relativeDir>180:
		relativeDir-=360
		
	return relativeDir

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

ball_pos = (0, 0)
ball_radius = 0
goal_y_pos = (0, 0)
goal_y_dimensions = 0
goal_b_pos = (0, 0)
goal_b_dimensions = 0

inv_gamma = 1.0 / gamma
gamma_table = np.array([((i / 255.0) ** inv_gamma) * 255
	for i in np.arange(0, 256)]).astype("uint8")

def getFrame(_frame):
	frame = cv2.resize(_frame, frameDimensions)
	return frame

def getHSVFrame(frame):
	#hsv = cv2.LUT(frame, gamma_table)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (5, 5), 5)
	return hsv

#cv2.namedWindow("image", cv2.WINDOW_NORMAL)

#cv2.namedWindow('ballmask', cv2.WINDOW_NORMAL)
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
		#cv2.imshow('ballmask', mask)

		if (area / (math.pi * (radius ** 2))) > 0.5:
			return center, radius
	else:
		#cv2.imshow('ballmask', mask)
		pass
	
	return None, None

#cv2.namedWindow('goalymask', cv2.WINDOW_NORMAL)
def findYGoal(hsvFrame):
	mask = cv2.inRange(hsvFrame, goalYLower, goalYUpper)

	image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) > 0:
		c = max(contours, key=cv2.contourArea)

		perimeter = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

		(x, y, w, h) = cv2.boundingRect(approx)
		ratio = w / h
		center = (int(x + w / 2), int(y + h / 2))

		#cv2.imshow('goalymask', mask)
		#print(ratio)
		if w > goalMinSize[0] and h > goalMinSize[1] and ratio > goalWidthHeightRatio - 0.5 and ratio < goalWidthHeightRatio + 0.5:
			return center, (w, h)

	return None, None
	#cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

#cv2.namedWindow('goalbmask', cv2.WINDOW_NORMAL)
def findBGoal(hsvFrame):
	mask = cv2.inRange(hsvFrame, goalBLower, goalBUpper)

	image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) > 0:
		c = max(contours, key=cv2.contourArea)

		perimeter = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

		(x, y, w, h) = cv2.boundingRect(approx)
		ratio = w / h
		center = (int(x + w / 2), int(y + h / 2))

		#cv2.imshow('goalbmask', mask)
		#print(ratio)
		if w > goalMinSize[0] and h > goalMinSize[1] and ratio > goalWidthHeightRatio - 0.5 and ratio < goalWidthHeightRatio + 0.5:
			return center, (w, h)

	return None, None    

while True:
	try:
		for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			frame = _frame.array
			
			if frame is None:
				print("no frame")
				continue
			#cv2.imshow("image", frame)
			print("frame")
			
			overlayedFrame = frame.copy()
			hsv = getHSVFrame(frame)
			
			ball_pos, ball_radius = findBall(hsv)
			if ball_pos:
				cv2.circle(overlayedFrame, ball_pos, ball_radius, (0, 255, 0), 2)

			goal_y_pos, goal_y_dimensions = findYGoal(hsv)
			if goal_y_pos:
				cv2.circle(overlayedFrame, goal_y_pos, 5, (0, 0, 255), 5)

			goal_b_pos, goal_b_dimensions = findBGoal(hsv)
			if goal_b_pos:
				cv2.circle(overlayedFrame, goal_b_pos, 5, (0, 0, 255), 5)
				
			#cv2.imshow('image', overlayedFrame)

			key = cv2.waitKey(1)
			rawCapture.truncate(0)

			try:
				
				#print("compassInitial   {}".format(compassInitial))
				#print("compassReadAngle {}".format(compass.readAngle()))
				#print("compassRelative  {}".format(goalComDir()))
				print("momentarySwitch  {}".format(momentary.read()))

				sleepdur = 0.4
				"""if botMode == 0:
					attack()

				elif botMode == 1:
					defend()"""

				# Go to ball test
				print("ballPos {}".format(ball_pos))

				if ball_pos:
					if ball_pos[0] < 150:
						motors.rotateCenter(-1,50)
						time.sleep(0.2)
						motors.stop()
						print("left")
					elif ball_pos[0] > 170:
						motors.rotateCenter(1,50)
						time.sleep(0.2)
						motors.stop()
						print("right")
					else:
						motors.goStraight(50)
						time.sleep(3)
						print("straight")
				else:
					motors.rotateCenter(-1,50)
					time.sleep(0.2)
					motors.stop()
					time.sleep(0.2)

				"""if ball_pos:
					if ball_pos[0] < 150:
						motors.rotateCenter(-1, 10)
					elif ball_pos[0] > 170:
						motors.rotateCenter(1, 10)
					else:
						motors.goStraight(10)
				"""
				print("loop")

			except KeyboardInterrupt:
				motors.stop()

	except:
		pass