/*
   en is used for analog data from 0 to 255 (but is mapped, so 0-100 over serial comms)
   in is used for digital - HIGH and LOW data, like instant h'bam... you know?
   input: DIRECTIONspeed (e.g. N100 - north wheel move at 100% power)
   output: ToFNumber:Distance (e.g. 1:234 - ToF sensor 1 measures 234mm)
*/
//#include "Adafruit_VL53L0X.h" // Created by Adafruit - library for ToF
#include <Wire.h> // to communicate with i2c devices

// board 1 motor 1
const int in11 = 12;
const int in12 = 11;
// board 1 motor 2
const int in13 = 10;
const int in14 = 9;
// board 2 motor 3
const int in21 = 5;
const int in22 = 4;
// board 2 motor 4
const int in23 = 3;
const int in24 = 2;

// momentary switch stuff for ball detection
const int sw = 22;
int swOut = HIGH;
int swState;
int lastSwState = LOW;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50; // CHANGE TO FIT

//// dual ToF setup (i2c address and shut down pins - to set custom address)
//#define LOX1_ADDRESS 0x30
//#define LOX2_ADDRESS 0x31
//#define SHT_LOX1 14
//#define SHT_LOX2 15
//// ToF objects
//Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
//Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();
//
////Input and Output Data
//VL53L0X_RangingMeasurementData_t measure1; // ToF measurements
//VL53L0X_RangingMeasurementData_t measure2;
int flSpeed = 0; // specific motor speed (percentage)
int flrSpeed = 0;
int frSpeed = 0;
int frrSpeed = 0;
int blSpeed = 0;
int blrSpeed = 0;
int brSpeed = 0;
int brrSpeed = 0;
String inputString = ""; // holds serial comm from rPi
String outputString = ""; // sends ToF data to rPi
boolean stringComplete = false;
int motNum;

void serialInput() {
  //Select correct motor driver and motor for control, and wheel direction (i.e. CW or ACW)
  if (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == 'a')
    {
      motNum = 1;
      stringComplete = true;
    }
    else if (inChar == 'A')
    {
      motNum = 11;
      stringComplete = true;
    }
    else if (inChar == 'b')
    {
      motNum = 2;
      stringComplete = true;
    }
    else if (inChar == 'B')
    {
      motNum = 21;
      stringComplete = true;
    }
    else if (inChar == 'd')
    {
      motNum = 3;
      stringComplete = true;
    }
    else if (inChar == 'D')
    {
      motNum = 31;
      stringComplete = true;
    }
    else if (inChar == 'c')
    {
      motNum = 4;
      stringComplete = true;
    }
    else if (inChar == 'C')
    {
      motNum = 41;
      stringComplete = true;
    }
    else if (inChar == '\n') //remove if necessary
    {
      stringComplete = true;
    }
    else
    {
      inputString += inChar;
      //inputString.concat(inChar);
      Serial.print("other:");
      Serial.println(inputString);
    }
  }
}

void setID() {
  //  // all reset
  //  digitalWrite(SHT_LOX1, LOW);
  //  digitalWrite(SHT_LOX2, LOW);
  //  delay(10);
  //  // all unreset
  //  digitalWrite(SHT_LOX1, HIGH);
  //  digitalWrite(SHT_LOX2, HIGH);
  //  delay(10);
  //
  //  // activating LOX1 and reseting LOX2
  //  digitalWrite(SHT_LOX1, HIGH);
  //  digitalWrite(SHT_LOX2, LOW);
  //
  //  // initing LOX1
  //  if(!lox1.begin(LOX1_ADDRESS)) {
  //    Serial.println(F("Failed to boot first VL53L0X"));
  //    while(1);
  //  }
  //  delay(10);
  //
  //  // activating LOX2
  //  digitalWrite(SHT_LOX2, HIGH);
  //  delay(10);
  //
  //  //initing LOX2
  //  if(!lox2.begin(LOX2_ADDRESS)) {
  //    Serial.println(F("Failed to boot second VL53L0X"));
  //    while(1);
  //  }
}

