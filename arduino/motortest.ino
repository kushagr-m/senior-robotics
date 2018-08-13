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
int nSpeed = 0;
int noSpeed = 0;
String inputString = ""; // holds serial comm from rPi
String outputString = ""; // sends ToF data to rPi
boolean stringComplete = false; 
int motNum = 1;


void serialInput()
  //Select correct motor driver and motor for control, and wheel direction (i.e. CW or ACW)
{
   while (Serial.available()) {
    char inChar = (char)Serial.read(); 
    
    if (inChar == 'A')
    {
      if (inChar == 'R')
      {
        motNum = 11;
        stringComplete = true;
      }
      else
      {
        motNum = 1;
        stringComplete = true;
      }
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

void setup() {
 Serial.begin(115200);
 inputString.reserve(200);
 outputString.reserve(200);
 Serial.println("set");
  pinMode(in11, OUTPUT);
  pinMode(in21, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(in22, OUTPUT);
  pinMode(in13, OUTPUT);
  pinMode(in23, OUTPUT);
  pinMode(in14, OUTPUT);
  pinMode(in24, OUTPUT);
}

void loop()
{
  serialInput();
  if (stringComplete) {
    if (motNum == 1) {
    nSpeed = map(inputString.toInt(),0,100,0,255); //Converts 0-100 values to 0-255
    noSpeed = 0;
    }
    else if (motNum == 11) {
    nSpeed = map(inputString.toInt(),0,100,0,255);
    noSpeed = 0;
    }
  }
    
    analogWrite(in11, nSpeed);
    analogWrite(in12, noSpeed);
    delay(500);
    
    inputString = "";
    //Add lines to clear xSpeed here if value retention not wanted
    stringComplete = false;
}
