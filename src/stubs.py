from enum import Enum

class Compass:
    def readAngle(self):
        return 0
compass = Compass()

class Pi:
    def momentary(self):
        return False

    class LEDColours(Enum):
        red = [True, False, False]
        green = [False, True, True]
        blue = [False, False, True]
        yellow = [True, True, False]
        cyan = [False, True, True]
        magenta = [True, False, True]
        white = [True, True, True]
        none = [False, False, False]

    def status_led(self, colour):
        pass
pi = Pi()

