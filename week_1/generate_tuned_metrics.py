import rocommon
import time

LOG_PATH = '/home/pi/Documents/log/'
ANGLE = 30.0
TOL = 0.05


if __name__ == '__main__':
    interface, motors = rocommon.setup()

    interface.startLogging(LOG_PATH + 'tuned_data')
    interface.increaseMotorAngleReferences(motors, [ANGLE, ANGLE])

    while not interface.motorAngleReferencesReached(motors):
        pass

    # collect more data after reaching reference angle
    time.sleep(5.0)

    interface.stopLogging()
    interface.terminate()
