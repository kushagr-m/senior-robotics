/*

hitechnic IR for arduino
https://blog.blechschmidt.saarland/hitechnic-infrared-seeker-library-for-arduino/
http://www.newjerseyftc.com/uploads/3/1/3/6/3136053/using_the_ir_seeker.pdf

*/

// defining low-level functionso

int getCompassValue() {
  // gets compass value [0,360]
}

int ballZone() {
  // gets the zone of the ball (12 30* intervals)
  // R: [-6,6]
  // 0 = NORTH
  // -6 = 6 = SOUTH
}

int ballStrength() {
  // gets the strength of the ball
  // R: [0,255]
}

void botMove(degrees) {
  // use holonomic drive with 3 wheels to move at a bearing of x degrees
}

// end low-level functions

// defining higher level functions

int ballTowards() {
  // gradient of distance between ball and bot.
  // R: {-1,0,1}
  // -1 = getting closer
  // 0 = constant strength
  // +1 = getting further
}

int ballMovementDir() {
  // calculate ball's direction of motion
}

// end higher level functions

int compassInitial;
int previousBallZone;

void setup() {

  compassInitial = getCompassValue(); // stores the initial compass value, this is the value we will lock to
  previousBallZone = ballZone();

}

void loop() {

  if (getCompassValue() != compassInitial) { // if we are not facing forward
    // turn to face forward
  }

  // save a few previous ball zone values, to estimate ball direction (in array?)
  // save a few previous strength values to estimate ball direction (in array?)


  /*

  if [ball is in front] {go directly ahead}
  if [ball is in front and L/R] {go L/R till ball directly in front of us}
  if [ball is behind us] {go L/R till cond 4 is met.}
  if [ball is behind and L/R] {go back till ball is ahead, then use cond 2.}

  }

  */

}
