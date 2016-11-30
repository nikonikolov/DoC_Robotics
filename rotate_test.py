import motor_params
input = float(raw_input("Enter angle: "))
if input < 0:
	angle = (345.0 / 360.0) * input
else:
	angle = (345.0 / 360.0) * input

motor_params.rotate(angle)
motor_params.rotate(angle)
motor_params.rotate(angle)
motor_params.rotate(angle)
