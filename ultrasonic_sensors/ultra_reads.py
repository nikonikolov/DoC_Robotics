from ultrasound import get_reading
from time import sleep



while True:
	print "--" + str(get_reading())
	sleep(0.1)
	print "++" + str(get_reading())
	sleep(0.1)
