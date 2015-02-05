import sys
sys.path.append('../lib')
import rocommon

SPEED = 4.0

def avoidance_manouvre(robot, angle):
    robot.MoveBackward(20)
    robot.Turn(angle)


if __name__ == "__main__":
    robot = rocommon.Robot()

    try:
        while True:
            if robot.left_bumper.IsTouching():
                avoidance_manouvre(robot, 90)
            elif robot.right_bumper.IsTouching():
                avoidance_manouvre(robot, -90)
            else:
                robot.SetRotationSpeed(SPEED)
    except KeyboardInterrupt:
        robot.Implode()
