import math
import os
import sys

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


def plot_data(data, plot_name=None):
    if plot_name==None:
        plot_name=""

    time = data[0]
    refAngle0 = data[1]
    angle0 = data[2]
    refAngle1 = data[3]
    angle1 = data[4]
    npRefAngle0 = np.array(refAngle0)
    npAngle0 = np.array(angle0)
    npRefAngle1 = np.array(refAngle1)
    npAngle1 = np.array(angle1)
    error0 = npRefAngle0 - npAngle0
    error1 = npRefAngle1 - npAngle1

    plt.figure()
    plt.title("Motor 0 " + plot_name)
    plt.plot(time, refAngle0, 'b-', label='refAngle0')
    plt.plot(time, angle0, 'r-', label='angle0')
    #plt.xticks(np.arange(min(time), max(time), .1))
    #plt.yticks(np.arange(min(min(refAngle1), min(refAngle0))-0.5, max(max(refAngle1), max(refAngle0))+0.5, .1))
    plt.xticks(np.arange(min(time), max(time), .1))
    plt.yticks(np.arange(min(refAngle0)-0.5, max(refAngle0)+0.5, .1))
    plt.grid()

    plt.figure()
    plt.title("Motor 0 " + plot_name)
    plt.plot(time, refAngle1, 'g-', label='refAngle1')
    plt.plot(time, angle1, 'y-', label='angle1')
    plt.xticks(np.arange(min(time), max(time), .1))
    plt.yticks(np.arange(min(refAngle1)-0.5, max(refAngle1)+0.5, .1))
    plt.grid()

    plt.figure()
    plt.title("Errors " + plot_name)
    plt.plot(time, error0, 'c-', label='error0')
    plt.plot(time, error1, 'k-', label='error1')
    plt.grid()


def main(args):
    total_1 = 17
    total_2 = len(args) - total_1

    plt.figure()
    for i, argv in enumerate(args[:17]):
        data = read_file(argv)
        plt.subplot(math.ceil(total_1 / 5.0), 5, i + 1)
        plot_data(data)

    plt.figure()
    for i, argv in enumerate(args[17:]):
        data = read_file(argv)
        plt.subplot(math.ceil(total_2 / 5.0), 5, i + 1)
        plot_data(data)
    plt.show()


#main(sys.argv[1:])
#data = read_file("a.log")
for arg in sys.argv[1:]:

    data = read_file(sys.argv[1])
    plot_data(data, arg)

plt.show()

