import RPi.GPIO as GPIO           # import RPi.GPIO module  
from enum import Enum
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  

MOMENTARY_PORT = 17
MOMENTARY_RESET_PORT = 4
LED_R_PORT = 23
LED_G_PORT = 24
LED_B_PORT = 25

GPIO.setup(MOMENTARY_PORT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def momentary():
	return not GPIO.input(MOMENTARY_PORT)

GPIO.setup(MOMENTARY_RESET_PORT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def momentary_reset():
	return not GPIO.input(MOMENTARY_RESET_PORT)

class LEDColours(Enum):
	red     = [True,  False, False]
	green   = [False, True,  False]
	blue    = [False, False, True]
	yellow  = [True,  True,  False]
	cyan    = [False, True,  True]
	magenta = [True,  False, True]
	white   = [True,  True,  True]
	none    = [False, False, False]

GPIO.setup(LED_R_PORT, GPIO.OUT)
GPIO.setup(LED_G_PORT, GPIO.OUT)
GPIO.setup(LED_B_PORT, GPIO.OUT)
def status_led(colour = LEDColours.none):
	states = colour.value
	GPIO.output(LED_R_PORT, GPIO.HIGH if states[0] else GPIO.LOW)
	GPIO.output(LED_G_PORT, GPIO.HIGH if states[1] else GPIO.LOW)
	GPIO.output(LED_B_PORT, GPIO.HIGH if states[2] else GPIO.LOW)

