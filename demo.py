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

motor_params.forward(40)
motor_params.forward(-40)
motor_params.Left90deg()
motor_params.Right90deg()


