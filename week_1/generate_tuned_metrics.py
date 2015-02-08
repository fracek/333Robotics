import sys
sys.path.append('../lib')
import rocommon
import time

LOG_PATH = '/home/pi/Documents/log/'
ANGLE = 30.0


if __name__ == '__main__':
    robot = rocommon.Robot()

    robot.start_logging(LOG_PATH + 'tuned_data')

    robot._move_by_angle(ANGLE)

    # collect more data after reaching reference angle
    time.sleep(5.0)

    robot.stop_logging()
    robot.implode()
