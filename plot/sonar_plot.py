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
        if len(nums) == 3:
            time.append(float(nums[0]))
            refAngle0.append(float(nums[1]))
            angle0.append(float(nums[2]))

    return time, refAngle0, angle0


def plot_data(data, plot_name=None):
    if plot_name==None:
        plot_name=""

    time, refAngle, angle = data
    npRefAngle = np.array(refAngle)
    npAngle = np.array(angle)
    error = npRefAngle - npAngle

    plt.figure()
    plt.title("Motor : " + plot_name)
    plt.plot(time, refAngle, 'b-', label='refAngle0')
    plt.plot(time, angle, 'r-', label='angle0')
    plt.xticks(np.arange(min(time), max(time), .1))
    plt.yticks(np.arange(min(refAngle)-0.5, max(refAngle)+0.5, .1))
    plt.grid()

    plt.figure()
    plt.title("Errors : " + plot_name)
    plt.plot(time, error, 'c-', label='error0')
    plt.grid()


def main(args):
    for arg in sys.argv[1:]:
        data = read_file(arg)
        plot_data(data, arg.split(".")[0])

    plt.show()


if __name__ == "__main__":
    main(sys.argv)
