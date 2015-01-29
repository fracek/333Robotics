import brickpi

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

