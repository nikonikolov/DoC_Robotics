import collections
import math
import random
import sys

sys.path.append('/home/pi/DoC_Robotics')
import motor_params

NUMBER_OF_PARTICLES = 100


def rotation_noise(p, alpha):
    angle = p + alpha + random.gauss(0, 1.0) * math.pi / 180.0
    #angle = p + alpha + random.gauss(0, 2.0) * math.pi / 180.0
    if angle > math.pi:
        angle -= 2 * math.pi
    elif angle < -math.pi:
        angle += 2 * math.pi
    return angle    
    

StateBase = collections.namedtuple("StateBase", ["particles", "weights"])


class State(StateBase):
    """State of the position of the robot at a point of time."""
    @property
    def x(self):
        return sum(p.x * w for p, w in zip(self.particles, self.weights))

    @property
    def y(self):
        return sum(p.y * w for p, w in zip(self.particles, self.weights))

    @property
    def theta(self):
        x = y = 0.
        for p, w in zip(self.particles, self.weights):
            x += math.cos(p.theta) * w
            y += math.sin(p.theta) * w

        return math.atan2(y, x)

    def rotate(self, alpha):
        return State(particles=[Particle(x=p.x, y=p.y, theta=rotation_noise(p.theta, alpha)) for p in self.particles],
                     weights=self.weights)

    def draw_particles(self):
        DISTANCE_TO_PIXEL = 10.0
        print "drawParticles:" + str([(100 + p.x * DISTANCE_TO_PIXEL,
                                       100 + p.y * DISTANCE_TO_PIXEL,
                                       p.theta)
                                      for p in self.particles])

    def move_forward(self, d):
        particles = []
        for particle in self.particles:
            x, y, theta = particle
            e = random.gauss(0, 1)
            f = random.gauss(0, 0.25 * math.pi / 180.0)
            particles.append(Particle(
                    x + (d + e) * math.cos(theta),
                    y + (d + e) * math.sin(theta),
                    theta + f))
        return State(particles=particles, weights=self.weights)

    @property
    def position(self):
        x_total =0
        y_total =0
        theta_total =0
        for p in self.particles:
            x_total += p.x
            y_total += p.y
            if p.theta < 0:
                theta_total += (2*math.pi - p.theta)
            else:
                theta_total += p.theta
    
        theta_average = theta_total/NUMBER_OF_PARTICLES
        if theta_average > math.pi:
            theta_average %= 2*math.pi
            theta_average -= 2*math.pi

        return Particle(x=x_total/NUMBER_OF_PARTICLES, y=y_total/NUMBER_OF_PARTICLES, theta=theta_average)


Particle = collections.namedtuple("Particle", ["x", "y", "theta"])
Dest = collections.namedtuple("Dest", ["x", "y"])


def navigateToWaypoint(state, dest):
    goal_theta = math.atan2(dest.y - state.y, dest.x - state.x)
    delta_theta_rad = goal_theta - state.theta
    if delta_theta_rad > math.pi:
        delta_theta_rad -= 2*math.pi
    elif delta_theta_rad < -math.pi:
        delta_theta_rad += 2*math.pi  
    motor_params.rotate(delta_theta_rad / math.pi * 180.0)
    state = state.rotate(delta_theta_rad)
    dist = min(20.0, math.sqrt((state.y - dest.y)**2 + (state.x - dest.x)**2))
    motor_params.forward(dist)
    return state.move_forward(dist)


def main():
    state = State(particles=[Particle(x=0, y=0, theta=0)] * NUMBER_OF_PARTICLES,
                  weights=[1.0 / NUMBER_OF_PARTICLES
                           for _ in range(NUMBER_OF_PARTICLES)])
    
    while True:
        args = raw_input("Enter a destination waypoint: ")
        x, y = args.strip().split()
        dest = Dest(x=float(x), y=float(y))
        state = navigateToWaypoint(state, dest)
        print (state.x, state.y, state.theta)


if __name__ == "__main__":
    main()
