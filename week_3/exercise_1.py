import sys
sys.path.append('../lib')
import rocommon

SIGMA = 0.3
STEP_DISTANCE = 10

if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot(sigma=SIGMA)

    try:
        for _ in xrange(0, 4):
            for _ in xrange(0, 4):
                robot.move_forward(STEP_DISTANCE)
                robot.draw_particles()
            robot.turn(-90)
            robot.draw_particles()
    except KeyboardInterrupt:
        robot.implode()
