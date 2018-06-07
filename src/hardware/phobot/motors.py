def kRound(inValue, nearest = 45):
    return (round(inValue/nearest)*nearest)

# RAW
# power range: [-100,100]
# -ve: counterclockwise
# +ve: clockwise

def front(power = 100):
    print("front(",power,")",sep='')
    return

def back(power = 100):
    print("back(",power,")",sep='')
    return

def left(power = 100):
    print("left(",power,")",sep='')
    return

def right(power = 100):
    print("right(",power,")",sep='')
    return

# Helper functions
def stop():
    front(0)
    back(0)
    left(0)
    right(0)
    return


def directional(direction, power = 100):

    return

def goStraight(power = 100):
    stop()
    left((-1*power))
    right(power)
    return

def goLeft(power = 100):
    stop()
    front(power)
    back((-1*power))
    return

def goRight(power = 100):
    stop()
    front((-1*power))
    back(power)
    return