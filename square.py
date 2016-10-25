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


def square(side=None):
    if side==None:
        side = 40
    for i in range(4):
        motor_params.forward(side)
        motor_params.Left90deg()

def test_angle(angle):
    motor_params.forward(10)
    #rotate(angle)
    motor_params.TurnOpposite(angle)
    motor_params.forward(10)

def rot_angle(angle, dist=None):
    if dist==None:
        dist=10
    motor_params.forward(dist)
    motor_params.rotate(angle)
    motor_params.forward(dist)

def rot_angle_calibrate(angle, dist=None):
    if dist==None:
        dist=10
    motor_params.forward(dist)
    motor_params.TurnOpposite(angle)
    motor_params.forward(dist)


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
#motor_params.forward(40)
#motor_params.rotate(90)


#rot_angle(90)
#motor_params.motor_rotate(17)
#rot_angle_calibrate(-7)


