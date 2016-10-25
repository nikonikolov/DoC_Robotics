import argparse
import contextlib
import time
import sys
import math
import brickpi
import motor_params

#cmd_parser.add_argument('k_p', type=float, help='P gain')
interface = motor_params.interface#args = cmd_parser.parse_args()
motors = motor_params.motors


def TurnOpposite(angle):
    """Given angle for motor 0, rotate 0 and 1 in opposite directions.
    """
    interface.increaseMotorAngleReferences(motors, [angle, -angle])

    while not interface.motorAngleReferencesReached(motors):
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

#square()
#test_angle(float(sys.argv[1]))
forward(40)


