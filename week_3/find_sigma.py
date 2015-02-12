import sys
sys.path.append('../lib')
import rocommon

STEP_DISTANCE = 20
F_SIGMA = 0.01

if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot(e_sigma=0.5, f_sigma=F_SIGMA)

    try:
        for dist in xrange(0, 200 / STEP_DISTANCE):
            robot.move_forward(STEP_DISTANCE)
            print('{} =  {}'.format(dist, robot.position_estimate()))
            sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    robot.implode()
