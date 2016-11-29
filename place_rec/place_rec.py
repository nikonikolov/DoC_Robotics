#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import bisect
import random
import math
import os
import sys
import collections
import getpass

import numpy as np

sys.path.append('/home/pi/DoC_Robotics')
sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')
sys.path.append('/home/pi/DoC_Robotics/touch_sensors')
sys.path.append('/home/pi/DoC_Robotics/MCL')
sys.path.append('/home/pi/DoC_Robotics/pmotion')


if getpass.getuser() == "pi":
    import motor_params
    import ultrasound
    import touch_sensors
    import walls
    import motion_predict
else:
    import matplotlib.pyplot as plt

# NOTE: if you change this, reading a signature from file might read a wrong signature; Comparing signatures will also fail; Solution - delete all current signatures
STEP = 5

FACE_FORWARD = math.pi / 2
FACE_LEFT = math.pi
FACE_RIGHT = 0.0
FACE_BACK = -math.pi / 2

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
NORMAL_DIR = SCRIPT_DIR + "/data/normal/"
BOTTLE_DIR = SCRIPT_DIR + "/data/bottles/"

# NOTE: thete is in radians while rstart and rend are in degrees; theta must be in the range -180 to 180
SignaturePoint = collections.namedtuple(
        "SignaturePoint", ["x", "y", "theta", "rstart", "rend"])

SIGNATURE_POINTS = [
    SignaturePoint(x=40, y=128, theta=0, rstart=30, rend=150),
    # SignaturePoint(x=170, y=40, theta=0, rstart=30, rend=150),
    # SignaturePoint(x=140, y=40, theta=0, rstart=30, rend=150),
]
# Angle is in degrees, distance is in cm.
BottleLocation = collections.namedtuple(
        "BottleLocation", ["angle", "distance"])


def remove_cluster_anomalies(clusters):
    if len(clusters) == 0:
        return clusters
    threshold = math.floor(0.7 * max(c[1] - c[0] for c in clusters))
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


def threshold_differences(test_values, observations):
    threshold = 200.0
    return [1 if ((observed - expected) ** 2) > 200.0 else 0
            for observed, expected
            in zip(observations, test_values)]


def weighted_average_bottle_belief(bottle_vals, observations, angles):
    """
    Arguments:
        bottle_vals - truncated array of reading where the bottle is supposed to be
        observations - truncated array of reading of the place without a bottle there
        angles - truncated array of the corresponding angles for the above readings
    """
    total_error = sum( abs(b-o) for b, o in zip(bottle_vals, observations) )

    angle = sum( float(abs(b-o))/total_error * a for b, o, a in zip(bottle_vals, observations, angles) )
    distance = sum( float(abs(b-o))/total_error * b for b, o in zip(bottle_vals, observations) ) + 5

    i = bisect.bisect_right(angles, angle)
    d1 = observations[i]
    d2 = observations[i+1]
    a1 = angles[i]
    a2 = angles[i+1]
    distance = (d2 - d1) / (a2 - a1) * (angle - a1) + d1

    return BottleLocation(distance=distance, angle=angle - 90.0)

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

    # Get array of the same size of the as the signatures that contains zeros and ones based on threshold
    thresholded = threshold_differences(test_signature.sig,
                                        observations)
    print "Thresholded:"
    print thresholded
    print "Observations:"
    print observations
    print "Expected:"
    print test_signature.sig
    print "Angles"
    print angles

    # Get a list of ranges speficying the stard and end indices of the biggest clusters 
    clusters = remove_cluster_anomalies(binary_signal_partition_by(thresholded))
    if len(clusters) == 1:
        cluster_indices = range(clusters[0][0], clusters[0][1])
        
        normal_clustered = [test_signature.sig[i] for i in cluster_indices]
        bottle_clustered = [observations[i] for i in cluster_indices]
        angles_clustered = [angles[i] for i in cluster_indices]

        distance = np.median(bottle_clustered) + 10.0
        angle = np.median(angles_clustered)
        
        # Using weighted bottle belief
        return weighted_average_bottle_belief(bottle_clustered, normal_clustered, angles_clustered)
        
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


    def takeSignature(self, start_angle, end_angle, sig_point):
        """
            Take a signature and return LocationSignature()
            @param start_angle: orientation angle relative to the robot orienation to start taking sonar measurements from - in degrees
            @param end_angle:   orientation angle relative to the robot orienation to end taking sonar measurements - in degrees
            @param sig_point:   point at which the reading is being taken 
        """

        ls = LocationSignature()
        if start_angle > end_angle:
            step = -STEP
        else:
            step = STEP

        for angle in range(int(start_angle), int(end_angle), step):
            self.setOrientation(float(angle) * math.pi / 180)
            reading = ultrasound.get_reading()
            if reading > ultrasound.MAX_DIST:
                reading = ultrasound.GARBAGE
  
            # Get the absolute orientation at which the measurement is being taken
            theta = sig_point.theta + math.radians(angle - 90)
            if theta > math.pi:
                theta -= 2 * math.pi
            elif theta < -math.pi:
                theta += 2 * math.pi

            # Get the reading that is supposed to be read at that position
            particle = motion_predict.Particle(x=sig_point.x, y=sig_point.y, theta=theta)
            expected_dist = walls.getWallDist(particle)

            # if the expected reading is not garbage and the actual reading is garbage, substitute the actual reading with the simulated one
            # when another signature is taken at the same point, the reading will either fail and be substituted again or it will succeed
            # if successful and no bottle, error will be too small to affect the algorithm; if bottle then the proper difference in signatures will be noted    
            if expected_dist != ultrasound.GARBAGE and reading == ultrasound.GARBAGE:
                reading = expected_dist

            # note - if reading is not garbage but it is supposed to be, we should save the reading as it is: we either have a bottle or made a successful reading anyway

            ls.sig.append(reading)

        return ls

    def setOrientation(self, orientation):
        # We need to orientation to be in robot terms
        orientation = math.pi * 29.0 / 180.0 - orientation
        
        if orientation < -math.pi:
            orientation = -math.pi
        elif orientation > math.pi:
            orientation = math.pi

        myOrientation = motor_params.interface.getMotorAngle(
              ultrasound.SONAR_MOTOR_PORT)[0]
        # orientation now between 0 & 2pi
        myOrientation = myOrientation % (math.pi * 2)
        if (myOrientation > math.pi):
            myOrientation -= math.pi*2
        print "orientation =", orientation / math.pi * 180.0
        print "myOrientation =", myOrientation / math.pi * 180.0
        ultrasound.rotate_sensor(orientation - myOrientation)


