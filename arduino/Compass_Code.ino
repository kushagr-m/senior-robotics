// Ensure compass is fixed to a stable surface and is not tilted in any direction! 
#include <Wire.h>

#define OLED_ADDR 0x3C
#define compass_address 0x1E
#define compass_XY_excitation 1160
#define compass_Z_excitation 1080
#define compass_rad2deg 57.296

#define compass_cal_x_offset 116
#define compass_cal_y_offset  225
#define compass_cal_x_gain 1.1
#define compass_cal_y_gain 1.12

float compass_x_offset = 0;
float compass_y_offset = 0;
float compass_z_offset = 0;
float compass_gain_factor = 1;
float compass_x_scaled;
float compass_y_scaled;
float compass_z_scaled;
float compass_x_gain_error = 1;
float compass_y_gain_error = 1;
float compass_z_gain_error = 1;
float bearing = 0;
int compass_x = 0;
int compass_y = 0;
int compass_z = 0;

// reads data from compass and updates the global x,y,z co-ordinate variables
void compass_read() {
  Wire.beginTransmission(compass_address);
  Wire.write(0x02);
  Wire.write(0b10000001); //00 for continuous mode, 01 for single
  Wire.endTransmission();
  Wire.requestFrom(compass_address, 6);

  if (6 <= Wire.available()) {
    compass_x = Wire.read() << 8 | Wire.read();
    compass_y = Wire.read() << 8 | Wire.read();
    compass_z = Wire.read() << 8 | Wire.read();
  }
}

// calculates magnetometer offset using +ve/-ve bias, updates x,y,z offset global variables
void compass_offset_calibration() {
  /* Calculates difference in gain in each axis using sensor's built-in self field excitation function
     Calculates the mean of each axes' magnetic field strength when it is rotated in a full revolution
  */
  //GAIN OFFSET ESTIMATION
  //Configure control register for +ve bias
  Wire.beginTransmission(compass_address);
  Wire.write(0x00);
  Wire.write(0b01110001);
  /* format: 0 A A DO2 DO1 DO0 MS1 MS2
    A A                        DO2 DO1 DO0      Sample Rate [Hz]      MS1 MS0    Measurment Mode
    0 0 = No Average            0   0   0   =   0.75                   0   0   = Normal
    0 1 = 2 Sample average      0   0   1   =   1.5                    0   1   = Positive Bias
    1 0 = 4 Sample Average      0   1   0   =   3                      1   0   = Negative Bais
    1 1 = 8 Sample Average      0   1   1   =   7.5                    1   1   = -
    1   0   0   =   15 (Default)
    1   0   1   =   30
    1   1   0   =   75
    1   1   1   =   -
  */
  Wire.endTransmission();
  compass_read(); //first data set is junk, not used

  //Read positively biased data
  while (compass_x < 200 | compass_y < 200 | compass_z < 200) {
    compass_read();
  }

  compass_x_scaled = compass_x * compass_gain_factor;
  compass_y_scaled = compass_y * compass_gain_factor;
  compass_z_scaled = compass_z * compass_gain_factor;

  // Offset = 1160 - '+ve data'
  compass_x_gain_error = (float)compass_XY_excitation / compass_x_scaled;
  compass_y_gain_error = (float)compass_XY_excitation / compass_y_scaled;
  compass_z_gain_error = (float)compass_Z_excitation / compass_z_scaled;


  // Configure control register for -ve bias mode
  Wire.beginTransmission(compass_address);
  Wire.write(0x00);
  Wire.write(0b01110010); //refer to table of bit configurations above
  Wire.endTransmission();
  compass_read(); //junk again

  //Read negatively biased data
  while (compass_x > -200 | compass_y > -200 | compass_z > -200) {
    compass_read();
  }

  compass_x_scaled = compass_x * compass_gain_factor;
  compass_y_scaled = compass_y * compass_gain_factor;
  compass_z_scaled = compass_z * compass_gain_factor;


  // Take average of the offsets
  compass_x_gain_error = (float)((compass_XY_excitation / abs(compass_x_scaled)) + compass_x_gain_error) / 2;
  compass_y_gain_error = (float)((compass_XY_excitation / abs(compass_y_scaled)) + compass_y_gain_error) / 2;
  compass_z_gain_error = (float)((compass_Z_excitation / abs(compass_z_scaled)) + compass_z_gain_error) / 2;

  //OFFSET ESTIMATION
  // Configure control register for normal mode
  Wire.beginTransmission(compass_address);
  Wire.write(0x00);
  Wire.write(0b01111000); //just look up twice kek
  Wire.endTransmission();

  //calibration of magnetometer
  for (byte i = 0; i < 10; i++) {
    compass_read(); //first few data sets are junk again
  }
  float x_max = -4000;
  float y_max = -4000;
  float z_max = -4000;
  float x_min = 4000;
  float y_min = 4000;
  float z_min = 4000;
  unsigned long t = millis();

  while (millis() - t <= 5000) { //not actually 30s in reality, check!
    compass_read();
    compass_x_scaled = (float)compass_x * compass_gain_factor * compass_x_gain_error;
    compass_y_scaled = (float)compass_y * compass_gain_factor * compass_y_gain_error;
    compass_z_scaled = (float)compass_z * compass_gain_factor * compass_z_gain_error;

    x_max = max(x_max, compass_x_scaled);
    y_max = max(y_max, compass_y_scaled);
    z_max = max(z_max, compass_z_scaled);


    x_min = min(x_min, compass_x_scaled);
    y_min = min(y_min, compass_y_scaled);
    z_min = min(z_min, compass_z_scaled);
  }

  compass_x_offset = ((x_max - x_min) / 2) - x_max;
  compass_y_offset = ((y_max - y_min) / 2) - y_max;
  compass_z_offset = ((z_max - z_min) / 2) - z_max;
}

