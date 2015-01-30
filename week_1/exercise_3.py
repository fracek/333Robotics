import rocommon
import time

TAU_TO_ANGLE = 17.95

METER_TO_ANGLE = 20. / 55


def angle_for_turn(turn_angle):
    return TAU_TO_ANGLE * turn_angle / 360.0


# distance in cm
def angle_for_distance(distance):
    return METER_TO_ANGLE * distance


def move_by_angle(interface, motors, angle):
    interface.increaseMotorAngleReferences(motors, [angle, angle])


def turn_by_angle(interface, motors, angle):
    interface.increaseMotorAngleReferences(motors, [angle, -angle])


if __name__ == '__main__':

    interface, motors = rocommon.setup()

    while True:
        choice = raw_input('T = turn; M = move: ')
        angle = float(input("Angle (real): "))

        if choice == 'T':
            turn_by_angle(interface, motors, angle_for_turn(angle))
        else:
            move_by_angle(interface, motors, angle_for_distance(angle))

        while not interface.motorAngleReferencesReached(motors):
            motorAngles = interface.getMotorAngles(motors)
            if motorAngles:
                print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
            time.sleep(0.1)

        print "Destination reached!"

    interface.terminate()
