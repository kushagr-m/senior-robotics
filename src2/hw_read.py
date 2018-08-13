import serial
ser = serial.Serial('/dev/ttyACM0',115200) # change to ACM1 if that is the USB port

def readSerial():

	# vv UNCOMMENT WHEN TOF vv
	#global data1TOF
	#global data2TOF
	#global data3TOF
	#global data4TOF

	global dataSwitch
	global dataCompass

	readSerial=ser.readline() # reads from serial until EOL character received - i.e. \n
	
	#if '1:' in readSerial: # Time of Flight sensors VV
	#    data1TOF = readSerial
	#elif '2:' in readSerial:
	#    data2TOF = readSerial
	#elif '3:' in readSerial:
	#    data3TOF = readSerial
	#elif '4:' in readSerial:
	#    data4TOF = readSerial
	# 
		
	if 'HIGH' in readSerial: # Momentary switch to detect ball VV
		dataSwitch = True
	elif 'LOW' in readSerial:
		dataSwitch = False
	else: # The only thing else that readSerial can be
		dataCompass = int(readSerial)

	return