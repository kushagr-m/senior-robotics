import vision
import motors
from time import sleep

try:
    #import compass
    import pi
except ImportError:
    print("Disabling Pi specific functions")
    from stubs import *

moveBot = True

try:
    print("Started MAIN SCRIPT")

    ballDirection = 1
    ballLastXPos = 0
    while True:
        stop = vision.loop()
        if stop:
            break
        
        moveBot = pi.momentary()
        if moveBot: # motors and shit
            centrePadding = 80
            print(vision.getBallCenter())

            if vision.getBallCenter() is not None:
                ballXPos = vision.getBallCenter()[0]
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
                            
    # do a bit of cleanup
    vision.cleanup()
    motors.cleanup()
    print("Script Ended Cleanly")
    
except KeyboardInterrupt:
    vision.cleanup()
    motors.cleanup()
    print("Keyboard Interrupt/nCleaned")