void serialOutput() {
  // ToF Code
  //  lox1.rangingTest(&measure1, false); // change to 'true' to get debug data
  //  lox2.rangingTest(&measure2, false);
  //
  //  // print sensor readings
  //  Serial.print("1:");
  //  if(measure1.RangeStatus != 4) {     // if not out of range
  //    Serial.println(measure1.RangeMilliMeter);
  //  } else {
  //    Serial.println("out of range");
  //  }
  //  Serial.print("2:");
  //  if(measure2.RangeStatus != 4) {
  //    Serial.println(measure2.RangeMilliMeter);
  //  } else {
  //    Serial.println("out of range");
  //  }

  // debounced momentary switch code - UNTESTED
  int reading = digitalRead(sw);
  if (reading != lastSwState) {
    lastDebounceTime = millis();
  }

  if (millis() - lastDebounceTime > debounceDelay) {
    if (reading != swState) {
      swState = reading;
      if (swState == HIGH) {
        swOut = !swOut;
      }
    }
  }
  Serial.println(swState);
  lastSwState = reading;
}

void setup(){
  Serial.begin(115200);
  inputString.reserve(200);
  outputString.reserve(200);

  //  // wait for serial ready, shut down and reset for separate addresses
  //  while (! Serial) { delay(1); }
  //  pinMode(SHT_LOX1, OUTPUT);
  //  pinMode(SHT_LOX2, OUTPUT);
  //  digitalWrite(SHT_LOX1, LOW);
  //  digitalWrite(SHT_LOX2, LOW);
  //  setID();

  // motor driver outputs and momentary switch input
  pinMode(in11, OUTPUT);
  pinMode(in21, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(in22, OUTPUT);
  pinMode(in13, OUTPUT);
  pinMode(in23, OUTPUT);
  pinMode(in14, OUTPUT);
  pinMode(in24, OUTPUT);
  pinMode(sw, INPUT_PULLUP);

  stringComplete = false;
}

void loop()
{
  serialInput();
  if (stringComplete) {
    Serial.print("inputstring:");
    Serial.println(inputString);
    if (motNum == 1) {
      flSpeed = map(inputString.toInt(), 0, 100, 0, 255); //Converts 0-100 values to 0-255
      Serial.println(flSpeed);
      analogWrite(in11, flSpeed);
      analogWrite(in12, 0);
    }
    else if (motNum == 11) {
      flrSpeed = map(inputString.toInt(), 0, 100, 0, 255);
      analogWrite(in11, 0);
      analogWrite(in12, flrSpeed);
    }
    if (motNum == 2) {
      frSpeed = map(inputString.toInt(), 0, 100, 0, 255);
      analogWrite(in13, frSpeed);
      analogWrite(in14, 0);
    }
    else if (motNum == 21) {
      frrSpeed = map(inputString.toInt(), 0, 100, 0, 255);
      analogWrite(in13, 0);
      analogWrite(in14, frrSpeed);
    }
    if (motNum == 3) {
      blSpeed = map(inputString.toInt(), 0, 100, 0, 255);
      analogWrite(in21, blSpeed);
      analogWrite(in22, 0);
    }
    else if (motNum == 31) {
      blrSpeed = map(inputString.toInt(), 0, 100, 0, 255);
      analogWrite(in21, 0);
      analogWrite(in22, blrSpeed);
    }
    if (motNum == 4) {
      brSpeed = map(inputString.toInt(), 0, 100, 0, 255);
      analogWrite(in23, brSpeed);
      analogWrite(in24, 0);
    }
    else if (motNum == 41) {
      brrSpeed = map(inputString.toInt(), 0, 100, 0, 255);
      analogWrite(in23, 0);
      analogWrite(in24, brrSpeed);
    }

    inputString = "";
    //Add lines to clear xSpeed here if value retention not wanted
    stringComplete = false;
  }

  analogWrite(in11, flSpeed);
  analogWrite(in12, flrSpeed);
  analogWrite(in13, frSpeed);
  analogWrite(in14, frrSpeed);
  analogWrite(in21, blSpeed);
  analogWrite(in22, blrSpeed);
  analogWrite(in23, brSpeed);
  analogWrite(in24, brrSpeed);
  
  //serialOutput(); // momentary switch, no ToF
}
