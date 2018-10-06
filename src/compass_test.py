#from hmc5883l import hmc5883l as Compass
import motors
import time
import compass
#compass = Compass(declination=(11, 37))

try:
    compassInitial = compass.loop()
    # 90 deg:
    # turn counterclockwise till >90
    while True:
        motors.rotateCenter(direction=-1,power=50)
        #have_a_quick_snooze(0.05)
        angle = compass.loop()
        time.sleep(0.01)
        #signed angle
        difference = abs(angle-compassInitial)
        print("a:",angle,"b:",difference, "t:",time.perf_counter())
        if difference >= 90:
            motors.stop()
            compassInitial = angle
            time.sleep(1)
            print('new initial',compassInitial)
except Exception as e:
    print(e)
    motors.stop()