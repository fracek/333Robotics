import numpy as np
import time
from probabilistic_robot import ProbabilisticRobot
from particles import ParticleSet
from canvas import Canvas


class FinalRobot(ProbabilisticRobot):

    def __init__(self, num_bins=36, sig_location='signatures', map=None, num_sig=3):
        ProbabilisticRobot.__init__(self, use_spinning_sonar=True,
                                    starting_x=[0, 0, 0], map=map)
        self.num_bins = num_bins
        self.num_sig = num_sig
        self.sig_location = sig_location
        self.signatures = np.zeros((num_sig, num_bins))

    def location_sig(self):
        sig = np.zeros(self.num_bins)
        for i in range(self.num_bins):
            self.sonar.rotate_by(2.0 * np.pi / float(self.num_bins))
            sonar_value = self.sonar.value()
            sig[i] = sonar_value
        self.sonar.rotate_by(-2.0 * np.pi)
        return sig

    def register_location(self, idx):
        sig = self.location_sig()
        np.save(self._location_path(idx), sig)

    def load_location(self, idx):
        sig = np.load(self._location_path(idx))
        self.signatures[idx, :] = sig

    def load_all_locations(self):
        for i in range(0, self.num_sig):
            self.load_location(i)

    def _location_path(self, idx):
        return '{}/loc_{}.npy'.format(self.sig_location, idx)

    def guess_location(self):
        sig = self.location_sig()
        min_idx = None
        min_err = np.inf
        for shift in range(0, self.num_bins):
            errors = np.sum((self.signatures - np.roll(sig, shift))**2, axis=1)
            if np.min(errors) < min_err:
                min_idx = np.argmin(errors)
                min_err = np.min(errors)
        return min_idx
