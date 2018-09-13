import RPi.GPIO as GPIO           # import RPi.GPIO module  
from enum import Enum
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  

momentary_port = 16
LED_R_PORT = 25
LED_G_PORT = 8
LED_B_PORT = 7

GPIO.setup(momentary_port, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def momentary():
	return not GPIO.input(momentary_port)

class LEDColours(Enum):
	red = [True, False, False]
	green = [False, True, True]
	blue = [False, False, True]
	yellow = [True, True, False]
	cyan = [False, True, True]
	magenta = [True, False, True]
	white = [True, True, True]
	none = [False, False, False]

GPIO.setup(LED_R_PORT, GPIO.OUT)
GPIO.setup(LED_G_PORT, GPIO.OUT)
GPIO.setup(LED_B_PORT, GPIO.OUT)
def status_led(colour = LEDColours.none):
	states = colour.value
	GPIO.output(LED_R_PORT, GPIO.HIGH if states[0] else GPIO.LOW)
	GPIO.output(LED_B_PORT, GPIO.HIGH if states[1] else GPIO.LOW)
	GPIO.output(LED_G_PORT, GPIO.HIGH if states[2] else GPIO.LOW)

