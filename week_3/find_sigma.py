import sys
sys.path.append('../lib')
import rocommon
from math import pi

STEP_DISTANCE = 20
E_SIGMA = 0.5
F_SIGMA = 0.1
G_SIGMA = 0.5

if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot(e_sigma=E_SIGMA, f_sigma=F_SIGMA, g_sigma=G_SIGMA)

    try:
        if False:
            for dist in xrange(0, 200 / STEP_DISTANCE):
                robot.move_forward(STEP_DISTANCE)
                print('{} =  {}'.format(dist, robot.position_estimate()))
                sys.stdin.readline()
        else:
            for angle in xrange(0, 10):
                robot.turn(2 * pi / 10.0)
                print('{} =  {}'.format(dist, robot.position_estimate()))
    except KeyboardInterrupt:
        pass
    robot.implode()
