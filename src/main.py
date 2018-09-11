import vision
import motors

try:
    #import compass
    import pi
except ImportError:
    print("Disabling Pi specific functions")
    from stubs import *

moveBot = True

try:
    print("Started MAIN SCRIPT")

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

                if abs(ballXPos) <= centrePadding:
                    motors.goStraight(50)
                elif ballXPos > 0:
                    motors.rotateCenter(direction = 1, power = 50)
                elif ballXPos < 0:
                    motors.rotateCenter(direction = -1, power = 50)

            else:
                pass#motors.rotateCenter(direction = 1, power = 50)
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
