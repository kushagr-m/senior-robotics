import hw_motors as motors
#from hw_read import *

import hw_compass as compass

import hw_momentary as momentary

from ai_attack import *
from ai_defend import *

from time import sleep

botMode = 0
# 0 = attack
# 1 = defend

compass.initialise()
compassInitial = compass.readAngle()

def goalComDir():
	global compassInitial

	compassAngle = compass.readAngle()
	relativeDir = compassAngle-compassInitial
	
	if relativeDir<=-180:
		relativeDir+=360
	
	elif relativeDir>180:
		relativeDir-=360
		
	return relativeDir

while True:

	try:
		
		print("compassInitial   {}".format(compassInitial))
		print("compassReadAngle {}".format(compass.readAngle()))
		print("compassRelative  {}".format(goalComDir()))
		print("momentarySwitch  {}".format(momentary.read()))

		sleepdur = 0.4
			

		"""if botMode == 0:
			attack()

		elif botMode == 1:
			defend()"""
	
	except KeyboardInterrupt:
		motors.stop()