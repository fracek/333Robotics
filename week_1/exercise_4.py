import rocommon

TAU_TO_ANGLE = 17.85

METER_TO_ANGLE = 20. / 55


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

    interface, motors = rocommon.setup()

    for _ in xrange(0, 4):
        move_and_turn(interface, motors)

    interface.terminate()
