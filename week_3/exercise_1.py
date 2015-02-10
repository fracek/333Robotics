import sys
sys.path.append('../lib')
import rocommon

if __name__ == "__main__":
    robot = rocommon.Robot()

    try:
        robot.move_forward(10)
        robot.move_forward(10)
        robot.move_forward(10)
        robot.move_forward(10)
        robot.turn(-90)
        robot.move_forward(10)
        robot.move_forward(10)
        robot.move_forward(10)
        robot.move_forward(10)
    except KeyboardInterrupt:
        robot.implode()
