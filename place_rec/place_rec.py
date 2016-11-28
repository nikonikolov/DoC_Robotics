#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import math
import os
import sys

sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import ultrasound

# NOTE: if you change this, reading a signature from file might read a wrong signature; Comparing signatures will also fail; Solution - delete all current signatures
STEP = 5

FACE_FORWARD = math.pi / 2
FACE_LEFT = math.pi
FACE_RIGHT = 0.0
FACE_BACK = -math.pi / 2


BottleLocationBelief = collections.namedtuple(
        "BottleLocationBelief", ["angle", "distance"])


def binary_signal_partition_by(arr):
    in_signal = False
    indices = []
    beginning = i
    for i, v in enumerate(arr):
        if in_signal:
            if not v:
                indices.append((beginning, i))
        else:
            if v:
                beginning = i
                in_signal = True
    if in_signal:
        indices.append((beginning, len(arr)))
    return indices


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

    def compare(self, other, point):
        """Check if a bottle is observed.

        Arguments:
            other: Another LocationSignature object.
            point: The point we believe the robot to be.
        Returns:
            The angle of the bottle, relative to point.rstart if we
            believe that a bottle is within sight. None otherwise.
        """
        # signature_point has attributes x, y, theta, rstart, rend
        step = -STEP if rstart > rend else STEP
        angles = list(range(point.rstart, point.rend, step))
        # The sonar observations.
        observations = other.signature
        thresholded = [1 if abs(observed - expected) > 10.0 else 0
                       for observed, expected
                       in zip(observations, self.sig)]
        clusters = binary_signal_partition_by(thresholded)
        if len(clusters) == 1:
            cluster_indices = range(clusters[0][0], clusters[0][1])
            cluster_readings = [observations[i] for i in cluster_indices]
            distance = sum(cluster_readings) / len(cluster_readings)
            angle = (sum(angles[i] for i in cluster_indices) /
                     len(cluster_readings))
            return BottleLocationBelief(
                    distance=distance, angle=angle)
        else:
            return None

    def delete_loc_files(self):
        """
        Delete all files in ./data
        """
        filenames = os.listdir("./data")
        for f in filenames:
            os.remove(f)

    def save(self):
        """
        Save the signature in a file with a proper name based on the point and STEP
        """
        if self.x == 0 or self.y == 0:
            print "ERROR in SingatureManager.save() - point is not set"
            return

        filename = "data/%d.%d.%d.dat" % (self.x, self.y, int(STEP))
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')
        for i in self.sig:
            f.write(str(i) + "\n")
        f.close();

    def read(self, x, y):
        """
        Read a LocationSignature from file based on the location of the point
        If such file does not exists, an empty LocationSignature is returned
        """
        self.x = x
        self.y = y

        filename = ""
        filenames = os.listdir("./data")
        for f in filenames:
            args = f.split(".")
            if x == int(args[0]) and y == int(args[1]):
                filename = f
        if filename == "":
            print "ERROR in SignatureManager.read() - no file with coordinates %d %d %d" % x, y, STEP

        f = open("./data/" + filename, 'r')
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


def get_bottle_angle(ls1, ls2):
    """
        NOTE: orienation at which the signatures were taken matters
    """
    max_diff = 0
    max_i = 0
    #diff = 0

    for i, val in enumerate(ls1.sig):
        diff = (ls1.sig[i] - ls2.sig[i])**2
        if diff > max_diff:
            max_i = i
            max_diff = diff

    return max_i*STEP

rot_sensor = RotatingSensor()

def main():
    #rot_sensor.setOrientation(FACE_FORWARD)
    #rot_sensor.setOrientation(FACE_BACK)
    #rot_sensor.setOrientation(FACE_RIGHT)
    #rot_sensor.setOrientation(FACE_LEFT)
    #rot_sensor.setOrientation(FACE_FORWARD)

    #ls = rot_sensor.takeSignature(30.0, 150.0)
    #ls.x , ls.y = 3, 3
    #ls.save()
    
    ls = LocationSignature()
    ls.read(1,1)

    ls_bottle = LocationSignature()
    ls_bottle.read(2,2)
    
    print get_bottle_angle(ls_bottle, ls)


if __name__ == "__main__":
    main()
