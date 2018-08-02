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
int m1Speed = 0;
int m2Speed = 0;
int m3Speed = 0;
int m4Speed = 0;
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
  //PETE'S BITS
   while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    if (inChar == 'a')
    {
      motNum = 1;
    }
    else if (inChar == 'b')
    {
      motNum = 2;
    }
    else if (inChar == 'c')
    {
      motNum = 3;
    }
    else if (inChar == 'd')
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
  //Input Stuff
  /*
   * Kush, what is the notation for the motors?
   * What is the format of the data to be received?
   */
  //PETE'S BITS
  serialInput();
  if (stringComplete) {
    if (motNum == 1) {
    m1Speed = inputString.toInt();
    }
    else if (motNum == 2) {
    m2Speed = inputString.toInt();
    }
    else if (motNum == 3) {
    m3Speed = inputString.toInt();
    }
    else if (motNum == 4) {
    m4Speed = inputString.toInt();
    }
    bot.manualMotorsPWM(m1Speed, m2Speed, m3Speed, m4Speed);
    Serial.println(inputString);
    Serial.println(inputString.toInt());
     //clear the string:
    inputString = "";
    stringComplete = false;
  

  serialOutput();
  Serial.println(outputString);
}
