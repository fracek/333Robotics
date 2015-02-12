import sys
sys.path.append('../lib')
import rocommon
from math import pi

SPEED = 6.0


def avoidance_manouvre(robot, angle):
    robot.move_backward(20)
    robot.turn(angle)


if __name__ == "__main__":
    robot = rocommon.Robot()

    try:
        while True:
            if robot.left_bumper.touching():
                avoidance_manouvre(robot, pi/2)
            elif robot.right_bumper.touching():
                avoidance_manouvre(robot, -pi/2)
            else:
                robot.set_rotation_speed(SPEED)
    except KeyboardInterrupt:
        robot.implode()
