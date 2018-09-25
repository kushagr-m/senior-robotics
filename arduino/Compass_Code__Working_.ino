/*
  There is no tilt compensation, so make sure compass is aligned correctly, and stable!
*/

#include <Wire.h>

#define HMC5883L_ADDRESS 0x1E
#define HMC5883L_DEFAULT_ADDRESS 0x1E

void setup() {
  //Initialize Serial and I2C communications
  Serial.begin(9600);
  Wire.begin();
  //Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(HMC5883L_ADDRESS); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();
}

void loop() {
  int x, y, z; //triple axis data

  //Tell the HMC5883 where to begin reading data
  Wire.beginTransmission(HMC5883L_ADDRESS);
  Wire.write(0x03); //select register 3, X MSB register
  Wire.endTransmission();

  //Read data from each axis, 2 registers per axis
  Wire.requestFrom(HMC5883L_ADDRESS, 6);
  if (6 <= Wire.available()) {
    x = Wire.read() << 8; //X msb
    x |= Wire.read(); //X lsb
    z = Wire.read() << 8; //Z msb
    z |= Wire.read(); //Z lsb
    y = Wire.read() << 8; //Y msb
    y |= Wire.read(); //Y lsb
  }

  // Quick Fix from steelgoose
  if (x > 32767)
    x = x - 65536;
  if (y > 32767)
    y = y - 65536;
  if (z > 32767)
    z = z - 65536;

  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.print(z);
  Serial.println();
  delay(250);
}
