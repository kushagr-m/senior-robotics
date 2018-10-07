from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

board = PyMata3(com_port="/dev/ttyUSB0")
board.set_pin_mode(0, Constants.ANALOG)
def heading():
    return board.analog_read(0)

def difference(a, b, direction=1):
    if direction == 1:
        # Turning clockwise
        if b > a:
            return b - a
        else:
            return 360 - a + b
    else:
        # Turning anticlockwise
        if b < a:
            return a - b
        else:
            return 360 - b + a

calibration_point = 0
def calibrate():
    global calibration_point
    calibration_point = heading()

def calibratedHeading():
    # Get heading from the calibration point betweren -180 and 180
    global calibration_point
    diff = difference(calibration_point, heading())
    if diff > 180:
        return -(360 - diff)
    else:
        return diff