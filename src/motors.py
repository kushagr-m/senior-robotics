import math
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants as PyMataConstants

# Motor pins
motors = [
    (5, 4), # FL
    (3, 2), # FR
    (10, 9), # BL
    (12, 11), # BR
    (6, 7) # Dribbler
]

current_power = [ 0, 0, 0, 0, 0 ]

board = PyMata3(com_port="/dev/ttyS0")
# board = PyMata3()

# Set up motor output pins
for motor in motors:
    board.set_pin_mode(motor[0], PyMataConstants.PWM)
    board.set_pin_mode(motor[1], PyMataConstants.PWM)

def set_motor(motor, power = 100):
    if current_power[motor] != power:
        current_power[motor] = power
        scaled_power = math.floor(abs(power) * 2.55)
        print("Set motor ", motor, scaled_power)

        if power > 0:
            board.analog_write(motors[motor][0], scaled_power)
            board.analog_write(motors[motor][1], 0)
        else:
            board.analog_write(motors[motor][0], 0)
            board.analog_write(motors[motor][1], scaled_power)

def FL(power):
    set_motor(0, power)

def FR(power):
    set_motor(1, power)

def BL(power):
    set_motor(2, power)

def BR(power):
    set_motor(3, power)

def Dribbler(power):
    set_motor(4, power)

def stop():
    FL(0)
    FR(0)
    BR(0)
    BL(0)
    Dribbler(0)

def goStraight(power = 100):
    FR(power)
    FL(-1*power)
    BR(power)
    #BR(0)
    BL(-1*power)
    #BL(0)

def goLeft(power = 100):
    FR(power)
    #FR(0)
    FL(power)
    BR(-1*power)
    #BR(0)
    BL(-1*power)

def goRight(power = 100):
    FR(-1*power)
    FL(-1*power)
    #FL(0)
    BR(power)
    BL(power)
    #BL(0)

def goBack(power = 100):
    FR(-1*power)
    #FR(0)
    FL(power)
    #FL(0)
    BR(-1*power)
    BL(power)

def goFR(power = 100):
    FL(-1*power)
    FR(0)
    BL(0)
    BR(power)

def goFL(power = 100):
    FL(0)
    FR(power)
    BL(-1*power)
    BR(0)

def goBR(power = 100):
    FL(0)
    FR(-1*power)
    BL(power)
    BR(0)

def goBL(power = 100):
    FL(power)
    FR(0)
    BL(0)
    BR(-1*power)

def rotateCenter(direction = -1, power = 100):
    if direction < 0:
        #FR(power)
        FR(0)
        FL(power)
        BR(power)
        #BL(power)
        BL(0)

    if direction > 0:
        #FR(-1*power)
        FR(0)
        FL(-1*power)
        BR(-1*power)
        #BL(-1*power)
        BL(0)

def rotateFrAxis(direction = -1, power = 100):
    if direction < 0:
        FR(0)
        FL(0)
        BR(-1*power)
        BL(-1*power)

    if direction > 0:
        FR(0)
        FL(0)
        BR(power)
        BL(power)
        
def reverse():
    for i in range(0, len(current_power)):
        set_motor(i, -current_power[i])


def cleanup():
    stop()

board.set_pin_mode(0, PyMataConstants.ANALOG)
def compassHeading():
    return board.analog_read(0)