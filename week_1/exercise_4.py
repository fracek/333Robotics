import sys
sys.path.append('../lib')
import rocommon


if __name__ == '__main__':

    robot = rocommon.Robot()

    for _ in xrange(0, 4):
        robot.move_forward(40)
        robot.Left90deg()

    robot.implode()
