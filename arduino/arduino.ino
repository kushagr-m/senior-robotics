/*
 * en is used for analog data from 0 to 255 (but is mapped, so 0-100 over serial comms)
 * in is used for digital - HIGH and LOW data, like instant h'bam... you know?
 */

// board 1 motor 1
int en1A = 13;
int in11 = 12;
int in12 = 11;
// board 1 motor 2
int en1B = 8;
int in13 = 10;
int in14 = 9;
// board 2 motor 3
int en2A = 6;
int in21 = 5;
int in22 = 4;
// board 2 motor 4
int en2B = 1;
int in23 = 3;
int in24 = 2;
//Input and Output Data
int nSpeed = 0
int eSpeed = 0
int sSpeed = 0
int wSpeed = 0
String inputString = "";
String outputString = "";
boolean stringComplete = false;
int motNum = 1;

void setup()
{
  Serial.begin(9600);
  inputString.reserve(200);
  outputString.reserve(200);
  
  pinMode(en1A, OUTPUT);
  pinMode(en2A, OUTPUT);
  pinMode(en1B, OUTPUT);
  pinMode(en2B, OUTPUT);
  pinMode(in11, OUTPUT);
  pinMode(in21, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(in22, OUTPUT);
  pinMode(in13, OUTPUT);
  pinMode(in23, OUTPUT);
  pinMode(in14, OUTPUT);
  pinMode(in24, OUTPUT);
}

void serialInput()
  //Select correct motor driver and motor for control
{
   while (Serial.available()) {
    char inChar = (char)Serial.read(); 
    
    if (inChar == 'N')
    {
      motNum = 1;
      stringComplete = true;
    }
    else if (inChar == 'E')
    {
      motNum = 2;
      stringComplete = true;
    }
    else if (inChar == 'S')
    {
      motNum = 3;
      stringComplete = true;
    }
    else if (inChar == 'W')
    {
      motNum = 4;
      stringComplete = true;
    }
    else if (inChar == '\n') //remove if necessary
    {
      stringComplete = true;
    }
    else
    {
      inputString += inChar;
    }
  } 
}


void serialOutput() {
  while (Serial.available()) {
    //Code for time of flight sensors go here
    //Format is RangeF:123, where 123 represents 123mm from the front sensor to an obstacle/wall in its front

    //TOF front
    String ranf = "";
    //TOF left
    String ranl = "";
    //TOF right
    String ranr = "";
    //TOF back
    String ranb = "";

    outputString = ranf + ranl + ranr + ranb;
  }
}

void loop()
{
  serialInput();
  if (stringComplete) {
    if (motNum == 1) {
    nSpeed = map(inputString.toInt(),0,100,0,255); //Converts 0-100 values to 0-255
    }
    else if (motNum == 2) {
    eSpeed = map(inputString.toInt(),0,100,0,255);
    }
    else if (motNum == 3) {
    sSpeed =map(inputString.toInt(),0,100,0,255);
    }
    else if (motNum == 4) {
    wSpeed = map(inputString.toInt(),0,100,0,255);
    }
    
    analogWrite(en1A, nSpeed);
    analogWrite(en1B, eSpeed);
    analogWrite(en2A, sSpeed);
    analogWrite(en2B, wSpeed);
    
    Serial.print(nSpeed); //For testing only! Delete to prevent unnecessary undefined serial comms to rPi
    Serial.print(eSpeed);
    Serial.print(sSpeed);
    Serial.println(wSpeed);
    inputString = "";
    //Add lines to clear xSpeed here if value retention not wanted
    stringComplete = false;
  
  serialOutput();
  Serial.println(outputString);
  }
}
