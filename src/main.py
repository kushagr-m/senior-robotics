from threaded.vision import VisionProcess
import time
import cv2 as cv
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', default=0, type=int, dest='debug_level', help='The debug level to use (0-2). [Default = 0]')
parser.add_argument('-q', '--quiet-mode', default=False, type=bool, dest='quiet_mode', help='Disables all movement [Default = False]')
parser.add_argument('-s', '--go-straight', default=False, type=bool, dest='go_straight', help='Go straight if the ball is straight ahead. [Default = False]')
parser.add_argument('-c', '--center-padding', default=140, type=int, dest='center_padding', help='how many pixels either side of the middle is the ball in the center [Default=80]')
parser.add_argument('-o', '--out-of-frame', default=False, type=bool, dest='out_of_frame', help='Rotate if the ball is out of frame? [Default=False]')
args = parser.parse_args()

print('USE ARGUMENTS PLEASE')
time.sleep(0.2)

DEBUG_LEVEL = args.debug_level
quiet_mode = args.quiet_mode

try:
	if not quiet_mode: 
		import pi
		import motors
		import compass
	else:
		print('Quiet mode was enabled. Disabling Pi-specific functions.')
		from stubs import *
except ImportError:
	quiet_mode = True
	print('Failed to import motors.py and pi.py.\nQuiet mode was enabled. Disabling Pi-specific functions.')
	from stubs import *

print('Debug level:',DEBUG_LEVEL)

# start vision process
vp = VisionProcess().start()

print('Started main script.')

# calibration stuffs
ballCenterPadding = 140 #args.center_padding

lastSwitchState = pi.momentary()
compass_correcting = 0

try:

	state = "start"
	
	while True:
		ballDetected, ballCenter, queue, ballArea = vp.read()
		hsvatBallCenter, currentFPS, maxVal = vp.readDebug()
		print(ballDetected,ballCenter, ballArea, hsvatBallCenter, currentFPS,'fps',state)

		if not quiet_mode:
			if pi.momentary():
				if lastSwitchState == False:
					compass.calibrate()
				lastSwitchState = True

				# heading = compass.calibratedHeading()
				# if heading < 30 or compass_correcting == -1:
				# 	motors.rotateCenter(direction=1, power=60)
				# 	compass_correcting = -1
				# 	if heading < 0:
				# 		continue
				# 	motors.stop()
				# 	compass_correcting = 0
				# if heading > 30 or compass_correcting == 1:
				# 	motors.rotateCenter(direction=-1, power=60)
				# 	compass_correcting = 1
				# 	if heading > 0:
				# 		continue
				# 	motors.stop()
				# 	compass_correcting = 0

				if ballDetected is True:

					if ballArea > 2000000:
						state = "got ball"
						currentBearing = compass.calibratedHeading()
						compassDeadzone = 45

						if abs(currentBearing) <= compassDeadzone:
							state = "straight goal ball"
							motors.goStraight(100)
						elif currentBearing > 0:
							motors.rotateFrAxis(direction = 1, power = 70)
						elif currentBearing < 0:
							motors.rotateFrAxis(direction = -1, power= 70)
							
					else:
						state = "finding"
						if abs(ballCenter[0]) <= ballCenterPadding:
							motors.goStraight(60)
						elif ballCenter[0] > 0:
							motors.rotateCenter(direction=1,power=100)
							time.sleep(0.01)
							motors.rotateCenter(direction=1,power=50)
						elif ballCenter[0] < 0:
							motors.rotateCenter(direction=-1,power=100)
							time.sleep(0.01)
							motors.rotateCenter(direction=-1,power=50)

				elif args.out_of_frame or True:
					state = "blind"
					if len(queue) != 0:
						if queue[-1][0] > 0:
							motors.rotateCenter(direction=1,power=100)
							time.sleep(0.01)
							motors.rotateCenter(direction=1,power=50)
						elif queue[-1][0] <= 0:
							motors.rotateCenter(direction=-1,power=100)
							time.sleep(0.01)
							motors.rotateCenter(direction=-1,power=50)
					else:
						motors.rotateCenter(direction=1,power=80)
				else:
					motors.stop()
			else:
				motors.stop()
				lastSwitchState = False
				compass_correcting = 0

		# DEBUG
		if DEBUG_LEVEL > 0:
			OutputFrames = vp.OutputFrame()
			outlineCenter, outlineRadius = vp.minEnclosing()

			if OutputFrames[0] is not None:
				CameraOutput = OutputFrames[0]

				if ballCenter is not None and ballDetected:
					absoluteBallCenter = (ballCenter[0] + 160, ballCenter[1] + 120)
					cv.circle(CameraOutput, absoluteBallCenter, 4, (255,0,0), -1)	
					
				cv.imshow('Camera', CameraOutput)
			
			if DEBUG_LEVEL > 1:
				if OutputFrames[1] is not None:	
					cv.imshow('Grayscale Mask', OutputFrames[1])
				if OutputFrames[2] is not None:
					cv.imshow('ballCenter mask', OutputFrames[2])
				if OutputFrames[3] is not None:
					cv.imshow('hsv Mask', OutputFrames[3])
			
			if cv.waitKey(1) & 0xFF == ord('q'):
				break
	
except KeyboardInterrupt:
	print("Keyboard Interrupt")

# do a bit of cleanup
vp.stop()
motors.cleanup()
print("Script Ended Cleanly")