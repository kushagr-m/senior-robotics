import serial
ser = serial.Serial('/dev/ttyACM0',115200) # change to ACM1 if that is the USB port

def readSerial():
    readSerial=ser.readline() # reads from serial until EOL character received - i.e. \n

   if '1:' in readSerial: # Time of Flight sensors VV
       data1TOF = readSerial
   elif '2:' in readSerial:
       data2TOF = readSerial
   elif '3' in readSerial:
       data3OF = readSerial
   elif '4' in readSerial:
       data4OF = readSerial
   elif 'HIGH' in readSerial: # Momentary switch to detect ball VV
       dataSwitch = readSerial
   elif 'LOW' in readSerial:
       dataSwitch = readSerial
   else: # The only thing else that readSerial can be
       dataCompass = readSerial
