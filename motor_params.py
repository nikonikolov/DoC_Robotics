import time

import brickpi


T = 0.4
G = 800

interface = brickpi.Interface()
interface.initialize()

motors = [0,1]
MOTOR_LEFT = 0
MOTOR_RIGHT = 1

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParamsLeft = interface.MotorAngleControllerParameters()
motorParamsLeft.maxRotationAcceleration = 8.0
motorParamsLeft.maxRotationSpeed = 12.0
motorParamsRight = interface.MotorAngleControllerParameters()
motorParamsRight.maxRotationAcceleration = 8.2
motorParamsRight.maxRotationSpeed = 12.0
# tune all the following parameters

motorParamsLeft.feedForwardGain = 255/20.0
motorParamsLeft.minPWM = 18.0
motorParamsLeft.pidParameters.minOutput = -255
motorParamsLeft.pidParameters.maxOutput = 255
motorParamsLeft.pidParameters.k_p = 0.6*G
motorParamsLeft.pidParameters.k_i = 2*motorParamsLeft.pidParameters.k_p/T*0.3
motorParamsLeft.pidParameters.K_d = motorParamsLeft.pidParameters.k_p*T/8

motorParamsRight.feedForwardGain = 255/20.0
motorParamsRight.minPWM = 18.0
motorParamsRight.pidParameters.minOutput = -255
motorParamsRight.pidParameters.maxOutput = 255
motorParamsRight.pidParameters.k_p = 0.6*G
motorParamsRight.pidParameters.k_i = 2*motorParamsRight.pidParameters.k_p/T*0.3
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

#angle is in degrees - positive angle turns right
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

def forward(dist):
    if dist > 0:
        angle = dist_to_motor_angle(dist)
    elif dist < 0:
        angle = -dist_to_motor_angle(-dist)
    else:
        angle = 0
    angle = angle * 40.0 / 38.84
    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
        time.sleep(0.03)
    print "Destination reached!"


# angle is in radians
def motor_rotate(angle):
    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
        time.sleep(0.03)
    print "Destination reached!"
