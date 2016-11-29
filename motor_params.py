import threading
import time

import brickpi


T = 0.4
G = 750

interface = brickpi.Interface()
interface.initialize()

motors = [0,1]
MOTOR_LEFT = 0
MOTOR_RIGHT = 1

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParamsLeft = interface.MotorAngleControllerParameters()
motorParamsLeft.maxRotationAcceleration = 11.55
motorParamsLeft.maxRotationSpeed = 12.0
motorParamsRight = interface.MotorAngleControllerParameters()
motorParamsRight.maxRotationAcceleration = 12.0
motorParamsRight.maxRotationSpeed = 12.0
# tune all the following parameters

motorParamsLeft.feedForwardGain = 255/20.0
motorParamsLeft.minPWM = 18.0
motorParamsLeft.pidParameters.minOutput = -255
motorParamsLeft.pidParameters.maxOutput = 255
motorParamsLeft.pidParameters.k_p = 0.6*G
#motorParamsLeft.pidParameters.k_i = 2*motorParamsLeft.pidParameters.k_p/T*0.3
motorParamsLeft.pidParameters.k_i = 1.3*motorParamsLeft.pidParameters.k_p/T
motorParamsLeft.pidParameters.K_d = motorParamsLeft.pidParameters.k_p*T/8

motorParamsRight.feedForwardGain = 255/20.0
motorParamsRight.minPWM = 18.0
motorParamsRight.pidParameters.minOutput = -255
motorParamsRight.pidParameters.maxOutput = 255
motorParamsRight.pidParameters.k_p = 0.6*G
#motorParamsRight.pidParameters.k_i = 2*motorParamsRight.pidParameters.k_p/T*0.3
motorParamsRight.pidParameters.k_i = 1.3*motorParamsRight.pidParameters.k_p/T
motorParamsRight.pidParameters.K_d = motorParamsRight.pidParameters.k_p*T/8

interface.setMotorAngleControllerParameters(motors[MOTOR_LEFT], motorParamsLeft)
interface.setMotorAngleControllerParameters(motors[MOTOR_RIGHT], motorParamsRight)


def updateParams(motorParams, motor_idx=None):
    if motor_idx==None:
        interface.setMotorAngleControllerParameters(motors[MOTOR_LEFT], motorParamsLeft)
        interface.setMotorAngleControllerParameters(motors[MOTOR_RIGHT], motorParamsRight)
    else:
        if motor_idx == MOTOR_RIGHT:
            interface.setMotorAngleControllerParameters(motors[motor_idx], motorParamsRight)
        elif motor_idx == MOTOR_LEFT:
            interface.setMotorAngleControllerParameters(motors[motor_idx], motorParamsLeft)
        else:
            print "Warning wrong motor port [%d] in motor_params.updateParams " % motor_idx

def TurnOpposite(angle):
    """Given angle for motor 0, rotate 0 and 1 in opposite directions.
    """
    interface.increaseMotorAngleReferences(motors, [angle, -angle])

    while not interface.motorAngleReferencesReached(motors):
	time.sleep(0.03)
    print "Destination reached!"


def Left90deg():
    rotate(90)


def Right90deg():
    rotate(-90)


# dist is in cm
def dist_to_motor_angle(dist):
    # Small wheels
    return (dist*0.362569757118 + 0.172055463539) 
    # Big wheels
    #return (dist*0.2959687 + 0.1) 
    #return (dist*0.2959687 - 0.03339163) 

# angle is in degrees
def rotate_right_to_motor_angle(angle):
    return 360.0 / 335.0 * (angle*0.0444657336443 + -0.0442952349217)
    # Small Wheels
    # return (angle*0.0444657336443 + -0.0442952349217)
    # Big Wheels
    #return (angle*0.038050073 + 0.0675)
    
# angle is in degrees
def rotate_left_to_motor_angle(angle):
    return 360.0 / 332.5 * (angle*0.0437977717284 - 0.0205027479275)
    # Small Wheels with refreshed PID values
    # return (angle*0.0437977717284 - 0.0205027479275)
    # Small Wheels
    # return (angle*0.0437977717284 + 0.0235027479275)
    # Big Wheels
    #return (angle*0.038050073 + 0.0675)

#angle is in degrees - positive angle turns left
def rotate(angle):
    #wheels_dist = 13.6 
    #perimeter = 2*math.pi*(wheels_dist/2) 
    #travel_dist = angle/360*perimeter
    #motor_angle = dist_to_motor_angle(travel_dist)
    if angle<0:
        motor_angle = rotate_right_to_motor_angle(-angle)
    elif angle>0:
        motor_angle = rotate_left_to_motor_angle(-angle)
    else:
        motor_angle = 0
    TurnOpposite(motor_angle)


def better_dist_to_motor_angle(dist):
    if dist > 0:
        angle = dist_to_motor_angle(dist)
    elif dist < 0:
        angle = -dist_to_motor_angle(-dist)
    else:
        angle = 0
    return angle * 40.0 / 38.84


def forward(dist):
    angle = better_dist_to_motor_angle(dist)
    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
        time.sleep(0.03)
    print "Destination reached!"


def angle_to_dist(angle):
    """Angles is in degrees. Used for forward calculation."""
    return (angle * 38.84 / 40.0 - 0.172055463539) / 0.362569757118



def slow_down_forward(dist, termination_callback, overshoot=0.0):
    """
    Forward with decreasing velocity as we get close to an object.

    Arguments:
        dist: The distance in centimeters to move the roboto.
        termination_callback: A callback that is run, with no arguments
                              at every loop iteration. If the callback
                              returns True, the motors stop immediately.
    """
    distance_moved = 0.0
    hit_bottle = False
    beginning_angle = interface.getMotorAngle(0)[0]
    interface.setMotorRotationSpeedReferences(
            motors, [20.0, 20.0])
    while distance_moved < dist + overshoot:
        if termination_callback():
            hit_bottle = True
            break
        angle = interface.getMotorAngle(0)[0]
        distance_moved = angle_to_dist(angle - beginning_angle)
        # Multiply by 0.7, just to be more conservative about the distance.
        speed = max(3.0, min(8.0, dist * 0.7 - distance_moved))
        interface.setMotorRotationSpeedReferences(
                motors, [speed, speed])
    interface.setMotorPwm(motors[0], 0)
    interface.setMotorPwm(motors[1], 0)
    return distance_moved, hit_bottle


# angle is in radians
def motor_rotate(angle):
    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
        time.sleep(0.03)
    print "Destination reached!"


def main():
    forward(50)

if __name__ == "__main__":
    main()
