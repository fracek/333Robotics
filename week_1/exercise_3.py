import brickpi
import time

TAU_TO_ANGLE = 18.0

METER_TO_ANGLE = 3.14 / 10.0

K_u = [850.0, 800.0]
P_u = [0.3, 0.3]


def setup():
    interface = brickpi.Interface()
    interface.initialize()

    motors = [0, 1]

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    for motor in motors:
        k_p = 0.6 * K_u[motor]
        k_i = 2.0 * k_p / P_u[motor]
        k_d = k_p * P_u[motor] / 8.0
        motorParams = interface.MotorAngleControllerParameters()
        motorParams.maxRotationAcceleration = 6.0
        motorParams.maxRotationSpeed = 12.0
        motorParams.feedForwardGain = 255 / 20.0
        motorParams.minPWM = 18.0
        motorParams.pidParameters.minOutput = -255
        motorParams.pidParameters.maxOutput = 255
        motorParams.pidParameters.k_p = k_p
        motorParams.pidParameters.k_i = k_i
        motorParams.pidParameters.k_d = k_d

        interface.setMotorAngleControllerParameters(motor, motorParams)

    return interface, motors


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

    interface, motors = setup()

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
