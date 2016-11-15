import motor_params as mp

angle = (360.0 / 332.5) * 180.0
distance = (40.0 / 38.84) * 40

mp.forward(distance)
mp.rotate(angle)
mp.forward(distance)
mp.rotate(angle)
