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



class LocationSignature:
    """
        Store a signature characterizing a location
    """
    def __init__(self, x=0, y=0):
        self.sig = []                   # signature data
        self.x = x                      # x argument of the point the signature is created for
        self.y = y                      # y argument of the point the signature is created for

    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

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
        
        f = open(filename, 'r')
        for line in f:
            self.sig.append(int(line))
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

    for i, val in enumerate(ls1):
        diff += (ls1[i] - ls2[i])**2
        if diff > max_diff:
            max_i = i
            max_diff = diff

    return i*STEP

rot_sensor = RotatingSensor()

def main():
    #rot_sensor.setOrientation(FACE_FORWARD)
    #rot_sensor.setOrientation(FACE_BACK)
    #rot_sensor.setOrientation(FACE_RIGHT)
    #rot_sensor.setOrientation(FACE_LEFT)
    #rot_sensor.setOrientation(FACE_FORWARD)

    ls = rot_sensor.takeSignature(45, 135)
    ls.x , ls.y = 1, 1
    ls.save()




if __name__ == "__main__":
    main()
