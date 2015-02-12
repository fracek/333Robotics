import sys
sys.path.append('../lib')
import rocommon

STEP_DISTANCE = 10

if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot()

    try:
        for _ in xrange(0, 4):
            for _ in xrange(0, 4):
                robot.move_forward(STEP_DISTANCE)
                robot.draw_particles()
            robot.left_90()
            robot.draw_particles()
    except KeyboardInterrupt:
        robot.implode()
