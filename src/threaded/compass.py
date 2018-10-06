import smbus2 as smbus
import math
from threading import Thread
from time import sleep

#some MPU6050 Registers and their Address
Register_A     = 0              #Address of Configuration register A
Register_B     = 0x01           #Address of configuration register B
Register_mode  = 0x02           #Address of mode register

X_axis_H    = 0x03              #Address of X-axis MSB data register
Z_axis_H    = 0x05              #Address of Z-axis MSB data register
Y_axis_H    = 0x07              #Address of Y-axis MSB data register
declination = 11.62             #define declination angle of location where measurement going to be done
pi          = 3.14159265359     #define pi value

Device_Address = 0x1e   # HMC5883L magnetometer device address

class CompassProcess:
    def __init__(self):
        print("CompassProcess: Initialising")

        self.stopped = False
        self.bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards

        # write to register 4
        self.bus.write_byte_data(Device_Address, Register_A, 0x70)
        #Write to Configuration Register B for gain
        self.bus.write_byte_data(Device_Address, Register_B, 0xa0)
        #Write to mode Register for selecting mode
        self.bus.write_byte_data(Device_Address, Register_mode, 0)

        self.headingAngle = 0

    def readRaw(self, addr):
        #Read raw 16-bit value
        high = self.bus.read_byte_data(Device_Address, addr)
        low = self.bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from module
        if(value > 32768):
            value = value - 65536
        return value

    def readAngle(self):
        return self.headingAngle

    def start(self):
        t = Thread(target=self.Process,args=(),name='CompassProcess')
        t.daemon = True
        t.start()
        print("CompassProcess: Started.")
        return self

    def stop(self):
        self.stopped = True

    def Process(self):
        while not self.stopped:
            x = self.readRaw(X_axis_H)
            #z = self.readRaw(Z_axis_H)
            y = self.readRaw(Y_axis_H)

            heading = math.atan2(y, x) + declination
            heading = heading%(2*pi)

            self.headingAngle = heading

            sleep(0.1)

        self.bus.close()
        print("CompassProcess: Stopped.")