import numpy as np
import sys
import bisect
import random

sys.path.append('/home/pi/DoC_Robotics/pmotion')
sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import motion_predict
import walls
import ultrasound

# TO DO: calculate the standard deviation and the constant likelihood
SONAR_CONSTANT_LIKELIHOOD = 0.05 
SONAR_STD = 2
UNSENSIBLE_READINNGS_THRESHOLD = 50
NUMBER_OF_PARTICLES = motion_predict.NUMBER_OF_PARTICLES


class UnsensibleReadings(Exception):
    pass


def calculate_likelihood(x, y, theta, z):
    """
    param: z: sonar measurement
    """
    particle = motion_predict.Particle(x=x, y=y, theta=theta)
    m = walls.getWallDist(particle, walls.wallmap)          # calculate estimated measurment for this particle
    # if incidence angle or distance is out of range then skip the update
    if m == float("inf"):
        return -1
    return np.exp(-np.power(z - m, 2.) / (2 * np.power(SONAR_STD, 2.))) + SONAR_CONSTANT_LIKELIHOOD


def updateMeasurement(state, z):
    """
    param: z: sonar measurement
    """
    unsensible_readings = 0
    new_weights = []
    for p,w in zip(state.particles, state.weights):
        likelihood = calculate_likelihood(p.x, p.y, p.theta, z)
        if likelihood < 0:
            unsensible_readings+=1
            new_weights.append(SONAR_CONSTANT_LIKELIHOOD * w)     
        else:
            new_weights.append(likelihood * w)     
    if unsensible_readings > UNSENSIBLE_READINNGS_THRESHOLD:
        print "I am here"
        raise UnsensibleReadings
    return motion_predict.State(particles=state.particles, weights=new_weights)


def normalize(state):
    total_weight = sum(w for w in state.weights)
    return motion_predict.State(particles=state.particles, 
                                weights=[w/total_weight for w in state.weights])


def resample(state):
    first = True
    stack = []
    for i, w in enumerate(state.weights):
        if first:
            stack.append(w)
            first = False
        else:
            stack.append(stack[i-1]+w)

    new_state = motion_predict.State(particles=[], weights=[])
    for _ in range(NUMBER_OF_PARTICLES):
        i = bisect.bisect(stack, random.random())
        new_state.weights.append(1.0 / NUMBER_OF_PARTICLES)
        new_state.particles.append(state.particles[i])
    return new_state


def MCLStep(state):
    try:
        print "Begining:"
        print state.x, state.y, state.theta
        state = updateMeasurement(state, ultrasound.get_reading())
        print "updated measurement:"
        print state.x, state.y, state.theta
        state = normalize(state)
        print "normalized:"
        print state.x, state.y, state.theta
        return resample(state)
    except UnsensibleReadings:
        return state


def main():
    ultrasound.setup()
    
    WAYPOINTS =[
            walls.Point(84, 30),
            walls.Point(180, 30),
            walls.Point(180, 54),
            walls.Point(138, 54),
            walls.Point(138, 168),
            walls.Point(114, 168),
            walls.Point(114, 84),
            walls.Point(84, 84),
            walls.Point(84, 30)]

    state = motion_predict.State(
            particles=[motion_predict.Particle(
                    x=WAYPOINTS[0].x, y=WAYPOINTS[0].y, theta=0)] * NUMBER_OF_PARTICLES,
            weights=[1.0 / NUMBER_OF_PARTICLES
                     for _ in range(NUMBER_OF_PARTICLES)])
    
    for waypoint in WAYPOINTS[1:]:
        # waypoint refers to the next destination
        while True:
            x_is_close = abs(state.x - waypoint.x) <= 1.0
            y_is_close = abs(state.y - waypoint.y) <= 1.0

            if x_is_close and y_is_close:
                # We have reached our destination, rotate!
                break
            else:
                state = motion_predict.navigateToWaypoint(state, waypoint)
                state = MCLStep(state)
                print "Final:"
                print state.x, state.y, state.theta
                # state.draw_particles()


if __name__ == "__main__":
    main()
