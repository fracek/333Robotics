import numpy as np
from robot import Robot
from math import atan2


class ParticleSet:

    def __init__(self, particles_number, sigma):
        self.particles_number = particles_number
        self.mu = 0.0
        self.sigma = sigma
        # [x, y, theta]
        self.x = np.zeros([particles_number, 3])
        self.w = np.ones(particles_number) / particles_number

    def _normal(self):
        return np.random.normal(self.mu, self.sigma, self.particles_number)

    def predict_move(self, distance):
        e = self._normal()
        f = self._normal()
        # x
        self.x[:, 0] += (distance + e) * np.cos(self.x[:, 2])
        # y
        self.x[:, 1] += (distance + e) * np.sin(self.x[:, 2])
        # theta
        self.x[:, 2] += f

        return self.x

    def predict_turn(self, alpha):
        g = self._normal()
        self.x[:, 2] += alpha + g

        return self.x


class ProbabilisticRobot(Robot):

    NUMBER_OF_PARTICLES = 100

    def __init__(self, sigma=0.3, use_spinning_sonar=False):
        Robot.__init__(self, use_spinning_sonar)
        self.ps = ParticleSet(ProbabilisticRobot.NUMBER_OF_PARTICLES, sigma)

    def move_forward(self, distance):
        Robot.move_forward(self, distance)
        self.ps.predict_move(distance)

    def turn(self, angle):
        Robot.turn(self, angle)
        self.ps.predict_turn(angle)

    def move_to_waypoint(self, wp):
        mean_x = np.sum(self.ps.x.T * self.ps.w, axis=1)
        d = wp - mean_x[:2]
        abs_angle = atan2(d[1], d[0])
        angle = np.degrees(abs_angle) - mean_x[2]
        self.turn(angle)
        distance = np.sqrt(np.sum(d**2))
        self.move_forward(distance)

    def draw_particles(self):
        particles = 2.0 * self.ps.x + [500.0, 250.0, 0.0]
        particles_list = [(r[0], r[1], r[2]) for r in particles]
        print('drawParticles: {}'.format(particles_list))
