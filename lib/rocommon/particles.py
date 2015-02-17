import numpy as np


class ParticleSet:

    def __init__(self, starting_x, particles_number, e_sigma, f_sigma, g_sigma):
        self.particles_number = particles_number
        self.mu = 0.0
        self.e_sigma = e_sigma
        self.f_sigma = f_sigma
        self.g_sigma = g_sigma
        # [x, y, theta]
        self.x = np.zeros([particles_number, 3])
        self.x[0, :] = starting_x
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
