import numpy as np
import sys
import bisect

sys.path.append('/home/pi/DoC_Robotics/pmotion')
sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import motion_predict
import walls
import ultrasound

# TO DO: calculate the standard deviation and the constant likelihood
SONAR_CONSTANT_LIKELIHOOD =  
SONAR_STD =
UNSENSIBLE_READINNGS_THRESHOLD = 

NUMBER_OF_PARTICLES = motion_predict.NUMBER_OF_PARTICLES

class UnsensibleReadings(Expcetion):
    pass

def calculateLikelihood(x, y, theta, z):
    """
    param: z: sonar measurement
    """
    
    def sonarLikelihood(x, mu):
        """ 
        param: x:   variable (z = actual measurement)
        param: mu:  mean (estimated measurement)
        """
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(SONAR_STD, 2.))) + SONAR_CONSTANT_LIKELIHOOD

    m = walls.getWallDist(particle, walls.wallmap)          # calculate estimated measurment for this particle
    # if incidence angle or distance is out of range then skip the update
    if m == 0:
        return -1
    return sonarLikelihood(z, m)

def updateMeasurement(state, z):
    """
    param: z: sonar measurement
    """
    unsensible_readings = 0
    new_weights = []
    for p,w in zip(state.particles, state.weights):
        likelihood = calculateLikelihood(p.x, p.y, p.theta, z)
        if likelihood < 0:
            unsensible_readings+=1
            new_weights.append(SONAR_CONSTANT_LIKELIHOOD * w)     
        else:
            new_weights.append(likelihood * w)     
    if unsensible_readings > UNSENSIBLE_READINNGS_THRESHOLD:
        raise UnsensibleReadings
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
    try:
        return resample(normalize(updateMeasurement(state, ultrasound.get_reading())))
    except UnsensibleReadings:
        return state



def main();
    ultrasound.setup()
    state = motion_predict.State(particles=[motion_predict.Particle(x=0, y=0, theta=0)] * NUMBER_OF_PARTICLES,
                  weights=[1.0 / NUMBER_OF_PARTICLES
                           for _ in range(NUMBER_OF_PARTICLES)])

    WAPOINTS =[
            (84, 30),
            (180, 30),
            (180, 54),
            (138, 54),
            (138, 168),
            (114, 168),
            (114, 84),
            (84, 84),
            (84, 30)]


    for waypoint in WAYPOINTS:
        state = motion_predict.navigateToWaypoint(state, dest)
        state = MCLStep(state)        
        print (state.x, state.y, state.theta)


if __name__ == "__main__":
    main()
