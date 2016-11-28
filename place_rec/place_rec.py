#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import math
import os
import sys
import collections

import numpy as np
import matplotlib.pyplot as plt

sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

#import ultrasound

# NOTE: if you change this, reading a signature from file might read a wrong signature; Comparing signatures will also fail; Solution - delete all current signatures
STEP = 5

FACE_FORWARD = math.pi / 2
FACE_LEFT = math.pi
FACE_RIGHT = 0.0
FACE_BACK = -math.pi / 2

NORMAL_DIR = "/home/pi/DoC_Robotics/place_rec/normal/"
BOTTLE_DIR = "/home/pi/DoC_Robotics/place_rec/bottles/"

SignaturePoint = collections.namedtuple("SignaturePoint", ["x", "y", "theta", "rstart","rend"])

SIGNATURE_POINTS = [
    SignaturePoint(),
]
BottleLocationBelief = collections.namedtuple(
        "BottleLocationBelief", ["angle", "distance"])


def compare(test_signature, observed_signature, point):
    """Check if a bottle is observed.

    Arguments:
        test_signature: The signature without the bottle.
        observed_signature: The signature that we want to test with.
        point: The location where the two signatures were taken.
    Returns:
        The angle of the bottle, relative to point.rstart if we
        believe that a bottle is within sight. None otherwise.
    """
    # signature_point has attributes x, y, theta, rstart, rend
    step = -STEP if point.rstart > point.rend else STEP
    angles = list(range(point.rstart, point.rend, step))
    # The sonar observations.
    observations = observed_signature.sig
    thresholded = [1 if ((observed - expected) ** 2) > 20.0 else 0
                   for observed, expected
                   in zip(observations, test_signature.sig)]
    clusters = binary_signal_partition_by(thresholded)
    if len(clusters) == 1:
        cluster_indices = range(clusters[0][0], clusters[0][1])
        cluster_readings = [observations[i] for i in cluster_indices]
        distance = np.median(cluster_readings) + 10.0
        angle = np.median(angles[i] for i in cluster_indices)
        return BottleLocationBelief(
                distance=distance, angle=math.pi / 2 - angle)
    else:
        return None


class LocationSignature:
    """
        Store a signature characterizing a location
    """
    def __init__(self):
        # signature data
        self.sig = []

    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

    def delete_loc_files(self):
        """
        Delete all files in target_dir
        """
        filenames = os.listdir(target_dir)
        for f in filenames:
            os.remove(f)

    def save(self, sig_point, target_dir):
        """
        Save the signature in a file with a proper name based on the point and STEP
        """
        if self.x == 0 or self.y == 0:
            print "ERROR in SingatureManager.save() - point is not set"
            return

        filename = "%s%d.%d.%d.dat" % (target_dir, self.x, self.y, int(STEP))
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')
        for i in self.sig:
            f.write(str(i) + "\n")
        f.close();

    def read(self, sig_point, target_dir):
        """
        Read a LocationSignature from file based on the location of the point
        If such file does not exists, an empty LocationSignature is returned
        """

        filename = ""
        filenames = os.listdir(target_dir)
        for f in filenames:
            args = f.split(".")
            if x == int(args[0]) and y == int(args[1]):
                filename = f
        if filename == "":
            print "ERROR in SignatureManager.read() - no file with coordinates %d %d %d in %s" % x, y, STEP, target_dir

        f = open(target_dir + filename, 'r')
        for line in f:
            self.sig.append(int(float(line.strip())))
        f.close();

        if not len(self.sig):
            print "WARNING: SignatureManager.read() - signature does not exist"


class RotatingSensor:
    """
        Save state of the rotating sonar sensor and take LocationSignature readings
    """
    def __init__(self, orientation=math.pi / 2):
        """
        Arguments:
            orientation(Number): PI / 2 means it is centered. It is ranged from -PI to PI
                                 Its values are in radians.
        """
        self.orientation = orientation


    def takeSignature(self, start_angle, end_angle):
        """
            Take a signature and return LocationSignature()
            @param start_angle: orientation angle relative to the robot orienation to start taking sonar measurements from - in degrees
            @param end_angle:   orientation angle relative to the robot orienation to end taking sonar measurements - in degrees
        """

        ls = LocationSignature()
        if start_angle > end_angle:
            step = -STEP
        else:
            step = STEP

        for angle in range(int(start_angle), int(end_angle), step):
            self.setOrientation(float(angle) * math.pi / 180)
            ls.sig.append(ultrasound.get_reading())

        return ls

    def setOrientation(self, orientation):
        if orientation < -math.pi:
            orientation = -math.pi
        elif orientation > math.pi:
            orientation = math.pi
        ultrasound.rotate_sensor(self.orientation - orientation)
        self.orientation = orientation
        print "self.orientation =", orientation


def get_signatures_dist(ls1, ls2):
    """
        NOTE: orienation at which the signatures were taken matters
    """
    dist = 0

    for i, val in enumerate(ls1):
        dist += (ls1[i] - ls2[i])**2
    return dist


def get_bottle_angle(ls1, ls2, sig_point):
    """
        NOTE: orienation at which the signatures were taken matters
    """
    max_diff = 0
    max_i = 0
    error = []

    for i, val in enumerate(ls1.sig):
        diff = (ls1.sig[i] - ls2.sig[i])**2
        error.append(diff)
        if diff > max_diff:
            max_i = i
            max_diff = diff

    plt.figure()
    plt.plot(error)
    plt.figure()
    plt.plot(ls1.sig)

    plt.figure()
    plt.plot(ls2.sig)

    return max_i*STEP

rot_sensor = RotatingSensor()

def main():
    #rot_sensor.setOrientation(FACE_FORWARD)
    #rot_sensor.setOrientation(FACE_BACK)
    #rot_sensor.setOrientation(FACE_RIGHT)
    #rot_sensor.setOrientation(FACE_LEFT)
    #rot_sensor.setOrientation(FACE_FORWARD)

    #for sig_point in SIGNATURE_POINTS:

        # Take a measurement with     
    #sig_point = SIGNATURE_POINTS[0]
    #ls = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend)
    #ls.save(sig_point, )

    ls_normal = LocationSignature()
    ls_normal.read(sig_point, NORMAL_DIR)

    #input("Press Enter to continue...")    

    ls_bottle = LocationSignature()
    ls_bottle.read(sig_point, BOTTLE_DIR)
    
    print get_bottle_angle(ls_bottle, ls_normal)

    #plt.show()


if __name__ == "__main__":
    main()
