import sys
sys.path.append('../lib')
import rocommon

if __name__ == "__main__":
    try:
        robot = rocommon.FinalRobot()
        for i in range(0, 3):
            print('[START] loc {}'.format(i))
            robot.register_location(i)
            print('[DONE] loc {}'.format(i))
            raw_input('press any key to continue')
    except KeyboardInterrupt:
        pass
    robot.implode()
