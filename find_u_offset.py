import math
import motor_params
from ultrasonic_sensors import ultrasound

raw_input("Please make sure that the ultrasonic sensor is facing forwards. Then, Please hit enter.")
print "Angle: ", motor_params.interface.getMotorAngle(2)[0] * 180.0 / math.pi
