import sys
import bisect
import random

sys.path.append('/home/pi/DoC_Robotics/MCL')
sys.path.append('/home/pi/DoC_Robotics/pmotion')
sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import motor_params
import motion_predict
import ultrasound
import walls


def main():
    ultrasound.rotate_sensor()


if __name__ == "__main__":
    main()
