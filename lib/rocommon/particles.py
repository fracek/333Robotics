import numpy as np


class ParticleSet:

    def __init__(self, starting_x, particles_number, e_sigma, f_sigma, g_sigma):
        self.particles_number = particles_number
        self.mu = 0.0
        self.e_sigma = e_sigma
        self.f_sigma = f_sigma
        self.g_sigma = g_sigma
        # [x, y, theta]
        #self.x = np.zeros([particles_number, 3])
        self.x = np.tile(starting_x, (particles_number, 1))
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

    def normalize(self):
        self.w /= np.sum(self.w)

    def resample(self):
        """
        Implementation of resampling wheel: https://www.udacity.com/course/viewer#!/c-cs373/l-48704330
        """
        index = int(np.random.rand() * self.particles_number)
        beta = 0
        max_weight = max(self.w)
        new_x = np.zeros((self.particles_number, 3))
        for i in xrange(self.particles_number):
            beta += np.random.rand() * 2.0 * max_weight
            while self.w[index] < beta:
                beta -= self.w[index]
                index = (index + 1) % self.particles_number
            new_x[i] = self.x[index]
        self.x = new_x
        self.w = np.ones(len(self.w)) / len(self.w)
