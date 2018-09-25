/*
  There is no tilt compensation, so make sure compass is aligned correctly, and stable!
*/

#include <Wire.h>

#define HMC5883L_ADDRESS 0x1E
#define HMC5883L_DEFAULT_ADDRESS 0x1E

int trigPinX = 11;
int echoPinX = 12;
long durationX, cmX;

int trigPinY = 2;
int echoPinY = 3;
long durationY, cmY;

void distanceX() {
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trigPinX, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinX, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinX, LOW);

  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPinX, INPUT);
  durationX = pulseIn(echoPinX, HIGH);

  cmX = (durationX / 2) / 29.1;
}

void distanceY() {
  digitalWrite(trigPinY, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPinY, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinY, LOW);

  pinMode(echoPinY, INPUT);
  durationY = pulseIn(echoPinY, HIGH);

  cmY = (durationY / 2) / 29.1;
}

void setup() {
  //Initialize Serial and I2C communications
  Serial.begin(9600);
  Wire.begin();
  //Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(HMC5883L_ADDRESS); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();

  pinMode(trigPinX, OUTPUT);
  pinMode(echoPinX, INPUT);
  pinMode(trigPinY, OUTPUT);
  pinMode(echoPinY, INPUT);
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

  distanceX();
  distanceY();

  Serial.print("x: ");
  Serial.print(x);
  Serial.print(" | y: ");
  Serial.print(y);
  Serial.print(" | z: ");
  Serial.print(z);
  Serial.print(" || ");
  Serial.print(cmX);
  Serial.print("cm | ");
  Serial.print(cmY);
  Serial.print("cm");
  Serial.println();
  delay(250);
}
