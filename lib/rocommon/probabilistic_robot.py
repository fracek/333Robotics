import numpy as np
from robot import Robot
from particles import ParticleSet
from canvas import Canvas


class ProbabilisticRobot(Robot):

    NUMBER_OF_PARTICLES = 100
    ANGLE_THRESHOLD = np.radians(2.0)

    def __init__(self, e_sigma=0.03, f_sigma=0.01, g_sigma=0.03, use_spinning_sonar=False, map=None, starting_x=[0, 0, 0]):
        Robot.__init__(self, use_spinning_sonar)
        self.ps = ParticleSet(
            starting_x, ProbabilisticRobot.NUMBER_OF_PARTICLES, e_sigma, f_sigma, g_sigma)
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

    def _compute_expected_depth(self, pos):
        [x, y, theta] = pos
        def compute_distance_from_wall(wall):
            (Ax, Ay, Bx, By) = wall

            # Check angle beta between sonar and the normal to the wall
            num = np.cos(theta)*(Ay - By) + np.sin(theta) * (Bx - Ax)
            den = np.sqrt(np.square(Ay - By) + np.square(Bx - Ax))
            beta = np.arccos(num / den)
            if np.abs(beta) > np.pi/4.0:
                return np.inf

            # Compute distanec between sonar and wall
            num = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
            den = (By - Ay) * np.cos(theta) - (Bx - Ax) * np.sin(theta)
            m = num / den

            # Check hit point on the wall
            # SEE: http://www.lucidarme.me/?p=1952
            C = np.array([x + m * np.cos(theta), y + m * np.sin(theta)])
            AB = [Bx - Ax, By - Ay]
            AC = C - [Ax, Ay]
            K_ac = np.dot(AB, AC)
            K_ab = np.dot(AB, AB)
            if (0 < K_ac < K_ab) and m >= 0:
                return m

            return np.inf

        distances = [compute_distance_from_wall(w) for w in self.map.walls]
        print('distances = {}'.format(distances))

    def _compute_likelihood(self, x, z):
        m = self._compute_expected_depth(x)
        return m

    def update_measurement(self):
        sonar_value = self.sonar.value()
        if sonar_value and sonar_value is not 255:
            likelihoods = [self._compute_likelihood(x, sonar_value) for x in self.ps.x]

    def draw_particles(self):
        canvas = Canvas()
        canvas.draw_particles(self.ps.x)
