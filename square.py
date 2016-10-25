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
motorParams.pidParameters.k_i = 2*motorParams.pidParameters.k_p/T*0.3
motorParams.pidParameters.K_d = motorParams.pidParameters.k_p*T/8*1.5


interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)


# DO NOT EDIT ABOVE THIS LINE, THOSE ARE ALL THE TUNING STUFF


def TurnOpposite(angle):
    """Given angle for motor 0, rotate 0 and 1 in opposite directions.
    """
    interface.increaseMotorAngleReferences(motors, [angle, -angle])

    while not interface.motorAngleReferencesReached(motors):
	# motorAngles = interface.getMotorAngles(motors)
	# if motorAngles :
	#     print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
	time.sleep(0.1)

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
    return dist*0.296

# angle is in degrees
def rotate_to_motor_angle(angle):
    return (angle*0.038050073 + 0.0998)

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
        time.sleep(0.1)
    print "Destination reached!"


def square(side=None):
    forward(-5.0)
    Right90deg()
    Left90deg()
    return
    if side==None:
        side = 40
    for i in range(4):
        forward(side)
        Left90deg()

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



