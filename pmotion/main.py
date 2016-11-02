import random

STANDARD_DEVIATION = 1.0
particles = [(0, 0, 0) for _ in range(100)]  # type: Tuple[int, int, int]


def update_particles_straight(d):
    for i in range(len(particles)):
        x, y, theta = particles[i]
        e = random.gauss(0, 1.0)
        f = random.gauss(0, 1.0)
        particles[i] = (x + (d + e) * np.cos(theta),
                        y + (d + e) * np.sin(theta),
                        theta + f)


def update_particles_rotation(alpha):
    for i in range(len(particles)):
        g = random.gauss(0, 1.0)
        x, y, theta = particles[i]
        particles[i] = (x, y, theta + alpha + g)
