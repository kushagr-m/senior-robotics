# senior-robotics
arduino code for robocup soccer open division

## team:
- john
- elvis
- leon
- ben
- angus
- kush

### Todo:
- [ ] work out algorithms to figure out ball position and movement
- [ ] work out how to react to the ball position
- [ ] work out horizontal position of the bot for nudges etc

### Reminders:
- Check wheel clockwise spin direction - if not, edit `/arduino/arduino.ino` and change ints *RATHER THAN rewiring*
- Check if RPi can send data to Arduino, and vice versa
- If ToF sensors to be installed, change compass' SCL and SDA pins to breadboard, and connect ToFs' to same line. All to connect to pins 20 and 21 on Arduino
- If ToF sensors installed, edit `/arduino/arduino.ino` and `/src/hardware/phobot/sensors.py` according to instructory comments
