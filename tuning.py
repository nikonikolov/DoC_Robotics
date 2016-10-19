import brickpi
import time
import argparse

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

motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 0.6*G
motorParams.pidParameters.k_i = 2*motorParams.pidParameters.k_p/T*0.5
motorParams.pidParameters.k_d = motorParams.pidParameters.k_p*T/8

interface.startLogging("a.log")
interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

while True:
    angle = float(input("Enter a angle to rotate (in radians): "))

    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
	motorAngles = interface.getMotorAngles(motors)
	if motorAngles :
	    print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
	time.sleep(0.1)

    print "Destination reached!"


interface.stopLogging()
interface.terminate()
