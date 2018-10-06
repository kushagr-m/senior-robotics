import smbus2 as smbus
import math
from hmc5883l import hmc5883l
#from h2 import HMC5883L

declination = 11.62 #define declination angle of location where measurement going to be done
pi          = 3.14159265359

compass = hmc5883l()
# compass = HMC5883L(1)

xOffset = 0
yOffset = 0

calibrationData = []
isCalibrating = False
def calibrateStart():
    global isCalibrating
    global calibrationData

    calibrationData = []
    isCalibrating = True

def calibrateStop():
    global isCalibrating
    global calibrationData

    isCalibrating = False

    minX = math.inf
    minY = math.inf
    maxX = -math.inf
    maxY = -math.inf

    for i in range(0, len(calibrationData)):
        x, y, z = calibrationData[i]
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    
    xOffset = (minX + maxX) / 2
    yOffset = (minY + maxY) / 2
    
    calibrationData = []

headingAngle = 0
def readAngle():
    global headingAngle
    return headingAngle

def loop():
    global headingAngle
    (x, y, z) = compass.axes()
    # x = compass.get_field_x()
    # y = compass.get_field_y()
    # z = compass.get_field_z()

    if isCalibrating:
        calibrationData.append((x, y, z))

    #heading = math.atan2(x - xOffset, y - yOffset)
    #heading = heading%(2*pi)
    
    heading = (90 - math.atan2(y, x) * 180/pi) if y > 0 else (270 - math.atan2(y, x) * 180/pi)
    
    #convert into angle
    #headingAngle = (int(heading * 180/pi) + declination) % 360

    return headingAngle

#while True:
#	print("Heading: " + str(readAngle()), flush=True)
\

if __name__ == "__main__":
    while True:
        currentHeading = loop()
        print(currentHeading)