#import brickpi
import time
import motor_params

interface = motor_params.interface

ULTRASONIC_PORT = 2 

interface.sensorEnable(ULTRASONIC_PORT, brickpi.SensorType.SENSOR_ULTRASONIC);
desired_dist = 30

while True:
	usReading = interface.getSensorValue(ULTRASONIC_PORT)

	if usReading :
		dist = usReading[0]
		error = desired_dist - dist
		if error => 1 or error <= -1:
			motor_params.motorParamsLeft.maxRotationSpeed = motor_params.motorParamsRight.maxRotationSpeed = error
			motor_params.updateParams()
	else:
		print "Failed US reading"

	time.sleep(0.05)

interface.terminate()
