#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import math
import os
import sys
import collections

import numpy as np

sys.path.append('/home/pi/DoC_Robotics')
sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import motor_params
import ultrasound

# NOTE: if you change this, reading a signature from file might read a wrong signature; Comparing signatures will also fail; Solution - delete all current signatures
STEP = 5

FACE_FORWARD = math.pi / 2
FACE_LEFT = math.pi
FACE_RIGHT = 0.0
FACE_BACK = -math.pi / 2

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
NORMAL_DIR = SCRIPT_DIR + "/data/normal/"
BOTTLE_DIR = SCRIPT_DIR + "/data/bottles/"

SignaturePoint = collections.namedtuple(
        "SignaturePoint", ["x", "y", "theta", "rstart", "rend"])

SIGNATURE_POINTS = [
    SignaturePoint(x=1, y=1, theta=5, rstart=30, rend=150),
]
# Angle is in degrees, distance is in cm.
BottleLocation = collections.namedtuple(
        "BottleLocation", ["angle", "distance"])


def remove_cluster_anomalies(clusters):
    if len(clusters) == 0:
        return clusters
    threshold = math.floor(0.7 * max(c[1] - c[0] for c in cluters))
    threshold = threshold or 1
    return [c for c in clusters if c[1] - c[0] > threshold]


def binary_signal_partition_by(arr):
    in_signal = False
    indices = []
    beginning = 0
    for i, v in enumerate(arr):
        if in_signal:
            if not v:
                indices.append((beginning, i))
                in_signal = False
        else:
            if v:
                beginning = i
                in_signal = True
    if in_signal:
        indices.append((beginning, len(arr)))
    return indices


def get_bottle_belief(test_signature, observed_signature, point):
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
    # TODO(fyquah): Dynamically calculate this based on the test signature.
    threshold = 200.0
    thresholded = [1 if ((observed - expected) ** 2) > 200.0 else 0
                   for observed, expected
                   in zip(observations, test_signature.sig)]
    print thresholded
    print "Observations:"
    print observations
    print "Expected:"
    print test_signature.sig
    clusters = remove_cluster_anomalies(binary_signal_partition_by(thresholded))
    if len(clusters) == 1:
        cluster_indices = range(clusters[0][0], clusters[0][1])
        cluster_readings = [observations[i] for i in cluster_indices]
        distance = np.median(cluster_readings) + 10.0
        angle = np.median([angles[i] for i in cluster_indices])
        return BottleLocation(
                distance=distance, angle=angle - 90.0)
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
        filename = "%s%d.%d.%d.dat" % (
                target_dir, sig_point.x, sig_point.y, int(STEP))
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
            if sig_point.x == int(args[0]) and sig_point.y == int(args[1]):
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


def test_production():
    for sig_point in SIGNATURE_POINTS:

        ls_normal = LocationSignature()
        ls_normal.read(sig_point, NORMAL_DIR)

        raw_input("Place a bottle somewhere and press enter")    

        ls_bottle = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend)
        ls_bottle.save(sig_point, BOTTLE_DIR)
    
        bottle_loc = get_bottle_belief(ls_bottle, ls_normal, sig_point)

        if bottle_loc is not None:
            print bottle_loc
            motor_params.rotate(bottle_loc.angle)
            motor_params.forward(bottle_loc.distance)
        else:
            print "Bottle loc is None!"

        raw_input("Place the robot in a the next signature point for a new test and press enter")    

def test_performance():
    for sig_point in SIGNATURE_POINTS:

        ls_normal = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend)
        ls_normal.save(sig_point, NORMAL_DIR)

        raw_input("Place a bottle somewhere and press enter")    

        ls_bottle = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend)
        ls_bottle.save(sig_point, BOTTLE_DIR)
    
        bottle_loc = get_bottle_belief(ls_normal, ls_bottle, sig_point)

        print bottle_loc

        motor_params.rotate(bottle_loc.angle)
        motor_params.forward(bottle_loc.distance)


        raw_input("Place the robot in a the next signature point for a new test and press enter")    

def show_plots(test_sig, observed_sig):
    for sig_point in SIGNATURE_POINTS:

        observed_sig = LocationSignature()
        observed_sig.read(sig_point, NORMAL_DIR)

        raw_input("Place a bottle somewhere and press enter")    

        test_sig = LocationSignature()
        test_sig.read(sig_point, BOTTLE_DIR)

        error = get_correlation_diff()

        plt.figure()
        plt.title("Observed Signature")
        plt.plot(observed_sig.sig)

        plt.figure()
        plt.title("Test Signature")
        plt.plot(test_sig.sig)

        plt.figure()
        plt.title("Correlation Error")
        plt.plot(error)

        plt.show()

rot_sensor = RotatingSensor()

def main():
    test_production()

if __name__ == "__main__":
    main()
