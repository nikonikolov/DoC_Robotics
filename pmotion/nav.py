import collections
import math
import random

import motor_params

NUMBER_OF_PARTICLES = 100


def rotation_noise(p, alpha):
    #return p + alpha + random.gauss(0, 2.0) * math.pi / 180.0
    
    angle = p + alpha + random.gauss(0, 2.0) * math.pi / 180.0
    if angle > 180:
        angle -= 360
    elif angle < -180:
        angle += 360
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
        return sum(p.theta * w for p, w in zip(self.particles, self.weights))

    def rotate(self, alpha):
        return State(
                particles=[Particle(
                        x=p.x, y=p.y,
                        theta=rotation_noise(p.theta, alpha))
                                for p in self.particles],
                weights=self.weights)

    def move_forward(self, d):
        particles = []
        for particle in self.particles:
            x, y, theta = particle
            e = random.gauss(0, 0.07)
            f = random.gauss(0, 0.25 * math.pi / 180.0)
            particles.append(Particle(
                    x + (d + e) * math.cos(theta),
                    y + (d + e) * math.sin(theta),
                    theta + f))
        return State(particles=particles, weights=self.weights)


Particle = collections.namedtuple("Particle", ["x", "y", "theta"])
Dest = collections.namedtuple("Dest", ["x", "y"])


def navigateToWaypoint(state, dest):
    goal_theta = math.atan2(dest.y - state.y, dest.x - state.x)
    delta_theta_rad = goal_theta - state.theta
    #if delta_theta_rad > math.pi:
    #    delta_theta_rad = 2*math.pi - delta_theta_rad
    if delta_theta_rad > math.pi:
        delta_theta_rad = delta_theta_rad - 2*math.pi
    elif delta_theta_rad < -math.pi:
        delta_theta_rad += 2*math.pi  
    motor_params.rotate(delta_theta_rad / math.pi * 180.0)
    state = state.rotate(delta_theta_rad)
    dist = math.sqrt((state.y - dest.y)**2 + (state.x - dest.x)**2)
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
