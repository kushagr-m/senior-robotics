def circularRound(inValue, nearest = 45):
    while (inValue >= 360):
        inValue -= 360
    return (round(inValue/nearest)*nearest)

nPower = 0
ePower = 0
sPower = 0
wPower = 0

# RAW
# power range: [-100,100]
# -ve: counterclockwise
# +ve: clockwise

def N(power = 100):
    # set N power
    nPower = power
    print("N(",power,")",sep='')
    return

def E(power = 100):
    # set E power
    ePower = power
    print("E(",power,")",sep='')
    return

def S(power = 100):
    # set S power
    sPower = power
    print("S(",power,")",sep='')
    return

def W(power = 100):
    # set W power
    wPower = power
    print("W(",power,")",sep='')
    return

# disastrous function doesnt work
def getCurrent(whichWheel):
    if whichWheel is None:
        pass
    elif whichWheel == "N":
        return nPower
    elif whichWheel == "E":
        return ePower
    elif whichWheel == "S":
        return sPower
    elif whichWheel == "W":
        return wPower
    else:
        pass

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
    print("dir: ",direction)
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
    return