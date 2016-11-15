import numpy as np
import sys
import bisect

sys.path.append('/home/pi/DoC_Robotics/pmotion')

import motion_predict
import walls

# TO DO: calculate the standard deviation and the constant likelihood
SONAR_CONSTANT_LIKELIHOOD =  
SONAR_STD = 

NUMBER_OF_PARTICLES = motion_predict.NUMBER_OF_PARTICLES
WAYPOINTS = []


def calculate_likelihood(x, y, theta, z):
    """
    param: z: sonar measurement
    """
    
    def sonarLikelihood(x, mu):
        """ 
        param: x:   variable (z = actual measurement)
        param: mu:  mean (estimated measurement)
        """

    particle = motion_predict.Particle(x=x, y=y, theta=theta)
    m = walls.getWallDist(particle, walls.wallmap)          # calculate estimated measurment for this particle
    # if incidence angle or distance is out of range then skip the update
    if m == float("inf"):
        return -1
    return np.exp(-np.power(z - mu, 2.) / (2 * np.power(SONAR_STD, 2.))) + SONAR_CONSTANT_LIKELIHOOD


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
    return motion_predict.State(particles=state.particles, weights=new_weights)


def normalize(state):
    total_weight = sum(w for w in state.weights)
    return motion_predict.State(particles=state.particles, 
                                weights=[w/total_weight for w in state.weights])


def resample(state):
    first = True
    for w, i in enumerate(state.weights):
        if first:
            stack.append(w)
            first = False
        else:
            stack.append(stack[i-1]+w)

    new_state = motion_predict.State(particles=[], weights=[])
    for _ in range(NUMBER_OF_PARTICLES):
        i = bisect.bisect(stack, random.random())
        new_state.weights.append(state.weights[i])
        new_state.particles.append(state.particles[i])
    return new_state


def MCLStep(state):
    return resample(normalize(updateMeasurement(state)))


def navigateToWaypoint(state, dest):
    goal_theta = math.atan2(dest.y - state.y, dest.x - state.x)
    delta_theta_rad = goal_theta - state.theta
    if delta_theta_rad > math.pi:
        delta_theta_rad -= 2*math.pi
    elif delta_theta_rad < -math.pi:
        delta_theta_rad += 2*math.pi  
    motor_params.rotate(delta_theta_rad / math.pi * 180.0)
    state = state.rotate(delta_theta_rad)
    dist = min(20, math.sqrt(
            (state.y - dest.y)**2 + (state.x - dest.x)**2))
    motor_params.forward(dist)
    return MCLStep(state.move_forward(dist))


def main();
    state = motion_predict.State(
            particles=[motion_predict.Particle(x=84, y=30, theta=0)] * NUMBER_OF_PARTICLES,
            weights=[1.0 / NUMBER_OF_PARTICLES
                     for _ in range(NUMBER_OF_PARTICLES)])
    for waypoint in WAYPOINTS[1:]:
        # waypoint refers to the next destination
        while True:
            x_is_close = np.isclose(state.x, waypoint.x, atol=0.5)
            y_is_close = np.isclose(state.y, waypoint.y, atol=0.5)

            if x_is_close and y_is_close:
                # We have reached our destination, rotate!
                break
            else:
                state = navigate_to_waypoint(state, waypoint)


if __name__ == "__main__":
    main()
