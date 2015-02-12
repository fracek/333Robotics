import sys
sys.path.append('../lib')
import rocommon

SIGMA = 0.3
STEP_DISTANCE = 10
WEB = True

def print_position(robot):
    if WEB:
        robot.draw_particles()
    else:
        print('{}'.format(robot.ps.x))

if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot(sigma=SIGMA)

    try:
        for _ in xrange(0, 4):
            for _ in xrange(0, 4):
                robot.move_forward(STEP_DISTANCE)
                print_position(robot)
            robot.left_90()
            print_position(robot)
    except KeyboardInterrupt:
        robot.implode()
