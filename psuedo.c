int compassValue() {
    // get compass value
}

int ballZone() {
    // return a value of [-6,6]
} 
// if this has changed, then the ball is moving relative to us

int ballStrength() {
    // returns a positive value
}

int ballTowards() {
    // returns {0,1,2}
    // 0 = moving towards us
    // 1 = not moving relative to us
    // 2 = moving away from us
}

// we can move in 60* intervals


void setup() {
    int compassInitial = compassValue(); // value that we will lock to
    int iterations = 0;
}

void loop() {    

    if (compassValue() != compassInitial) {
        // MAKE IT THE SAME
    }

    // IF THE BALL IS MOVING SOUTH

    iterations += 1;

}