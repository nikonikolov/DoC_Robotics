import numpy as np
import matplotlib.pyplot as plt

def read_file(filename):
	f = open(filename, 'r')
	
	time = []
	refAngle0 = []
	angle0 = []
	refAngle1 = []
	angle1 = []

	for line in f:
		nums = line.split()
		if len(nums) == 5:
			time.append(float(nums[0]))
			refAngle0.append(float(nums[1]))
			angle0.append(float(nums[2]))
			refAngle1.append(float(nums[3]))
			angle1.append(float(nums[4]))

	return time, refAngle0, angle0, refAngle1, angle1


def plot_data(data):
	time = data[0]
	refAngle0 = data[1]
	angle0 = data[2]
	refAngle1 = data[3]
	angle1 = data[4]


	plt.plot(time, refAngle0, 'b-', label='refAngle0')
	plt.plot(time, angle0, 'r-', label='angle0')
	plt.plot(time, refAngle1, 'g-', label='refAngle1')
	plt.plot(time, angle1, 'y-', label='angle1')
	plt.xticks(np.arange(0, max(refAngle1), .1))
	plt.grid()
	plt.savefig('a.jpg')
	plt.show()


data = read_file("a.log")
plot_data(data)

