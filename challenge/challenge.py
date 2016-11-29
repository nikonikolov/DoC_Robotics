import time
import os
import math
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../pmotion')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../ultrasonic_sensors')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../MCL')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../place_rec')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../touch_sensors')

import touch_sensors
import motion_predict
import walls
import mcl
import place_rec
import motor_params

# TO DO: CALIBRATE THESE VALUES AND THE SONAR LIKELIHOOD VALUES IN mcl
WAYPOINT_MIN_OFFSET = 5.0
FINAL_WAYPOINT_MIN_OFFSET = 3.0

NUMBER_OF_PARTICLES = motion_predict.NUMBER_OF_PARTICLES

def get_bottle(sig_point):
    """
    Arguements:
        sig_point - the signature point for which you need to take measurement and to compare to
    Returns:
        place_rec.BottleLocation() or None 
    """

    ls_normal = place_rec.LocationSignature()
    ls_normal.read(sig_point, place_rec.NORMAL_DIR)
    
    ls_bottle = place_rec.rot_sensor.takeSignature(sig_point.rstart, sig_point.rend, sig_point)
    ls_bottle.save(sig_point, place_rec.BOTTLE_DIR)

    return place_rec.get_bottle_belief(ls_bottle, ls_normal, sig_point)

def uncertainRotate(state, dest):
    """
    Arguments: 
        state - of type State
        dest - absolute endpoint
    """
    goal_theta = math.atan2(dest.y - state.y, dest.x - state.x)
    delta_theta_rad = goal_theta - state.theta
    if delta_theta_rad > math.pi:
        delta_theta_rad -= 2*math.pi
    elif delta_theta_rad < -math.pi:
        delta_theta_rad += 2*math.pi  
    motor_params.rotate(delta_theta_rad / math.pi * 180.0)
    return state.rotate(delta_theta_rad)


def uncertainNavigate(state, dest):
    """
    Arguments: 
        state - of type State
        dest - absolute orientation
    """
    goal_theta = math.atan2(dest.y - state.y, dest.x - state.x)
    dist = math.sqrt((dest.y - state.y) ** 2 + (dest.x - state.x) ** 2)
    delta_theta_rad = goal_theta - state.theta
    if delta_theta_rad > math.pi:
        delta_theta_rad -= 2*math.pi
    elif delta_theta_rad < -math.pi:
        delta_theta_rad += 2*math.pi  
    motor_params.rotate(delta_theta_rad / math.pi * 180.0)
    state = state.rotate(delta_theta_rad)
    motor_params.forward(dist)
    return state.move_forward(dist)

def sigPointMCLStep(state, mcl_points):
    """
    mcl_points - an array of points with the same x and y, but different theta that corresponds to angles that we should face to run MCL "safely" - assuming there is no bottle there;
        Note that robot should already be at x, y
    """

    for point in mcl_orientaitons:
        uncertainRotate(state, point)
        state = mcl.MCLStep(state)

    return state



class BumpException(Exception):
    """Exception when the touch sensor bumps into something."""
    def __init__(self, sensor):
        super(BumpException, self).__init__()
        self._sensor = sensor

    @property
    def sensor(self):
        return self._sensor


def move_while_listen_bump(dist):
    angle = motor_params.better_dist_to_motor_angle(dist)
    motor_params.interface.increaseMotorAngleReferences(
            motor_params.motors, [angle,angle])
    while True:
        left = motor_params.interface.getSensorValue(
                touch_sensors.TOUCH_PORT_LEFT)[0]
        right = motor_params.interface.getSensorValue(
                touch_sensors.TOUCH_PORT_RIGHT)[0]
        if left:
            motor_params.interface.setMotorPwm(
                    motor_params.motors[0], 0)
            motor_params.interface.setMotorPwm(
                    motor_params.motors[1], 0)
            raise BumpException(touch_sensors.TOUCH_PORT_LEFT)
        elif right:
            motor_params.interface.setMotorPwm(
                    motor_params.motors[0], 0)
            motor_params.interface.setMotorPwm(
                    motor_params.motors[1], 0)
            raise BumpException(touch_sensors.TOUCH_PORT_RIGHT)
        elif motor_params.interface.motorAngleReferencesReached(
                motor_params.motors):
            break
        else:
            time.sleep(0.03)

