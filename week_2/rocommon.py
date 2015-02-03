import brickpi

# Wrap func to wait for angle references to be reached before returning
def wait_references_reached(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        ret = func(*args, **kwargs)
        self.WaitUntilDone()
        return ret
    return wrapper


class Bumper:
    def __init__(self, owner, port):
        self.owner = owner
        self.port = port
        owner.interface.sensorEnable(port, brickpi.SensorType.SENSOR_TOUCH)
        print('New Bumper on port {}'.format(port))

    def IsTouching(self):
        result = self.owner.interface.getSensorValue(self.port)
        if result:
            return result[0] == 1
        else:
            return False


class Robot:
    K_u = [750.0, 750.0]
    P_u = [0.25, 0.25]

    TAU_TO_ANGLE = 17.95

    METER_TO_ANGLE = 20. / 55

    def __init__(self):
        self.interface = brickpi.Interface()
        self.interface.initialize()

        self.motors = [0, 1]

        self.interface.motorEnable(self.motors[0])
        self.interface.motorEnable(self.motors[1])

        for motor in self.motors:
            k_p = 0.6 * Robot.K_u[motor]
            # TODO: hack to not die
            k_i = 2.0 * k_p / Robot.P_u[motor] * 0.1
            k_d = k_p * Robot.P_u[motor] / 8.0
            print('Motor {}: k_p = {:.2f} k_i = {:.2f} k_d = {:.2f}'.format(motor, k_p, k_i, k_d))
            motorParams = self.interface.MotorAngleControllerParameters()
            motorParams.maxRotationAcceleration = 6.0
            motorParams.maxRotationSpeed = 12.0
            motorParams.feedForwardGain = 255 / 20.0
            motorParams.minPWM = 18.0
            motorParams.pidParameters.minOutput = -255
            motorParams.pidParameters.maxOutput = 255
            motorParams.pidParameters.k_p = k_p
            motorParams.pidParameters.k_i = k_i
            motorParams.pidParameters.k_d = k_d

            self.interface.setMotorAngleControllerParameters(motor, motorParams)

        # setup bumper
        self.right_bumper = Bumper(self, 0)
        self.left_bumper = Bumper(self, 3)

    def _angle_for_turn(self, turn_angle):
        return Robot.TAU_TO_ANGLE * turn_angle / 360.0

    def _angle_for_distance(self, distance):
        return Robot.METER_TO_ANGLE * distance

    @wait_references_reached
    def _move_by_angle(self, angle):
        self.interface.increaseMotorAngleReferences(self.motors, [angle, angle])

    @wait_references_reached
    def _turn_by_angle(self, angle):
        self.interface.increaseMotorAngleReferences(self.motors, [-angle, angle])

    def WaitUntilDone(self):
        while not self.interface.motorAngleReferencesReached(self.motors):
            pass

    def Turn(self, angle):
        self._turn_by_angle(self._angle_for_turn(angle))

    def Left90deg(self):
        self.Turn(-90)

    def Right90deg(self):
        self.Turn(90)

    def MoveForward(self, distance):
        self._move_by_angle(self._angle_for_distance(distance))

    def MoveBackward(self, distance):
        self._move_by_angle(-self._angle_for_distance(distance))

    def Implode(self):
        self.interface.terminate()

    def StartLogging(self, path):
        print('START LOG ({})'.format(path))
        self.interface.startLogging(path)

    def StopLogging(self):
        self.interface.stopLogging()
        print('STOP LOG')

    def SetRotationSpeed(self, motors, speed):
        self.interface.setMotorRotationSpeedReferences(motors, [speed, speed])