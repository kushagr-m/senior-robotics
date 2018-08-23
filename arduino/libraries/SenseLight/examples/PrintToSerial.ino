#include "SenseLight.h"

SenseLight LightSensor(A0, 7); // (Analog Input, Enable Pin)

void setup() {
  Serial.begin(9600);
}

void loop() {
  LightSensor.refresh(); // Read from the analog input
  Serial.println(LightSensor.get());
  delay(100);
}