import sys
sys.path.append('../lib')
import rocommon

if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot()

    try:
        while True:
            wp = input('Waypoint ([x, y]): ')
            robot.move_to_waypoint(wp)
            robot.motors['L']['instance'].angle()
            print('{}'.format(robot.position_estimate()))
    except KeyboardInterrupt:
        robot.implode()
