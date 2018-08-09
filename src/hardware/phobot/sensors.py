import serial
ser = serial.Serial('/dev/ttyACM0',115200) # change to ACM1 if that is the USB port

def readSerial():
    readSerial=ser.readline() # reads from serial until EOL character received - i.e. \n
    
    dataCompass = readSerial # remove line ToF sensors are installed
    
    # V BELOW V Remove #hashtags once ToF sensors are installed o differentiate serial data from Arduino
   #if '1:' in readSerial:
   #    data1TOF = readSerial
   #elif '2:' in readSerial:
   #    data2TOF = readSerial
   #elif '3' in readSerial:
   #    data3OF = readSerial
   #elif '4' in readSerial:
   #    data4OF = readSerial
   #else:
   #    dataCompass = readSerial