def bump_termination_callback():
    left = motor_params.interface.getSensorValue(
            touch_sensors.TOUCH_PORT_LEFT)[0]
    right = motor_params.interface.getSensorValue(
            touch_sensors.TOUCH_PORT_RIGHT)[0]
    if left or right:
        return True


def test_production():
    for sig_point in SIGNATURE_POINTS:

        ls_normal = LocationSignature()
        ls_normal.read(sig_point, NORMAL_DIR)

        raw_input("Place a bottle somewhere and press enter")    

        ls_bottle = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend, sig_point)
        ls_bottle.save(sig_point, BOTTLE_DIR)
    
        bottle_loc = get_bottle_belief(ls_bottle, ls_normal, sig_point)

        if bottle_loc is not None:
            print bottle_loc
            motor_params.rotate(bottle_loc.angle)
            motor_params.interface.setMotorRotationSpeedReferences(
                    motor_params.motors, [8.0, 8.0])
            left = 0
            right = 0

            motor_params.slow_down_forward(
                    bottle_loc.distance, bump_termination_callback)
        else:
            print "Bottle loc is None!"

        raw_input("Place the robot in a the next signature point for a new test and press enter")    

def test_performance():
    for sig_point in SIGNATURE_POINTS:

        ls_normal = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend, sig_point)
        ls_normal.save(sig_point, NORMAL_DIR)

        raw_input("Place a bottle somewhere and press enter")    

        ls_bottle = rot_sensor.takeSignature(sig_point.rstart, sig_point.rend, sig_point)
        ls_bottle.save(sig_point, BOTTLE_DIR)
    
        bottle_loc = get_bottle_belief(ls_normal, ls_bottle, sig_point)

        print bottle_loc

        motor_params.rotate(bottle_loc.angle)
        motor_params.forward(bottle_loc.distance)


        raw_input("Place the robot in a the next signature point for a new test and press enter")    


def get_correlation_diff(test_sig, observed_sig):
    return [(a - b) ** 2 for a, b in
            zip(test_sig.sig, observed_sig.sig)]


def show_plots():
    for sig_point in SIGNATURE_POINTS:

        observed_sig = LocationSignature()
        observed_sig.read(sig_point, NORMAL_DIR)

        test_sig = LocationSignature()
        test_sig.read(sig_point, BOTTLE_DIR)

        error = get_correlation_diff(test_sig, observed_sig)
        thresholded = threshold_differences(
                test_sig.sig, observed_sig.sig)

        plt.figure()
        plt.title("Observed Signature")
        plt.ylim(0, 270)
        plt.plot(observed_sig.sig)

        plt.figure()
        plt.title("Test Signature")
        plt.ylim(0, 270)
        plt.plot(test_sig.sig)

        plt.figure()
        plt.title("Correlation Error")
        plt.plot(error)

        plt.figure()
        plt.ylim(-0.25, 1.25)
        plt.title("Thresholded")
        plt.plot(thresholded)

        plt.show()

rot_sensor = RotatingSensor()

def main():
    if getpass.getuser() == "pi":
        test_production()
    else:
        show_plots()

if __name__ == "__main__":
    main()