BOTTLES = {
    "A": [
        place_rec.SignaturePoint(x=100, y=40, theta=0, rstart=30, rend=135),
        #first point for detecting in A
        place_rec.SignaturePoint(x=150, y=40, theta=0, rstart=30, rend=150),
        #second point for detecting in A
    ],
    "B": [
        place_rec.SignaturePoint(x=105, y=70, theta=math.pi/2, rstart=22, rend=110),
        place_rec.SignaturePoint(x=105, y=140,  theta=math.pi/2,rstart=-20, rend=160),
    ],
    "C": [
        place_rec.SignaturePoint(x=75, y=50,  theta=math.pi,rstart=0, rend=90),
        place_rec.SignaturePoint(x=60, y=102, theta=math.pi/2, rstart=45,  rend=180),
    ],
    "FINAL": [
        place_rec.SignaturePoint(x=84, y=30,  theta=-math.pi, rstart=0, rend=0),
    ]
}


def main():

    walls.wallmap.draw()

    state = motion_predict.State(
            particles=[motion_predict.Particle(
                    x=BOTTLES["FINAL"][0].x, y=BOTTLES["FINAL"][0].y, theta=0)] * NUMBER_OF_PARTICLES,
            weights=[1.0 / NUMBER_OF_PARTICLES
                     for _ in range(NUMBER_OF_PARTICLES)])
    mcl.draw_particles(state)
    
    # visitpoints is a list of points that we need to visit
    for key, visitpoints in BOTTLES.iteritems():
        
        # Bottles
        if key != "FINAL":
            # waypoint refers to the next destination
            for waypoint, mcl_points in visitpoints:
                
                # Navigate properly
                while True:
                    x_is_close = abs(state.x - waypoint.x) <= WAYPOINT_MIN_OFFSET
                    y_is_close = abs(state.y - waypoint.y) <= WAYPOINT_MIN_OFFSET
    
                    if x_is_close and y_is_close:
                        # We have reached our destination
                        break
                    else:
                        # TO DO: Smart navigation with not many rotations
                        state = uncertainNavigate(state, waypoint)
                        # Run MCL
                        state = sigPointMCLStep(state, mcl_points)
                        print "CURRENT STATE: x=%f, y =%f, theta=%f" % (state.x, state.y, state.theta)
    
                # Make sure your orientation is the same as the orientation a signature must be taken at 
                state = uncertainRotate(state, waypoint)

                # Compare signatures
                bottle_loc = get_bottle(waypoint)

                # We did not find a bottle, go to the next waypoint
                # TO DO: What to do if we went to all waypoints and we still did not hit a bottle
                if bottle_loc is None:
                    print "BOTTLE NOT DETECTED"
                    continue
                # We have a possible bottle location
                else:
                    # 1. Try navigating to the bottle.
                    distance, hit_bottle = motor_params.slow_down_forward(
                            bottle_loc.distance,
                            place_rec.bump_termination_callback,
                            overshoot=15.0)
                    # Don't perform MCL here, we are fairly sure that it will
                    # screw up. (Due to the bottle).
                    state = state.move_forward(distance)

                    # 2. Regardless of whether we hit the bottle or not.
                    # TODO(fyquah): Possibly a better strategy?
                    motor_params.forward(-distance)
                    state = state.move_forward(-distance)

                    if hit_bottle:
                        # 3. Break if we hit the bottle. Then we go on to
                        #    handle the next bottle area.
                        break
                    else:
                        # 4. if we did not hit a bottle, we continue the loop.
                        #    Going to the next waypoint in the area.
                        continue
        # Final endpoint
        else:
            waypoint = visitpoints[0]

            # Navigate properly
            while True:
                x_is_close = abs(state.x - waypoint.x) <= FINAL_WAYPOINT_MIN_OFFSET
                y_is_close = abs(state.y - waypoint.y) <= FINAL_WAYPOINT_MIN_OFFSET
    
                if x_is_close and y_is_close:
                    # We have reached our destination
                    break
                else:
                    # TO DO: Make sure you are tunning MCL facing to the proper walls
                    state = motion_predict.navigateToWaypoint(state, waypoint)
                    state = mcl.MCLStep(state)
                    print "CURRENT STATE: x=%f, y =%f, theta=%f" % (state.x, state.y, state.theta)
    
    

if __name__ == "__main__":
    main()
