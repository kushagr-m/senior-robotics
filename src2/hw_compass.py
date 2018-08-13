import smbus2 as smbus
import math

#some MPU6050 Registers and their Address
Register_A     = 0              #Address of Configuration register A
Register_B     = 0x01           #Address of configuration register B
Register_mode  = 0x02           #Address of mode register

X_axis_H    = 0x03              #Address of X-axis MSB data register
Z_axis_H    = 0x05              #Address of Z-axis MSB data register
Y_axis_H    = 0x07              #Address of Y-axis MSB data register
declination = 11.62             #define declination angle of location where measurement going to be done
pi          = 3.14159265359     #define pi value

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x1e   # HMC5883L magnetometer device address

def initialise():
	# write to register 4
	bus.write_byte_data(Device_Address, Register_A, 0x70)
    #Write to Configuration Register B for gain
	bus.write_byte_data(Device_Address, Register_B, 0xa0)
    #Write to mode Register for selecting mode
	bus.write_byte_data(Device_Address, Register_mode, 0)
	return

def readRaw(addr):

	#Read raw 16-bit value
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)

    #to get signed value from module
    if(value > 32768):
        value = value - 65536
    return value

initialise()

def readAngle():
	x = readRaw(X_axis_H)
	z = readRaw(Z_axis_H)
	y = readRaw(Y_axis_H)

	heading = math.atan2(y, x) + declination

	heading=heading%(2*pi)

	#convert into angle
	headingAngle = int(heading * 180/pi)
	return headingAngle

#while True:
#	print("Heading: " + str(readAngle()), flush=True)