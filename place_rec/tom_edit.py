#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import math
import os
import sys
import time

import motor_params

sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import ultrasound

# NOTE: if you change this, reading a signature from file might read a wrong signature; Comparing signatures will also fail; Solution - delete all current signatures
STEP = 5 

FACE_FORWARD = math.pi / 2
FACE_LEFT = math.pi
FACE_RIGHT = 0.0
FACE_BACK = -math.pi / 2

interface = motor_params.interface

SONAR_MOTOR_PORT = 2

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
	orientation = orientation+1
        while orientation < -math.pi:
            orientation += 2*math.pi
        while orientation > math.pi:
            orientation -= 2*math.pi
        myOrientation = interface.getMotorAngle(SONAR_MOTOR_PORT)[0]
	myOrientation = myOrientation % (math.pi*2) #orientation now between 0 & 2pi
	if (myOrientation > math.pi):
            myOrientation -= math.pi*2
	print myOrientation, orientation
        self.rotate_sensor(orientation - myOrientation)


    def rotate_sensor(self, angle):
        """
            @param: angle - the angle the motor should rotate by - in radians
        """
        interface.increaseMotorAngleReference(SONAR_MOTOR_PORT, angle)
        while not interface.motorAngleReferenceReached(SONAR_MOTOR_PORT):
          time.sleep(0.03)
        print "Ultrasonic rotation reached."

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
