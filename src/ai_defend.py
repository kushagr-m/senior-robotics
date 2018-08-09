from main import *

def defend():

    # defender always faces ball
     # if we see the ball
    elif ballCenter is not None:

        if ballDirection() == 0:
            motor.goStraight()

        elif ballDirection() == -1:
            motors.goLeft()

        elif ballDirection() == 1:
            motors.goRight()

    return