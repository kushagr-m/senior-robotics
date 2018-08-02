/*
 * en is used for analog data from 0 to 255
 * in is used for digital - HIGH and LOW data
 * The rest is self explanatory, deal with it
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
String inputString = "";
String outputString = "";
boolean stringComplete = false;
int mNspeed = 0;
int mEspeed = 0;
int mSspeed = 0;
int mWspeed = 0;
int motNum = 0;

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
  
  Serial.println("I am ready for command and conquer, boss!");
}

void serialInput()
{
   while (Serial.available()) {
   // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    
    if (inChar == 'N')
    {
      motNum = 1;
    }
    else if (inChar == 'E')
    {
      motNum = 2;
    }
    else if (inChar == 'S')
    {
      motNum = 3;
    }
    else if (inChar == 'W')
    {
      motNum = 4;
    }
    else if (inChar == '\n')
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
    mNspeed = inputString.toInt();
    }
    else if (motNum == 2) {
    mEspeed = inputString.toInt();
    }
    else if (motNum == 3) {
    mSspeed = inputString.toInt();
    }
    else if (motNum == 4) {
    mWspeed = inputString.toInt();
    }
    
    //CODE TO MOVE THE MOTOR GOES HERE

    
    Serial.println(inputString);
    Serial.println(inputString.toInt());    
    //clear the string:
    inputString = "";
    stringComplete = false;
  
  serialOutput();
  Serial.println(outputString);
  }
}
