from lib import *

# RAW
# power range: [-100,100]
# -ve: counterclockwise
# +ve: clockwise

def N(power = 100):
    print("N(",power,")",sep='')
    return

def E(power = 100):
    print("E(",power,")",sep='')
    return

def S(power = 100):
    print("S(",power,")",sep='')
    return

def W(power = 100):
    print("W(",power,")",sep='')
    return

# Reset (stop all movement)
def stop():
    N(0)
    E(0)
    S(0)
    W(0)
    return

# direction = clockwise degrees between [0,359]
# power = between [-100,100]
def direction(direction, power = 100):
    direction = circularRound(direction,45)
    stop()
    if direction == 45:
        S(power)
        W(-1*power)
    elif direction == 90:
        N(-1*power)
        S(power)
    elif direction == 135:
        N(-1*power)
        W(power)
    elif direction == 180:
        E(-1*power)
        W(power)
    elif direction == 225:
        N(power)
        E(-1*power)
    elif direction == 270:
        N(power)
        S(-1*power)
    elif direction == 315:
        E(power)
        S(-1*power)
    else:
        E(power)
        W((-1*power))
    return direction