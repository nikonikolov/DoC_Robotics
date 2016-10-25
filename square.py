import argparse
import contextlib
import time
import sys
import math
import brickpi

#cmd_parser = argparse.ArgumentParser(description = 'Tune controller')
#cmd_parser.add_argument('k_p', type=float, help='P gain')
#args = cmd_parser.parse_args()

interface = brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParamsLeft = interface.MotorAngleControllerParameters()
motorParamsLeft.maxRotationAcceleration = 8.0
motorParamsLeft.maxRotationSpeed = 12.0
motorParamsRight = interface.MotorAngleControllerParameters()
motorParamsRight.maxRotationAcceleration = 8.0
motorParamsRight.maxRotationSpeed = 12.0
# tune all the following parameters

T = 0.4
G = 800

motorParamsLeft.feedForwardGain = 255/20.0
motorParamsLeft.minPWM = 18.0
motorParamsLeft.pidParameters.minOutput = -255
motorParamsLeft.pidParameters.maxOutput = 255
motorParamsLeft.pidParameters.k_p = 0.6*G
motorParamsLeft.pidParameters.k_i = 2*motorParamsLeft.pidParameters.k_p/T*0.3
motorParamsLeft.pidParameters.K_d = motorParamsLeft.pidParameters.k_p*T/8

motorParamsRight.feedForwardGain = 255/20.0
motorParamsRight.minPWM = 18.0
motorParamsRight.pidParameters.minOutput = -255
motorParamsRight.pidParameters.maxOutput = 255
motorParamsRight.pidParameters.k_p = 0.58*G
motorParamsRight.pidParameters.k_i = 2*motorParamsRight.pidParameters.k_p/T*0.3
motorParamsRight.pidParameters.K_d = motorParamsRight.pidParameters.k_p*T/8

interface.setMotorAngleControllerParameters(motors[0], motorParamsLeft)
interface.setMotorAngleControllerParameters(motors[1], motorParamsRight)


# DO NOT EDIT ABOVE THIS LINE, THOSE ARE ALL THE TUNING STUFF


def TurnOpposite(angle):
    """Given angle for motor 0, rotate 0 and 1 in opposite directions.
    """
    interface.increaseMotorAngleReferences(motors, [angle, -angle])

    while not interface.motorAngleReferencesReached(motors):
	# motorAngles = interface.getMotorAngles(motors)
	# if motorAngles :
	#     print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
	time.sleep(0.03)
    interface.setMotorPwm(motors[0], 0)
    interface.setMotorPwm(motors[1], 0)
    print "Destination reached!"


def Left90deg():
    rotate(-90)
    #TurnOpposite(dist_to_motor_angle(-10.691415022205297))
    # TurnOpposite(-3.1)


def Right90deg():
    rotate(90)
    #TurnOpposite(dist_to_motor_angle(10.711415022205297))


# dist is in cm
def dist_to_motor_angle(dist):
    return (dist*0.2959687 + 0.1) 
    #return (dist*0.2959687 - 0.03339163) 

# angle is in degrees
def rotate_to_motor_angle(angle):
    #return (angle*0.038050073 + 0.0998)
    # return (angle*0.038050073 + 0.08)
    return (angle*0.038050073 + 0.068)

# angle is in degrees - positive angle turns right
def rotate(angle):
    #wheels_dist = 13.6 
    #perimeter = 2*math.pi*(wheels_dist/2) 
    #travel_dist = angle/360*perimeter
    #motor_angle = dist_to_motor_angle(travel_dist)
    motor_angle = rotate_to_motor_angle(angle)
    TurnOpposite(motor_angle)

def forward(dist):
    angle = dist_to_motor_angle(dist)

    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
        time.sleep(0.03)
    interface.setMotorPwm(motors[0], 0)
    interface.setMotorPwm(motors[1], 0)
    print "Destination reached!"


def square(side=None):
    if side==None:
        side = 40
    for i in range(4):
        forward(side)
        Right90deg()

def test_angle(angle):
    forward(10)
    #rotate(angle)
    TurnOpposite(angle)
    forward(10)


@contextlib.contextmanager
def OpenInterface(filename):
    interface.startLogging()
    yield
    interface.terminate()
    interface.stopLogging()

"""
def main():
    with OpenInterface("rotate.log"):
        while True:
            TurnOpposite(-12.45)


if __name__ == "__main__":
    main()
"""

square()
#test_angle(float(sys.argv[1]))



