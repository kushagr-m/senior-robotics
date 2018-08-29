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

frame = None
ball_pos = (0, 0)
ball_radius = 0
goal_y_pos = (0, 0)
goal_y_dimensions = 0
goal_b_pos = (0, 0)
goal_b_dimensions = 0

def getBallPos():
	global ball_pos
	return ball_pos

def getBallRadius():
	global ball_radius
	return ball_radius

def getYGoalPos():
	global goal_y_pos
	return goal_y_pos

def getYGoalDimensions():
	global goal_y_dimensions
	return goal_y_dimensions

def getBGoalPos():
	global goal_b_pos
	return goal_b_pos

def getBGoalDimensions():
	global goal_b_dimensions
	return goal_b_dimensions

inv_gamma = 1.0 / gamma
gamma_table = np.array([((i / 255.0) ** inv_gamma) * 255
	for i in np.arange(0, 256)]).astype("uint8")

def getFrame(_frame = None):
	global frame
	if _frame is not None:
		frame = cv2.resize(_frame, frameDimensions)
	return frame

def getHSVFrame(frame):
	hsv = cv2.LUT(frame, gamma_table)
	hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (5, 5), 5)
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
	print("Start find ball")
	mask = cv2.inRange(hsvFrame, ballLower, ballUpper)
	mask = cv2.dilate(mask, None, iterations=3)
	print("FB: transformed")
	image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	print("FB: countours")
	if len(contours) > 0:
		c = max(contours, key=cv2.contourArea)
		
		area = cv2.contourArea(c)
		(x, y), radius = cv2.minEnclosingCircle(c)
		center = (int(x), int(y))
		radius = int(radius)
		print("FB: Found circle")

		cv2.circle(mask, center, radius, (255, 255, 255), 1)
		print("FB: Drew circle")
		#cv2.imshow('ballmask', mask)
		print("FB: Show mask")

		if (area / (math.pi * (radius ** 2))) > 0.75:
			return center, radius
	else:
		#cv2.imshow('ballmask', mask)
		print("FB: No mask")
	
	return None, None

"""
findGoal()

Inputs:  hsvFrame   - a frame in the HSV colour space
Outputs: center     - A (x, y) tuple representing the pixel coordinate of the center of the goal
		 dimensions - A (width, height) tuple representing the pixel size of the goal

		 Output is 'None, None' if a goal is not detected
"""
cv2.namedWindow('goalymask', cv2.WINDOW_NORMAL)
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
	cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

cv2.namedWindow('goalbmask', cv2.WINDOW_NORMAL)
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

def start_cv():

	global ball_pos
	global ball_radius
	global goal_y_pos
	global goal_y_dimensions
	global goal_b_pos
	global goal_b_dimensions

	global camera
	global rawCapture

	try:
		for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			global frame
			frame = getFrame(_frame.array)

			if frame is None:
				print("no frame")
				continue
			print("frame")
			overlayedFrame = frame.copy()
			hsv = getHSVFrame(frame)
			print("getframe")
			
			ball_pos, ball_radius = findBall(hsv)
			if ball_pos:
				cv2.circle(overlayedFrame, ball_pos, ball_radius, (0, 255, 0), 2)
			print("found ball")
			goal_y_pos, goal_y_dimensions = findYGoal(hsv)
			if goal_y_pos:
				cv2.circle(overlayedFrame, goal_y_pos, 5, (0, 0, 255), 5)
			print("found y")
			goal_b_pos, goal_b_dimensions = findBGoal(hsv)
			if goal_b_pos:
				cv2.circle(overlayedFrame, goal_b_pos, 5, (0, 0, 255), 5)
			
			print("preshow")
			#cv2.imshow('image', overlayedFrame)
			print("show")
			rawCapture.truncate(0)
			print("prewait")
			#cv2.waitKey(1)
			print("postwait")

		print("done")

	except KeyboardInterrupt:
		print('Stopping CV')
		cv2.destroyAllWindows()

	print("crash")

t = threading.Thread(target=start_cv)
t.daemon = True
t.start()