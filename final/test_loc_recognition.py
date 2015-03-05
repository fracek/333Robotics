import sys
sys.path.append('../lib')
import rocommon

if __name__ == "__main__":
    try:
        robot = rocommon.FinalRobot()
        robot.load_all_locations()
        loc = robot.guess_location()
        print('loc = {}'.format(loc))
    except KeyboardInterrupt:
        pass
    robot.implode()
