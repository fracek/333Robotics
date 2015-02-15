import ast
import sys
sys.path.append('../lib')
import rocommon


def parse_input(s):
    try:
        wp = ast.literal_eval(s)
        if type(wp) == list and len(wp) == 2:
            return wp
    except SyntaxError:
        pass
    return None


if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot()

    try:
        while True:
            s = raw_input('Waypoint ([x, y]): ')
            wp = parse_input(s)
            if wp:
                robot.move_to_waypoint(wp)
                print('Current Position: {}'.format(robot.position_estimate()))
            else:
                print('Invalid input {}'.format(s))
    except KeyboardInterrupt:
        robot.implode()
