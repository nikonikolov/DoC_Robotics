import time

import brickpi


T = 0.4
G = 800

interface = brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParamsLeft = interface.MotorAngleControllerParameters()
motorParamsLeft.maxRotationAcceleration = 8.0
motorParamsLeft.maxRotationSpeed = 12.0
motorParamsRight = interface.MotorAngleControllerParameters()
motorParamsRight.maxRotationAcceleration = 8.0
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
motorParamsRight.pidParameters.k_p = 0.58*G
motorParamsRight.pidParameters.k_i = 2*motorParamsRight.pidParameters.k_p/T*0.3
motorParamsRight.pidParameters.K_d = motorParamsRight.pidParameters.k_p*T/8

interface.setMotorAngleControllerParameters(motors[0], motorParamsLeft)
interface.setMotorAngleControllerParameters(motors[1], motorParamsRight)


def TurnOpposite(angle):
    """Given angle for motor 0, rotate 0 and 1 in opposite directions.
    """
    interface.increaseMotorAngleReferences(motors, [angle, -angle])

    while not interface.motorAngleReferencesReached(motors):
	time.sleep(0.03)
    interface.setMotorPwm(motors[0], 0)
    interface.setMotorPwm(motors[1], 0)
    print "Destination reached!"


def Left90deg():
    rotate(-90)


def Right90deg():
    rotate(90)


# dist is in cm
def dist_to_motor_angle(dist):
    # Small wheels
    return (dist*0.362569757118 + 0.152055463539) 
    # Big wheels
    #return (dist*0.2959687 + 0.1) 
    #return (dist*0.2959687 - 0.03339163) 

# angle is in degrees
def rotate_right_to_motor_angle(angle):
    # Small Wheels
    return (angle*0.0444657336443 + -0.0642952349217)
    # Big Wheels
    #return (angle*0.038050073 + 0.0675)
    
# angle is in degrees
def rotate_left_to_motor_angle(angle):
    # Small Wheels
    return (angle*0.0.0437977717284 + 0.0235027479275)
    # Big Wheels
    #return (angle*0.038050073 + 0.0675)

#angle is in degrees - positive angle turns right
def rotate(angle):
    #wheels_dist = 13.6 
    #perimeter = 2*math.pi*(wheels_dist/2) 
    #travel_dist = angle/360*perimeter
    #motor_angle = dist_to_motor_angle(travel_dist)
    if angle>0:
        motor_angle = rotate_right_to_motor_angle(angle)
    elif angle<0:
        motor_angle = rotate_left_to_motor_angle(angle)
    else:
        motor_angle = 0
    TurnOpposite(motor_angle)

def forward(dist):
    angle = dist_to_motor_angle(dist)
    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
        time.sleep(0.03)
    interface.setMotorPwm(motors[0], 0)
    interface.setMotorPwm(motors[1], 0)
    print "Destination reached!"


# angle is in radians
def motor_rotate(angle):
    interface.increaseMotorAngleReferences(motors,[angle,angle])

    while not interface.motorAngleReferencesReached(motors) :
        time.sleep(0.03)
    interface.setMotorPwm(motors[0], 0)
    interface.setMotorPwm(motors[1], 0)
    print "Destination reached!"





