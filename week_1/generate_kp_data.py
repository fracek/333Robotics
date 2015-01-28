import brickpi
import time

LOG_PATH = '/home/pi/Documents/log/'
ANGLE = 30.0
TOL = 0.05


def set_k_p(interface, motors, k_p):
    motorParams = interface.MotorAngleControllerParameters()
    motorParams.maxRotationAcceleration = 6.0
    motorParams.maxRotationSpeed = 12.0
    motorParams.feedForwardGain = 255 / 20.0
    motorParams.minPWM = 18.0
    motorParams.pidParameters.minOutput = -255
    motorParams.pidParameters.maxOutput = 255
    motorParams.pidParameters.k_p = k_p
    motorParams.pidParameters.k_i = 0.0
    motorParams.pidParameters.k_d = 0.0

    interface.setMotorAngleControllerParameters(motors[0], motorParams)
    interface.setMotorAngleControllerParameters(motors[1], motorParams)


def motorAngleReferencesReached(interface, motors):
    motorAngles = interface.getMotorAngles(motors)

    a0 = motorAngles[0][0]
    a1 = motorAngles[1][0]

    refs = interface.getMotorAngleReferences(motors)
    diffs = [abs(a0 - refs[0]), abs(a1 - refs[1])]

    errs = [diffs[0], diffs[1]]
    return (errs[0] < TOL * a0) and (errs[1] < TOL * a1)


if __name__ == '__main__':
    interface = brickpi.Interface()
    interface.initialize()

    motors = [0, 1]

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    k_ps = [x * 50.0 for x in range(1, 19)]

    for k_p in k_ps:
        set_k_p(interface, motors, k_p)
        print('Set k_p to {}'.format(k_p))
        interface.startLogging(LOG_PATH + 'k_p_{}'.format(int(k_p * 100)))
        print('k_p = {}: START'.format(k_p))
        interface.increaseMotorAngleReferences(motors, [ANGLE, ANGLE])

        try:
            while True:
                pass

        except KeyboardInterrupt:
            pass

        interface.stopLogging()
        print('k_p = {}: STOP'.format(k_p))
        time.sleep(3.0)
    interface.terminate()
