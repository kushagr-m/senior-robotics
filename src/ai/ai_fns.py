from ..main import *

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
