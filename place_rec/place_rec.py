#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import math
import os
import sys

sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import ultrasound


class LocationSignature:
    """
        Store a signature characterizing a location
    """
    def __init__(self, no_bins = 360):
        self.sig = [0] * no_bins
        
    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]


class SignatureContainer():
    """
        Manage files that contain location signatures
    """
    def __init__(self, size = 5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
        
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number. 
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;
 
    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)
            
        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
            f.close();
        else:
            print "WARNING: Signature does not exist."
        
        return ls
        

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


    def takeSignature(self, start_angle, end_angle, step=1):
        """
            Take a signature and return LocationSignature()
            @param start_angle: orientation angle relative to the robot orienation to start taking sonar measurements from
            @param end_angle:   orientation angle relative to the robot orienation to end taking sonar measurements
            @param step:        steps at which to take sonar measurements
        """

        angle_readings = range(start_angle, end_angle, step)
        ls = LocationSignature(len(angle_readings))
 
        for i, angle in enumerate(angle_readings):
            self.setOrientation(angle)
            ls[i] = ultrasound.get_reading()

        return ls

    def setOrientation(self, orientation):
        if orientation < -math.pi:
            orientation = -math.pi
        elif orientation > math.pi:
            orientation = math.pi
        ultrasound.rotate_sensor(-(orientation - self.orientation))
        self.orientation = orientation


"""
# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
    print "TODO:    You should implement the function that captures a signature."
    for i in range(len(ls.sig)):
        ls.sig[i] = random.randint(0, 255)
"""

# FILL IN: compare two signatures
def compare_signatures(ls1, ls2):
    dist = 0
    print "TODO:    You should implement the function that compares two signatures."
    return dist

def learn_location(start_angle, end_angle, step=1):
    """
        This function characterizes the current location, and stores the obtained 
        signature into the next available file.
    """

    ls = LocationSignature()
    rot_sensor.takeSignature(start_angle, end_angle, step)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return
    
    signatures.save(ls,idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location():
    ls_obs = LocationSignature();
    characterize_location(ls_obs);

    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    for idx in range(signatures.size):
        print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
        ls_read = signatures.read(idx);
        dist    = compare_signatures(ls_obs, ls_read)

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files(). 
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.



signatures = SignatureContainer(5)
rot_sensor = RotatingSensor()

#signatures.delete_loc_files()


FACE_FORWARD = math.pi / 2
FACE_LEFT = math.pi
FACE_RIGHT = 0.0
FACE_BACK = -math.pi / 2


def main():
    rot_sensor.setOrientation(FACE_FORWARD)
    rot_sensor.setOrientation(FACE_BACK)
    rot_sensor.setOrientation(FACE_RIGHT)
    rot_sensor.setOrientation(FACE_LEFT)
    rot_sensor.setOrientation(FACE_FORWARD)
    # learn_location();
    # recognize_location();


if __name__ == "__main__":
    main()
