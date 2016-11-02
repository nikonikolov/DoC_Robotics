import math
import random
import sys
import time


sys.path.append('/home/pi/DoC_Robotics/')

import motor_params


STANDARD_DEVIATION = 1.0
DISTANCE_TO_PIXEL = 10.0
particles = [(0, 0, 0) for _ in range(100)]  # type: Tuple[int, int, int]

def draw_particles():
    print "drawParticles:" + str([(200 + x * DISTANCE_TO_PIXEL,
                                   200 + y * DISTANCE_TO_PIXEL,
                                   t)
                                  for x, y, t in particles])


def update_particles_straight(d):
    for i in range(len(particles)):
        x, y, theta = particles[i]
        e = random.gauss(0, 0.07)
        f = random.gauss(0, 0.25 * math.pi / 180.0)
        particles[i] = (x + (d + e) * math.cos(theta),
                        y + (d + e) * math.sin(theta),
                        theta + f)


def update_particles_rotation(alpha):
    for i in range(len(particles)):
        g = random.gauss(0, 2.0) * math.pi / 180.0
        x, y, theta = particles[i]
        particles[i] = (x, y, theta + alpha + g)



for __ in range(4):
    draw_particles()
    for _ in range(4):
        motor_params.forward(10)
        update_particles_straight(10)
        draw_particles()

    motor_params.Left90deg()
    update_particles_rotation(math.pi / 2)
    draw_particles()
