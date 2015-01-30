import rocommon


if __name__ == '__main__':

    robot = Robot()

    for _ in xrange(0, 4):
        robot.MoveForward(40)
        robot.WaitUntilDone()
        robot.Left90deg()
        robot.WaitUntilDone()

    robot.Implode()
