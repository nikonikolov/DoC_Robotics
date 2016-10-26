import brickpi
import time
import argparse
import numpy as np

#cmd_parser = argparse.ArgumentParser(description = 'Tune controller')
#cmd_parser.add_argument('k_p', type=float, help='P gain')
#args = cmd_parser.parse_args()

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 12.0



# tune all the following parameters
T = 0.4
G = 800

# motorParams.feedForwardGain = 255/20.0
motorParams.feedForwardGain = 0.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 0.6*G
motorParams.pidParameters.k_i = 2*motorParams.pidParameters.k_p/T
motorParams.pidParameters.K_d = motorParams.pidParameters.k_p*T/8

k_i_zn = 2*motorParams.pidParameters.k_p/T
k_d_zn = motorParams.pidParameters.k_p*T/8

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

# Sequence of Ki and Kd values to try
Kd_vals = np.arange(1.0, 1.6, 0.1)
Ki_vals = np.arange(0.1, 0.6, 0.1)
angle = 6.0

for k_d in Kd_vals:
    for k_i in Ki_vals:
        motorParams.pidParameters.k_i = k_i_zn*k_i
	motorParams.pidParameters.K_d = k_d_zn*k_d
	angle = -angle
    	
	filename = "Ki_" + str(k_i) + "_Kd_" + str(k_d) + ".log"

	interface.startLogging(filename)
		
	interface.setMotorAngleControllerParameters(motors[0],motorParams)
	interface.setMotorAngleControllerParameters(motors[1],motorParams)

        interface.increaseMotorAngleReferences(motors,[angle,angle])

	while not interface.motorAngleReferencesReached(motors) :
	    motorAngles = interface.getMotorAngles(motors)
	    if motorAngles :
	        print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
	    time.sleep(0.5)

    	print "Destination reached!"

	interface.stopLogging()
interface.terminate()
