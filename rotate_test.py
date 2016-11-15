import motor_params
input = float(raw_input("Enter angle: "))
if input < 0:
	angle = (360.0 / 335.0) * input
else:
	angle = (360.0 / 332.5) * input

motor_params.rotate(angle)
