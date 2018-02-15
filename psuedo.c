int compassValue() {
    // get compass value
}

int ballZone() {
    /*
    return a value of [-6,6]
    0 = straight ahead
    -6 = 6 = behind
    */
} 

int ballStrength() {
    // returns a positive value
}

int ballTowards() {
    /*
    uses ballStrength as an input
    returns {0,1,2}
    0 = moving towards us
    1 = not moving relative to us
    2 = moving away from us
    */
}

/*

we can figure out the general direction of the ball using ballZone and ballTowards

if [ball is in front] {go directly ahead}
if [ball is in front and L/R] {go L/R till ball directly in front of us}
if [ball is behind us] {go L/R till cond 4 is met.}
if [ball is behind and L/R] {go back till ball is ahead, then use cond 2.}

}

*/

if (ballZone() > 0) && () {

}

/*
*/

// we can move in 60* intervals

void setup() {
    int compassInitial = compassValue(); // value that we will lock to
    int iterations = 0;
}

void loop() {    

    if (compassValue() != compassInitial) {
        // MAKE IT THE SAME 
        // LOCK BOT ORIENTATION TO NORTH
    }

    // IF THE BALL IS MOVING SOUTH

    iterations += 1;

}