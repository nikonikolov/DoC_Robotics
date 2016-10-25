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
