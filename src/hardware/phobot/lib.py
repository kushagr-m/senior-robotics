def circularRound(inValue, nearest = 45):
    while (inValue >= 360):
        inValue -= 360
    return (round(inValue/nearest)*nearest)
