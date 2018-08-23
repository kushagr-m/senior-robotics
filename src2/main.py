#import hw_motors as motors
import hw_motors2 as motors
#from hw_read import *

# import hw_compass as compass

import hw_momentary as momentary
from hw_vision import *
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

ball_pos = (0, 0)
ball_radius = 0
goal_y_pos = (0, 0)
goal_y_dimensions = 0
goal_b_pos = (0, 0)
goal_b_dimensions = 0

while True:
	try:
		global frame
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
			
		cv2.imshow('image', overlayedFrame)

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
					print("left")
				elif ball_pos[0] > 170:
					motors.rotateCenter(1,50)
					print("right")
				else:
					motors.goStraight(50)
					print("straight")
			else:
				motors.rotateCenter(-1,50)

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