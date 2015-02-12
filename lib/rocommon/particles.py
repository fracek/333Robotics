import numpy as np
from robot import Robot


class ParticleSet:

    def __init__(self, particles_number, e_sigma, f_sigma, g_sigma):
        self.particles_number = particles_number
        self.mu = 0.0
        self.e_sigma = e_sigma
        self.f_sigma = f_sigma
        self.g_sigma = g_sigma
        # [x, y, theta]
        self.x = np.zeros([particles_number, 3])
        self.w = np.ones(particles_number) / particles_number

    def _normal(self, sigma):
        return np.random.normal(self.mu, sigma, self.particles_number)

    def predict_move(self, distance):
        e = self._normal(self.e_sigma)
        f = self._normal(self.f_sigma)
        # x
        self.x[:, 0] += (distance + e) * np.cos(self.x[:, 2])
        # y
        self.x[:, 1] += (distance + e) * np.sin(self.x[:, 2])
        # theta
        self.x[:, 2] += f

        return self.x

    def predict_turn(self, alpha):
        g = self._normal(self.g_sigma)
        self.x[:, 2] += alpha + g

        return self.x


class ProbabilisticRobot(Robot):

    NUMBER_OF_PARTICLES = 100

    def __init__(self, e_sigma=0.5, f_sigma=0.1, g_sigma=0.5, use_spinning_sonar=False):
        Robot.__init__(self, use_spinning_sonar)
        self.ps = ParticleSet(ProbabilisticRobot.NUMBER_OF_PARTICLES, e_sigma, f_sigma, g_sigma)

    def move_forward(self, distance):
        Robot.move_forward(self, distance)
        self.ps.predict_move(distance)

    def turn(self, angle):
        Robot.turn(self, angle)
        self.ps.predict_turn(angle)

    def position_estimate(self):
        mean_x = np.sum(self.ps.x.T * self.ps.w, axis=1)
        return mean_x

    def move_to_waypoint(self, wp):
        mean_x = self.position_estimate()
        d = wp - mean_x[:2]
        abs_angle = np.arctan2(d[1], d[0])
        angle = abs_angle - mean_x[2]
        if abs(angle) > np.pi:
            angle -= np.sign(angle) * 2.0 * np.pi
        self.turn(angle)
        distance = np.sqrt(np.sum(d ** 2))
        self.move_forward(distance)

    def draw_particles(self):
        particles = 2.0 * self.ps.x + [500.0, 250.0, 0.0]
        particles_list = [(r[0], r[1], r[2]) for r in particles]
        print('drawParticles: {}'.format(particles_list))
