import bisect
import math
import random
import sys

sys.path.append('/home/pi/DoC_Robotics/MCL')
sys.path.append('/home/pi/DoC_Robotics/pmotion')
sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import motor_params
import motion_predict
import ultrasound
import walls


def main():
    while True:
        ultrasound.rotate_sensor(-math.pi)
        ultrasound.rotate_sensor(math.pi)


if __name__ == "__main__":
    main()
