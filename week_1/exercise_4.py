import brickpi

TAU_TO_ANGLE = 18.0
METER_TO_ANGLE = 3.14 / 10.0

K_u = 750.0
P_u = 0.5

K_p = 0.6 * K_u
K_i = 2.0 * K_p / P_u
K_d = K_p * P_u / 8.0


def setup():
    interface = brickpi.Interface()
    interface.initialize()

    motors = [0, 1]

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    motorParams = interface.MotorAngleControllerParameters()
    motorParams.maxRotationAcceleration = 6.0
    motorParams.maxRotationSpeed = 12.0
    motorParams.feedForwardGain = 255 / 20.0
    motorParams.minPWM = 18.0
    motorParams.pidParameters.minOutput = -255
    motorParams.pidParameters.maxOutput = 255
    motorParams.pidParameters.k_p = K_p
    motorParams.pidParameters.k_i = K_i
    motorParams.pidParameters.k_d = K_d

    interface.setMotorAngleControllerParameters(motors[0], motorParams)
    interface.setMotorAngleControllerParameters(motors[1], motorParams)

    return interface, motors


def angle_for_turn(turn_angle):
    return TAU_TO_ANGLE * turn_angle / 360.0


# distance in cm
def angle_for_distance(distance):
    return METER_TO_ANGLE * distance


# TODO: This should all be in a class... -fc
def move_by_angle(interface, motors, angle):
    interface.increaseMotorAngleReferences(motors, [angle, angle])


def turn_by_angle(interface, motors, angle):
    interface.increaseMotorAngleReferences(motors, [angle, -angle])


def wait_until_done(interface, motors):
    while not interface.motorAngleReferencesReached(motors):
        pass


def move_and_turn(interface, motors):
    move_by_angle(interface, motors, angle_for_distance(40))
    wait_until_done(interface, motors)

    turn_by_angle(interface, motors, angle_for_turn(90))
    wait_until_done(interface, motors)


if __name__ == '__main__':

    interface, motors = setup()

    for _ in xrange(0, 4):
        move_and_turn(interface, motors)

    interface.terminate()
