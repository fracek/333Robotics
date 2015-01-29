import rocommon
import time


def move_by_angle(interface, motors, angle):
    interface.increaseMotorAngleReferences(motors, [angle, angle])


def turn_by_angle(interface, motors, angle):
    interface.increaseMotorAngleReferences(motors, [angle, -angle])


if __name__ == '__main__':

    interface, motors = rocommon.setup()

    while True:
        choice = raw_input('T = turn; M = move: ')
        angle = float(input("Angle: "))

        if choice == 'T':
            turn_by_angle(interface, motors, angle)
        else:
            move_by_angle(interface, motors, angle)

        while not interface.motorAngleReferencesReached(motors):
            motorAngles = interface.getMotorAngles(motors)
            if motorAngles:
                print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
            time.sleep(0.1)

        print "Destination reached!"

    interface.terminate()
