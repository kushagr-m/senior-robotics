from threaded.vision import VisionProcess
from time import sleep
import cv2 as cv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', default=0, type=int, dest='debug_level', help='The debug level to use (0-2). Default is 0.')
args = parser.parse_args()

DEBUG_LEVEL = args.debug_level

try:
    #import compass
    import pi
    import motors
except ImportError:
    print("Disabling Pi specific functions")
    from stubs import *

vp = VisionProcess().start()

try:
    print("Started MAIN SCRIPT")

    moveBot = True
    ballDirection = 1
    ballLastXPos = 0

    while True:
        ballDetected, ballCenter, queue = vp.read()
        print(ballDetected, ballCenter)
        
        moveBot = pi.momentary()
        if moveBot: # motors and shit
            centrePadding = 80

            if ballDetected:
                ballXPos = ballCenter[0]
                ballDirection = -1 if ballLastXPos - ballXPos < 0 else 1
                ballLastXPos = ballXPos

                if abs(ballXPos) <= centrePadding:
                    motors.stop()
                    #sleep(0.3)
                    #motors.goStraight(50)
                    #sleep(0.3)
                elif ballXPos > 0:
                    motors.rotateCenter(direction = 1, power = 50)
                elif ballXPos < 0:
                    motors.rotateCenter(direction = -1, power = 50)

            else:
                motors.rotateCenter(direction = ballDirection, power = 45)
        else:
            motors.stop()
        
        # Debug
        if DEBUG_LEVEL > 0:
            OutputFrames = vp.OutputFrame()
            outlineCenter, outlineRadius = vp.minEnclosing()

            if OutputFrames[0] is not None:
                CameraOutput = OutputFrames[0]

                if ballCenter is not None:
                    absoluteBallCenter = (ballCenter[0] + 160, ballCenter[1] + 120)
                    cv.circle(CameraOutput, absoluteBallCenter, 4, (255,0,0), -1)	
                    outlineCenterint = (int(outlineCenter[0]),int(outlineCenter[1]))
                    cv.circle(CameraOutput, outlineCenterint, int(outlineRadius), (0,255,0), 3)
                    cv.putText(CameraOutput, str(ballCenter),(int(absoluteBallCenter[0]+(outlineRadius/90)),int(absoluteBallCenter[1]+(outlineRadius/40))),cv.FONT_HERSHEY_DUPLEX,(outlineRadius/100)+0.3,(255,255,255),int((outlineRadius/80)+0.3))		
                
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