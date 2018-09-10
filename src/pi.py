import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  

momentary_port = 16

GPIO.setup(momentary_port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def momentary():
	switchStatus = not GPIO.input(momentary_port)
	return switchStatus