// set magnetometer gain and update the gain_factor variable - DO NOT SIMPLIFY, CHANGE IF NEEDED
void compass_init(int gain){
  byte gain_reg,mode_reg;
  Wire.beginTransmission(compass_address);
  Wire.write(0x01);

  //refer below if statement for bit configuration for gain_reg
  if (gain == 0){
    gain_reg = 0b00000000;
    compass_gain_factor = 0.73;
  }
  else if (gain == 1){
    gain_reg = 0b00100000;
    compass_gain_factor= 0.92;
  }
  else if (gain == 2){
    gain_reg = 0b01000000;
    compass_gain_factor= 1.22;
  }
  else if (gain == 3){
    gain_reg = 0b01100000;
    compass_gain_factor= 1.52;
  }
  else if (gain == 4){
    gain_reg = 0b10000000;
    compass_gain_factor= 2.27;
  }
  else if (gain == 5){
    gain_reg = 0b10100000;
    compass_gain_factor= 2.56;
  }
  else if (gain == 6){
    gain_reg = 0b11000000;
    compass_gain_factor= 3.03;
  }
  else if (gain == 7){
    gain_reg = 0b11100000;
    compass_gain_factor= 4.35;
  }
  
  Wire.write(gain_reg);
  /* bit configuration = g2 g1 g0 0 0 0 0 0
  g2 g1 g0 = 0 0 1 for 1.3 guass
  g2 g1 g0 = 0 1 0 for 1.9 Guass
  */
  Wire.write(0b00000011);  // Put the magnetometer in idle (00 is cont., 01 for single, 11 for idle)
  Wire.endTransmission();
}

//transformed (scaled) co-ordinate values
void compass_scaled_reading(){
  compass_read();
  compass_x_scaled=compass_x*compass_gain_factor*compass_x_gain_error+compass_x_offset;
  compass_y_scaled=compass_y*compass_gain_factor*compass_y_gain_error+compass_y_offset;
  compass_z_scaled=compass_z*compass_gain_factor*compass_z_gain_error+compass_z_offset;
}

//calibrated angle to magnetic North for Melbourne (magnetic declination)
void compass_heading(){
  float declination_angle = 0.202749081; //i.e. 11 degrees 37 arcminutes
  compass_scaled_reading();
  if (compass_y_scaled>0){
    bearing = (90-atan(compass_x_scaled/compass_y_scaled)*compass_rad2deg) + declination_angle;
  }else if (compass_y_scaled<0){
    bearing = (270-atan(compass_x_scaled/compass_y_scaled)*compass_rad2deg) + declination_angle;
  }else if (compass_y_scaled==0 & compass_x_scaled<0){
    bearing = 180 + declination_angle;
  }else{
    bearing = declination_angle;
  }
}

void setup() {
  Serial.begin(9600);

  Wire.begin();
  compass_init(2); //Gain factor 1.22
  compass_offset_calibration();
}

void loop() {
  compass_scaled_reading();
  compass_heading();

  //Uncomment below for data for use with MagViewer
  Serial.print(compass_x_scaled);
  Serial.print(", ");
  Serial.print(compass_y_scaled);
  Serial.print(", ");
  Serial.println(compass_z_scaled);
  
  //Uncomment below for pure serial data to be sent
  /*
  Serial.print(compass_x_scaled);
  Serial.print("\n");
  Serial.print(compass_y_scaled);
  Serial.print("\n");
  Serial.print(compass_z_scaled);
  Serial.print("\n");
  Serial.print(bearing);
  Serial.print("\n");
  */
}
