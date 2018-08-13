import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  

gpioPort = 16

GPIO.setup(gpioPort, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read(gpioPort = 16):
	switchStatus = not GPIO.input(gpioPort)
	return switchStatus