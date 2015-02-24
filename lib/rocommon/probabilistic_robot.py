import numpy as np
from robot import Robot
from particles import ParticleSet
from canvas import Canvas
import likelihood as lh


class ProbabilisticRobot(Robot):

    NUMBER_OF_PARTICLES = 100
    ANGLE_THRESHOLD = np.radians(2.0)
    SONAR_READINGS_THRESHOLD = 30

    def __init__(self, e_sigma=0.03, f_sigma=0.01, g_sigma=0.03,
                 use_spinning_sonar=False, map=None, starting_x=[0, 0, 0]):
        Robot.__init__(self, use_spinning_sonar)
        self.ps = ParticleSet(
            starting_x, ProbabilisticRobot.NUMBER_OF_PARTICLES,
            e_sigma, f_sigma, g_sigma)
        self.map = map

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
        # Avoid updating particle when not turning
        if abs(angle) > ProbabilisticRobot.ANGLE_THRESHOLD:
            self.turn(angle)
        distance = np.sqrt(np.sum(d ** 2))
        self.move_forward(distance)

    def update_measurement(self):
        sonar_value = self.sonar.value()
        if sonar_value:
            distances = np.array([lh.compute_expected_depth(x, self.map.walls)
                                  for x in self.ps.x])
            bad_distances = np.isinf(distances)
            if np.sum(bad_distances) < ProbabilisticRobot.SONAR_READINGS_THRESHOLD:
                likelihoods = [lh.compute_likelihood(d, sonar_value)
                               for d in distances]
                self.ps.w *= likelihoods
                self.ps.normalize()
                self.ps.resample()

    def draw_particles(self):
        canvas = Canvas()
        canvas.draw_particles(self.ps.x, self.ps.w)
