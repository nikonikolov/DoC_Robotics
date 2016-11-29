#!/usr/bin/env python 

# Some suitable functions and data structures for drawing a map and particles

import time
import random
import math
import collections
import sys

sys.path.append('/home/pi/DoC_Robotics/ultrasonic_sensors')

import ultrasound

# Configurable Parameters
# Max / Minimum distance, angle that sonar sensor can measure
# Note that angle is relative to the perpendicular rather than the wall.
# and is in radians.
SONAR_MIN_DIST = ultrasound.MIN_DIST
SONAR_MAX_DIST = ultrasound.MAX_DIST
SONAR_MAX_ANGLE = ultrasound.MAX_ANGLE


Point = collections.namedtuple("Point", ["x", "y"])

# Functions to generate some dummy particles data:
def calcX():
    return random.gauss(80,3) + 70*(math.sin(t)); # in cm

def calcY():
    return random.gauss(70,3) + 60*(math.sin(2*t)); # in cm

def calcWeight():
    return random.random();

def calcTheta():
    return random.randint(-180,180);
    return random.randint(0,360);


class Canvas:
    """
    Canvas class for drawing map and particles:
    : takes care of a proper scaling and coordinate transformation between
      the map frame of reference (in cm) and the display (in pixels)
    """
    def __init__(self,map_size=210):
        self.map_size    = map_size;    # in cm;
        self.canvas_size = 768;         # in pixels;
        self.margin      = 0.05*map_size;
        self.scale       = self.canvas_size/(map_size+2*self.margin);

    def drawLine(self,line):
        x1 = self.__screenX(line[0]);
        y1 = self.__screenY(line[1]);
        x2 = self.__screenX(line[2]);
        y2 = self.__screenY(line[3]);
        # print "drawLine:" + str((x1,y1,x2,y2))

    def drawParticles(self,data):
        #display = [(self.__screenX(p.x]), self.__screenY(p.y)) + d[2:] for p, w in data];
        display = [(self.__screenX(d[0]), self.__screenY(d[1])) + d[2:] for d in data];
        # print "drawParticles:" + str(display);

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale


class Map:
    """
    Map class containing the walls of the arena
    """
    def __init__(self, canvas):
        self.walls = [];
        self.canvas = canvas

    def add_wall(self,wall):
        self.walls.append(wall);

    def clear(self):
        self.walls = [];

    def draw(self):
        for wall in self.walls:
            self.canvas.drawLine(wall);


canvas = Canvas()  # global canvas we are going to draw on
wallmap = Map(canvas);
O = Point(0, 0)
A = Point(0, 168)
B = Point(84, 168)
C = Point(84, 126)
D = Point(84, 210)
E = Point(168, 210)
F = Point(168, 84)
G = Point(210, 84)
H = Point(210, 0)
wallmap.add_wall( (O.x, O.y, A.x, A.y) )        # a
wallmap.add_wall( (A.x, A.y, B.x, B.y) )        # b
wallmap.add_wall( (C.x, C.y, D.x, D.y) )        # c
wallmap.add_wall( (D.x, D.y, E.x, E.y) )        # d
wallmap.add_wall( (E.x, E.y, F.x, F.y) )        # e
wallmap.add_wall( (F.x, F.y, G.x, G.y) )        # f
wallmap.add_wall( (G.x, G.y, H.x, H.y) )        # g
wallmap.add_wall( (H.x, H.y, O.x, O.y) )        # h


def getWallDist(particle, wallmap=wallmap,incidence_angle=True):
    """
    param: particle : @type motion_predict.Particle - x, y, theta
    param: wallmap  : @type Map

    Calculate distance from each wall. Then take the shortest wall where the point
    of intersection is within the wall
    Return ultrasound.GARBAGE if the distance is out of the range of the sonar sensor
    """
    smallest_inside_dist = ultrasound.GARBAGE

    for wall in wallmap.walls:
        Ax, Ay, Bx, By = wall
        # print "-- Testing wall: ", wall

        # TODO(fyquah): Handle ZeroDivisionError?
        denom = (By-Ay)*math.cos(particle.theta) - (Bx-Ax)*math.sin(particle.theta)
        # print "denom = ", denom
        if abs(denom) < 0.001:
            continue
        dist = ((By - Ay)*(Ax - particle.x) - (Bx - Ax)*(Ay - particle.y)) / denom
        # print "dist = ", dist
        if dist < SONAR_MIN_DIST or dist > SONAR_MAX_DIST:
            continue
        acos_value = (math.cos(particle.theta) * (Ay - By) + math.sin(particle.theta) * (Bx - Ax)) \
                / (math.sqrt((Ay - By) ** 2 + (Bx - Ax) ** 2))
        # print "acos = ", acos_value
        if acos_value  > 1 or acos_value < -1:
            continue 
        beta = math.acos(acos_value)
        # print "beta = ", beta
        if incidence_angle and beta > SONAR_MAX_ANGLE:
            continue

        meetX = particle.x + dist*math.cos(particle.theta)
        meetY = particle.y + dist*math.sin(particle.theta)
        inside = True
        # Check if x coordinate is inside
        if Ax>Bx:
            Ax, Bx = Bx, Ax
        if meetX < (Ax - 0.01) or meetX > (Bx + 0.01):
            inside = False

        # Check if y coordinate is inside
        if Ay>By:
            Ay, By = By, Ay
        if meetY < (Ay - 0.01) or meetY > (By + 0.01):
            inside = False

        if inside and dist<smallest_inside_dist:
            smallest_inside_dist = dist

    return smallest_inside_dist


class Particles:
    """
    Simple Particles set
    """
    def __init__(self, canvas):
        self.n = 10;
        self.data = [];
        self.canvas = canvas

    def update(self):
        self.data = [(calcX(), calcY(), calcTheta(), calcWeight()) for i in range(self.n)];
    
    def draw(self):
        self.canvas.drawParticles(self.data);


def main():
    global t
    wallmap.draw()

    particles = Particles(canvas);
    while True:
        particles.update();
        particles.draw();
        t += 0.05;
        time.sleep(0.05);


if __name__ == "__main__":
    t = 0
    main()

