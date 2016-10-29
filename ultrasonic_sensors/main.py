#import brickpi
import time
import motor_params
import numpy as np

interface = motor_params.interface

ULTRASONIC_PORT = 2 
HISTORY_SIZE = 5
ERROR_TRESHOLD = 1.0
K_P = 1.0
DEISRED_DIST = 30



def get_reading():
	us_reading = interface.getSensorValue(ULTRASONIC_PORT)

	if us_reading :
		dist = us_reading[0]

		if len(get_reading.history>=5):
			get_reading.history.pop(0)
		get_reading.history.append(dist)	
		return med_dist = np.median(get_reading.history)
	else:
		print "Failed US reading"
		return None

def main():
	interface.sensorEnable(ULTRASONIC_PORT, brickpi.SensorType.SENSOR_ULTRASONIC);

	get_reading.history = []

	while True:
		dist = get_reading()

		if dist != None:

			error = DEISRED_DIST - dist
			speed = - K_P * error
			if error => ERROR_TRESHOLD or error <= -ERROR_TRESHOLD:
				interface.setMotorRotationSpeedReferences(motor_params.motors, [speed,speed])
			else:
			    interface.setMotorPwm(motor_params.MOTOR_LEFT, 0)
	    		interface.setMotorPwm(motor_params.MOTOR_RIGHT, 0)

		time.sleep(0.05)
