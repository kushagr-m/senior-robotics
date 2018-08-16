## Components
- **Raspberry Pi 2 Model B+:** The brains for OpenCV and logic
  - **Raspberry Pi Camera Board 2:** To see
  - **HMC5833 Digital Compass:** To find angle to goal, communicates over i2c
  - **VL53L0X Time of Flight Sensors:** 4x, to find distance to edges
  - **SENSELIGHT v1 (TRIS10) Colour Sensors:** 4x, to detect field boundaries
  - **Momentary Switch:** To detect when ball is in contact with robot when out of camera view
  - **SPST Switch:** To turn off robot, or at least pause the code
  - **RGB LED:** FOr visual status codes
- **Arduino MEGA R3 2560**: Generates PWM signals to control motor drivers, communicates over serial
  - **L298N Dual H-Bridge Motor Driver:** 2x, uses PWM signals to control voltage to motors, has on board 5V regulator
    - **6V 294RPM Motors:** 4x, To move the robot
    - **42mm Omdirectional Wheels:** 4x, to enable omnidirectional movement
  - **RGB LED:** For visual status codes
- **Logic Level Converter:** Enables bidirectional communication over serial, converts 5V and 3.3V into each other for Arduino and Raspberry Pi
- **5V Converter:** Converts battery voltage to stable 5V to power Raspberry Pi
- **Zippy 5000 20C Li-Po Battery 7.4V:** Powers everything

----
## Schematic and PCB design
_See `/plans` for link to Upverter project, final schematic and PCB designs uploaded when complete_

----
## Other
- Print PCB as plates
- Have a way to turn on and off the robot without a computer
- Have status codes with RGB LEDs
- Do not have plates in red or colour similar to ball
