import compass
import time
import motors

try:
    compassInitial = compass.heading() 
    # 90 deg:
    # turn counterclockwise till >90
    while True:
        motors.rotateCenter(direction=-1,power=50)
        #have_a_quick_snooze(0.05)
        angle = compass.heading() 
        #signed angle
        difference = compass.difference(compassInitial, angle, -1)
        print("a:",compassInitial,"b:",angle,"d:",difference,"t:",time.perf_counter())
        if difference >= 90:
            motors.stop()
            compassInitial = compass.heading()
            time.sleep(1)
            print('new initial',compassInitial)
except Exception as e:
    print(e)
    motors.stop()