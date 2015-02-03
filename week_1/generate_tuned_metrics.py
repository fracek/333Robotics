import rocommon
import time

LOG_PATH = '/home/pi/Documents/log/'
ANGLE = 30.0


if __name__ == '__main__':
    robot = rocommon.Robot()

    robot.StartLogging(LOG_PATH + 'tuned_data')

    robot._move_by_angle(ANGLE)

    # collect more data after reaching reference angle
    time.sleep(5.0)

    robot.StopLogging()
    robot.Implode()
