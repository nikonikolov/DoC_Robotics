import math
import time
import sys
import os

import numpy as np
import brickpi

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../pmotion')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../ultrasonic_sensors')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../MCL')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../place_rec')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../touch_sensors')

import motor_params

interface = motor_params.interface


def calibrate():
    kp_values = range(100, 1000, 50)

    for i, kp in enumerate(kp_values):
        print "kp =", kp
        interface.startLogging("plot/new_pid_logs/kp_%d.log" % int(kp))
        left_motor_params = interface.MotorAngleControllerParameters()
        left_motor_params.maxRotationAcceleration = 8.0
        left_motor_params.maxRotationSpeed = 12.0
        left_motor_params.feedForwardGain = 255/20.0
        left_motor_params.minPWM = 18.0
        left_motor_params.pidParameters.minOutput = -255
        left_motor_params.pidParameters.maxOutput = 255
        left_motor_params.pidParameters.k_p = kp
        left_motor_params.pidParameters.k_i = 0
        left_motor_params.pidParameters.K_d = 0
        interface.setMotorAngleControllerParameters(
              motor_params.MOTOR_LEFT, left_motor_params)

        right_motor_params = interface.MotorAngleControllerParameters()
        right_motor_params.maxRotationAcceleration = 8.0
        right_motor_params.maxRotationSpeed = 12.0
        right_motor_params.feedForwardGain = 255/20.0
        right_motor_params.minPWM = 18.0
        right_motor_params.pidParameters.minOutput = -255
        right_motor_params.pidParameters.maxOutput = 255
        right_motor_params.pidParameters.k_p = kp
        right_motor_params.pidParameters.k_i = 0
        right_motor_params.pidParameters.K_d = 0
        interface.setMotorAngleControllerParameters(
              motor_params.MOTOR_RIGHT, right_motor_params)

        # Choose your action here.
        motor_params.rotate(180.0)
        motor_params.rotate(-180.0)
        # End of choose action.

        interface.stopLogging()
    interface.terminate()


if __name__== "__main__":
    calibrate()
