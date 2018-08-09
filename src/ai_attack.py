from main import *

def attack():
    #attacker loop

    """
    OBJECTIVE = GET IN LINE WITH THE BALL AND THE GOAL, GO TOWARDS GOAL
    FACE BALL AT ALL TIMES
    """

    # if we have the ball
    if read.momentary():

        if goalCenter is not None:
            # if goal is in view

            if goalCVDir() == 0:
                motors.goStraight()

            elif goalCVDir() == 1:
                motors.rotateFrAxis("left")

            elif goalCVDir() == -1":
                motors.rotateFrAxis("right")


        else:
            # if goal is not in view
            
            if goalComDir()>0:
                motors.rotateFrAxis("left")

            elif goalComDir()<0:
                motors.rotateFrAxis("right")


    if ballDirection() == -1:
        motors.rotateCenter("left")

    elif ballDirection() == 1:
        motors.rotateCenter("right")

    else:

        if ballRadius>ballCloseRadius:
            motors.goStraight()

        else:

            if goalComDir()>30:
                motors.goFL()

            elif goalComDir()<-30:
                motors.goFR()

            elif abs(goalComDir())<30:
                motors.goStraight()

    return