from enum import Enum

class Compass:
    def heading(self):
        return 0
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
compass = Compass()

class Pi:
    def momentary(self):
        return False

    def momentary_reset(self):
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

class Motors:
    def stop(self):
        pass

    def goStraight(self, power = 100):
        pass

    def goLeft(self, power = 100):
        pass

    def goRight(self, power = 100):
        pass

    def goBack(self, power = 100):
        pass

    def goFR(self, power = 100):
        pass

    def goFL(self, power = 100):
        pass

    def goBR(self, power = 100):
        pass

    def goBL(self, power = 100):
        pass

    def rotateCenter(self, direction = -1, power = 100):
        pass

    def rotateFrAxis(self, direction = -1, power = 100):
        pass
            
    def cleanup(self):
        pass
motors = Motors()