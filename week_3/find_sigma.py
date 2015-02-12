import sys
sys.path.append('../lib')
import rocommon

SIGMA = 0.3
STEP_DISTANCE = 20

if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot(sigma=SIGMA)

    try:
        for _ in xrange(0, 200 / STEP_DISTANCE):
            robot.move_forward(STEP_DISTANCE)
            print('I AM IN {}'.format(robot.position_estimate()))
            sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    robot.implode()
