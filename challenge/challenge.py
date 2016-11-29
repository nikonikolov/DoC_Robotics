import math
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../pmotion')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../ultrasonic_sensors')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../MCL')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '../place_rec')

import motion_predict
import walls
import mcl
import place_rec

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
    ls_normal.read(sig_point, NORMAL_DIR)
    
    ls_bottle = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend, sig_point)
    ls_bottle.save(sig_point, BOTTLE_DIR)

    return place_rec.get_bottle_belief(ls_bottle, ls_normal, sig_point)


def main():

    WAYPOINTS = place_rec.SIGNATURE_POINTS

    walls.wallmap.draw()

    state = motion_predict.State(
            particles=[motion_predict.Particle(
                    x=WAYPOINTS[0].x, y=WAYPOINTS[0].y, theta=0)] * NUMBER_OF_PARTICLES,
            weights=[1.0 / NUMBER_OF_PARTICLES
                     for _ in range(NUMBER_OF_PARTICLES)])
    mcl.draw_particles(state)
    
    # visitpoints is a list of points that we need to visit
    for key, visitpoints in BOTTLES.iteritems():
        
        # Bottles
        if key != "FINAL":
            # waypoint refers to the next destination
            for waypoint in visitpoints:
                
                # Navigate properly
                while True:
                    x_is_close = abs(state.x - waypoint.x) <= WAYPOINT_MIN_OFFSET
                    y_is_close = abs(state.y - waypoint.y) <= WAYPOINT_MIN_OFFSET
    
                    if x_is_close and y_is_close:
                        # We have reached our destination
                        break
                    else:
                        # TO DO: Decide where to run MCL
                        state = motion_predict.navigateToWaypoint(state, waypoint)
                        state = mcl.MCLStep(state)
                        print "CURRENT STATE: x=%f, y =%f, theta=%f" % (state.x, state.y, state.theta)
    
                # TO DO: Make sure orientation is ok if you are trying to find a bottle

                # Compare signatures
                bottle_loc = get_bottle(waypoint)

                # We did not find a bottle, go to the next waypoint
                # TO DO: What to do if we went to all waypoints and we still did not hit a bottle
                if bottle_loc is None:
                    print "BOTTLE NOT DETECTED"
                    continue

                # We have a a possible bottle location
                # TO DO: Handle case when there are more than one bottles
                else:
                    # TO DO: Navigate to the bottle with state uncertainty update
                    # TO DO: Navigate back - how        
                    print "BOTTLE DETECTED AT: ", bottle_loc
                    
                    motor_params.rotate(bottle_loc.angle)
                    motor_params.interface.setMotorRotationSpeedReferences(
                            motor_params.motors, [8.0, 8.0])
                    left = 0
                    right = 0
                    motor_params.slow_down_forward(
                            bottle_loc.distance, bump_termination_callback)

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
