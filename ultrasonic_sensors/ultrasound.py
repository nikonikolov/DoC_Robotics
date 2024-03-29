import math
import time
import numpy as np
import brickpi
import motor_params

SONAR_MOTOR_PORT = 2
ULTRASONIC_PORT = 3

# TO DO - CALIBRATE THESE VALUES
SENSOR_OFFSET = 3.0                             # Offset of the sensor from the center of the robot
MAX_DIST = 100.0 + SENSOR_OFFSET                # Max distance from a wall for a reliable reading
MIN_DIST = 10.0 + SENSOR_OFFSET                 # Min distance from a wall for a reliable reading 
MAX_ANGLE = 34.0 * math.pi / 180.0              # Max angle between wall normal and the robot for a reliable reading

# Number of readings to take before get_reading() returns a value 
NUM_READINGS = 3
GARBAGE = 265.0
GARBAGE_THRESHOLD = 120.0

interface = motor_params.interface

def get_reading():
    for _ in range(NUM_READINGS): 
        us_reading = interface.getSensorValue(ULTRASONIC_PORT)

        if us_reading :
            dist = us_reading[0]

            if len(get_reading.history) >= get_reading.HISTORY_SIZE:
                get_reading.history.pop(0)

            get_reading.history.append(dist)    
            med_reading = np.median(get_reading.history)
        else:
            print "Failed Reading"
    
    if med_reading < 20:
        med_reading +=3.5
    med_reading += SENSOR_OFFSET
    # print "US Reading: " + str(med_reading)
    
    return med_reading


def rotate_sensor(angle):
    """
        @param: angle - the angle the motor should rotate by - in radians
    """
    interface.increaseMotorAngleReference(SONAR_MOTOR_PORT, angle)
    while not interface.motorAngleReferenceReached(SONAR_MOTOR_PORT):
	time.sleep(0.03)
    # print "Ultrasonic rotation reached."


#OLD PRACTICAL PARAMS
DESIRED_DIST = 30
NORMAL_SPEED = 10.0
MAX_SPEED = max(motor_params.motorParamsRight.maxRotationSpeed, motor_params.motorParamsLeft.maxRotationSpeed)
MIN_SPEED = 3.0

def get_sleep_time(error):
    default_sleep = 0.08
    max_sleep = 0.08
    min_sleep = 0.06
    
    tuning_dist_max = 15.0
    tuning_dist_min = 0.0
    
    if abs(error) >= tuning_dist_max:
        return max_sleep
    return abs(error)/tuning_dist_max*(max_sleep - min_sleep) + min_sleep
def keep_front_distance():
    default_sleep = 0.08
    while True:
        dist = get_reading()
        
        #print dist
        if dist != None:
            error = DESIRED_DIST - dist
            speed = - keep_front_distance.K_P * error
            if error >= keep_front_distance.ERROR_TRESHOLD or error <= -keep_front_distance.ERROR_TRESHOLD:
                interface.setMotorRotationSpeedReferences(motor_params.motors, [speed,speed])
            else:
                interface.setMotorPwm(motor_params.MOTOR_LEFT, 0)
                interface.setMotorPwm(motor_params.MOTOR_RIGHT, 0)
            
            sleep_time = get_sleep_time(error)
        #time.sleep(0.08)
        time.sleep(sleep_time)
        sleep_time = default_sleep

def follow_wall():
    while True:
        dist = get_reading()

        if dist != None:
            error = DESIRED_DIST - dist
            speed_difference = - K_P * error
    
            if error >= follow_wall.ERROR_TRESHOLD or error <= -follow_wall.ERROR_TRESHOLD:
                speed_left = NORMAL_SPEED - speed_difference/2
                speed_right = NORMAL_SPEED - speed_difference/2
    
                if speed_right > MAX_SPEED: 
                    speed_right = MAX_SPEED
                if speed_left > MAX_SPEED: 
                    speed_left = MAX_SPEED
                if speed_right < MIN_SPEED: 
                    speed_right = MIN_SPEED
                if speed_left < MIN_SPEED: 
                    speed_left = MIN_SPEED

                interface.setMotorRotationSpeedReference(motor_params.MOTOR_LEFT, speed_left)
                interface.setMotorRotationSpeedReference(motor_params.MOTOR_RIGHT, speed_right)
            else:
                interface.setMotorRotationSpeedReferences(motor_params.motors, [NORMAL_SPEED,NORMAL_SPEED])
        time.sleep(0.05)


def main():
    # TUNE THESE VALUES
    keep_front_distance.K_P = 0.6
    keep_front_distance.ERROR_TRESHOLD = 1.0

    follow_wall.K_P = 1.0
    follow_wall.ERROR_TRESHOLD = 1.0

    keep_front_distance()
    #follow_wall()


def setup():
    # Setup ultrasonic sensor here.
    interface.sensorEnable(ULTRASONIC_PORT, brickpi.SensorType.SENSOR_ULTRASONIC);
    get_reading.history = []
    get_reading.HISTORY_SIZE = 3

    # The motor holding the sonar sensor.
    G = 250.0
    T = 0.4
    interface.motorEnable(SONAR_MOTOR_PORT)
    sonar_motor_params = interface.MotorAngleControllerParameters()
    sonar_motor_params.maxRotationAcceleration = 9.0
    sonar_motor_params.maxRotationSpeed = 12.0
    sonar_motor_params.feedForwardGain = 255/20.0
    sonar_motor_params.minPWM = 18.0
    sonar_motor_params.pidParameters.minOutput = -255
    sonar_motor_params.pidParameters.maxOutput = 255
    kp = 0.6 * G
    sonar_motor_params.pidParameters.k_p = kp
    sonar_motor_params.pidParameters.k_i = 3.3 * kp / T
    sonar_motor_params.pidParameters.K_d = 1.5 * kp * T / 8.0
    interface.setMotorAngleControllerParameters(SONAR_MOTOR_PORT, sonar_motor_params)


def simple_rotate():
    rotate_sensor(math.pi)
    rotate_sensor(-math.pi)


def calibrate():
    G = 1000
    kp_values = [150, 200, 250]

    for i, kp in enumerate(kp_values):
        print "kp =", kp
        interface.startLogging("plot/sonar_logs/sonar_kp_%d.log" % int(kp))
        sonar_motor_params = interface.MotorAngleControllerParameters()
        sonar_motor_params.maxRotationAcceleration = 8.0
        sonar_motor_params.maxRotationSpeed = 12.0
        sonar_motor_params.feedForwardGain = 255/20.0
        sonar_motor_params.minPWM = 18.0
        sonar_motor_params.pidParameters.minOutput = -255
        sonar_motor_params.pidParameters.maxOutput = 255
        sonar_motor_params.pidParameters.k_p = kp
        sonar_motor_params.pidParameters.k_i = 0
        sonar_motor_params.pidParameters.K_d = 0
        interface.setMotorAngleControllerParameters(SONAR_MOTOR_PORT, sonar_motor_params)

        rotate_sensor(math.pi)
        rotate_sensor(-math.pi)
        rotate_sensor(math.pi)
        rotate_sensor(-math.pi)
        interface.stopLogging()
    interface.terminate()


# setup on import
setup()


if __name__== "__main__":
    simple_rotate()
