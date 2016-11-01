import brickpi
import time
import motor_params
import numpy as np

interface = motor_params.interface

ULTRASONIC_PORT = 2 
DESIRED_DIST = 30

# TUNE THESE VALUES
NORMAL_SPEED = 10.0
MAX_SPEED = max(motor_params.motorParamsRight.maxRotationSpeed, motor_params.motorParamsLeft.maxRotationSpeed)
MIN_SPEED = 3.0


def get_reading():
    us_reading = interface.getSensorValue(ULTRASONIC_PORT)

    if us_reading :
        dist = us_reading[0]

        if len(get_reading.history) >= get_reading.HISTORY_SIZE:
            get_reading.history.pop(0)

        get_reading.history.append(dist)    
        return np.median(get_reading.history)
    else:
        print "Failed US reading"
        return None

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
    interface.sensorEnable(ULTRASONIC_PORT, brickpi.SensorType.SENSOR_ULTRASONIC);
    get_reading.history = []
    get_reading.HISTORY_SIZE = 5

    # TUNE THESE VALUES
    keep_front_distance.K_P = 0.6
    keep_front_distance.ERROR_TRESHOLD = 1.0

    follow_wall.K_P = 1.0
    follow_wall.ERROR_TRESHOLD = 1.0

    keep_front_distance()
    #follow_wall()


main()
