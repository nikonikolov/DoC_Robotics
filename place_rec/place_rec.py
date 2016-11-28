#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os

sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import ultrasound

# NOTE: if you change this, reading a signature from file might read a wrong signature; Comparing signatures will also fail; Solution - delete all current signatures
STEP_READING = 2 

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
        if self.x == 0 || self.y == 0:
            print "ERROR in SingatureManager.save() - point is not set"
            return

        filename = "%d.%d.dat" % self.x, self.y, int(STEP) 
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
            if x == int(args[0]) && y == int(args[1]):
                filename = f
        if filename == "":
            print "ERROR in SignatureManager.read() - no file with coordinates %d %d %d" % x, y, STEP
        
        f = open(filename, 'r')
        for line in f:
            self.sig.append(int(line))
        f.close();

        if(!len(self.sig)):
            print "WARNING: SignatureManager.read() - signature does not exist"


class RotatingSensor:
    """
        Save state of the rotating sonar sensor and take LocationSignature readings 
    """
    def __init__(self, orientation=0):
        """
            @param orienatation:
                - 0 means centered
                - range is -PI to PI
                - negative orientation means CCW plane, positive means CW plane
                - value is in radians
        """
        self.orientation = orientation


    def takeSignature(self, start_angle, end_angle):
        """
            Take a signature and return LocationSignature()
            @param start_angle: orientation angle relative to the robot orienation to start taking sonar measurements from - in degrees
            @param end_angle:   orientation angle relative to the robot orienation to end taking sonar measurements - in degrees
        """

        ls = LocationSignature()
 
        for angle in range(int(start_angle), int(end_angle), int(STEP)):
            self.setOrientation(float(angle) * math.pi / 180)
            ls.sig.append(ultrasound.get_reading())

        return ls

    def setOrientation(self, orientation):
        if orientation < -math.pi:
            orientation = -math.pi
        else if orientation > math.pi:
            orientation = math.pi
        ultrasound.rotate_sensor(orientation - self.orientation)
        self.orientation = orientation



# TO DO
def compare_signatures(ls1, ls2):
    """
        NOTE: orienation at which the signatures were taken matters
    """
    dist = 0
    print "TODO:    You should implement the function that compares two signatures."
    return dist

# TO DO
def learn_location(start_angle, end_angle, step=1):
    """
        This function characterizes the current location, and stores the obtained 
        signature into the next available file.
    """

    ls = rot_sensor.takeSignature(start_angle, end_angle, step)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return
    
    signatures.save(ls,idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files(). 
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.

signatures = SignatureContainer(5)
rot_sensor = RotatingSensor()

#signatures.delete_loc_files()

learn_location();
recognize_location();


"""

class SignatureContainer():
        Manage files that contain location signatures
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

# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
    print "TODO:    You should implement the function that captures a signature."
    for i in range(len(ls.sig)):
        ls.sig[i] = random.randint(0, 255)

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
"""
