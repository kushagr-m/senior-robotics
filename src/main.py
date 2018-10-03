from threaded.vision import VisionProcess
import time
import cv2 as cv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', default=0, type=int, dest='debug_level', help='The debug level to use (0-2). [Default = 0]')
parser.add_argument('-q', '--quiet-mode', default=False, type=bool, dest='quiet_mode', help='Disables all movement [Default = False]')
parser.add_argument('-s', '--go-straight', default=False, type=bool, dest='go_straight', help='Go straight if the ball is straight ahead. [Default = False]')
parser.add_argument('-c', '--center-padding', default=80, type=int, dest='center_padding', help='how many pixels either side of the middle is the ball in the center [Default=80]')
parser.add_argument('-o', '--out-of-frame', default=False, type=bool, dest='out_of_frame', help='Rotate if the ball is out of frame? [Default=False]')
args = parser.parse_args()

print('USE ARGUMENTS PLEASE')
time.sleep(0.2)

DEBUG_LEVEL = args.debug_level
quiet_mode = args.quiet_mode

try:
	if not quiet_mode: 
		import motors
		import pi
	else:
		print('Quiet mode was enabled. Disabling Pi-specific functions.')
		from stubs import *
except ImportError:
	quiet_mode = True
	print('Failed to import motors.py and pi.py.\nQuiet mode was enabled. Disabling Pi-specific functions.')
	from stubs import *

print('Debug level:',debug_level)

# start vision process
vp = VisionProcess().start()

print('Started main script.')

# calibration stuffs
ballCenterPadding = args.center_padding

try:
	
	while True:
		ballDetected, ballCenter, queue = vp.read()
		hsvatBallCenter, currentFPS = vp.readDebug()
		print(ballDetected,ballCenter,currentFPS)

		if not quiet_mode and pi.momentary():

			if ballDetected:

				if abs(ballCenter[0]) <= ballCenterPadding:
					if args.go_straight:
						motors.goStraight(60)
				elif ballCenter[0] > 0:
					motors.rotateCenter(direction=1,power=60)
				elif ballCenter[0] < 0:
					motors.rotateCenter(direction=-1,power=60)

			elif args.out_of_frame:
				
				if queue[-1][0] > 0:
					motors.rotateCenter(direction=1,power=60)
				elif queue[-1][0] < 0:
					motors.rotateCenter(direction=-1,power=60)


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