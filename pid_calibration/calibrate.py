import math
import time
import numpy as np
import brickpi

import motor_params

interface = motor_params.interface


def calibrate():
    G = 1000
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
        motor_params.Left90deg()
        motor_params.Right90deg()
        # End of choose action.

        interface.stopLogging()
    interface.terminate()


if __name__== "__main__":
    calibrate()
