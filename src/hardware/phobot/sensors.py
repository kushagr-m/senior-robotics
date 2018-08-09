import serial
ser = serial.Serial('/dev/ttyACM0',115200) # change to ACM1 if that is the USB port

def readSerial():
    readSerial=ser.readline() # reads from serial until EOL character received - i.e. \n
    
    if ':' in readSerial:
        dataTOF = readSerial
    else:
        dataCompass = readSerial