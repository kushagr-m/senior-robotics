from calibrationSetting import *

def circularRound(inValue, nearest = 45):
    while (inValue >= 360):
        inValue -= 360
    return (round(inValue/nearest)*nearest)

ballCloseRadius = 40
#radius of the ball being close

def ballDirection():
    if ((frameDimensions[0] - ballCenterPadding)/2 < ballCenter[0] < (frameDimensions[0] + ballCenterPadding)/2):
        return 0
    elif (ballCenter[0] > (frameDimensions[0]/2)):
        return 1
    elif (ballCenter[0] < (frameDimensions[0]/2)):
        return -1
    else: 
        pass

goalDirPadding = 10

def goalComDir(compassInitial, dataCompass):

    relativeDir = dataCompass-compassInitial

    if relativeDir<-179:
        relativeDir+=360

    elif relativeDir>180:
        relativeDir-=360
        
    return relativeDir

goalCenterPadding = 10

def goalCVDir():

    if ((frameDimensions[0] - goalCenterPadding)/2 < goalCenter[0] < (frameDimensions[0] + goalCenterPadding)/2):
        return 0
    elif (goalCenter[0] > (frameDimensions[0]/2)):
        return 1
    elif (goalCenter[0] < (frameDimensions[0]/2)):
        return -1
    else: 
        pass

def attack():
    #attacker loop

    """
    OBJECTIVE = GET IN LINE WITH THE BALL AND THE GOAL, GO TOWARDS GOAL
    FACE BALL AT ALL TIMES
    """

    # if we have the ball
    if dataSwitch:

        if goalCenter is not None:
            # if goal is in view

            if goalCVDir() == 0:
                motors.goStraight()

            elif goalCVDir() == 1:
                motors.rotateFrAxis("left")

            elif goalCVDir() == -1:
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

def defend():

	# defender always faces ball
	 # if we see the ball
	if ballCenter is not None:

		if ballDirection() == 0:
			motors.goStraight()

		elif ballDirection() == -1:
			motors.goLeft()

		elif ballDirection() == 1:
			motors.goRight()

	return