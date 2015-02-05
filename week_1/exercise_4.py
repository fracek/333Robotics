import sys
sys.path.append('../lib')
import rocommon


if __name__ == '__main__':

    robot = rocommon.Robot()

    for _ in xrange(0, 4):
        robot.MoveForward(40)
        robot.Left90deg()

    robot.Implode()
