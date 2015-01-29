import brickpi
import time
import rocommon

LOG_PATH = '/home/pi/Documents/log/'
ANGLE = 30.0
TOL = 0.05


if __name__ == '__main__':
    interface, motors = rocommon.setup()

    k_p = rocommon.K_u[0]
    print('Set k_p_final to {}'.format(k_p))
    interface.startLogging(LOG_PATH + 'k_p_final_{}'.format(int(k_p * 100)))
    print('k_p_final = {}: START'.format(k_p))
    interface.increaseMotorAngleReferences(motors, [ANGLE, ANGLE])

    try:
        while True:
            pass

    except KeyboardInterrupt:
        pass

    interface.stopLogging()
    print('k_p_final = {}: STOP'.format(k_p))
    time.sleep(3.0)
    interface.terminate()

