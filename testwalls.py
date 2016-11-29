import sys
import os
import getpass

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/pmotion')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/ultrasonic_sensors')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/MCL')

import math
import walls

import motion_predict

p = motion_predict.Particle(x=124, y=120, theta=math.radians(30))
print walls.getWallDist(p, incidence_angle=False)
