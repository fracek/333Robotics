import brickpi
import time
from math import pi


# Wrap func to wait for angle references to be reached before returning
def wait_references_reached(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        ret = func(*args, **kwargs)
        self.wait_until_done()
        return ret
    return wrapper


class Bumper:

    def __init__(self, owner, port):
        self.owner = owner
        self.port = port
        owner.interface.sensorEnable(port, brickpi.SensorType.SENSOR_TOUCH)
        print('New Bumper on port {}'.format(port))

    def __str__(self):
        return 'Bumper(owner = {}, port = {})'.format(self.owner, self.port)

    def touching(self):
        result = self.owner.interface.getSensorValue(self.port)
        if result:
            return result[0] == 1
        else:
            return False


class Sonar:

    def __init__(self, owner, sonarPort):
        self.owner = owner
        self.sonarPort = sonarPort
        owner.interface.sensorEnable(
            sonarPort, brickpi.SensorType.SENSOR_ULTRASONIC)

    def __str__(self):
        return 'Sonar(owner = {}, sonarPort = {})'.format(self.owner, self.sonarPort)

    def value(self):
        result = self.owner.interface.getSensorValue(self.sonarPort)
        if result:
            return result[0]
        else:
            return False


class SpinningSonar(Sonar):

    def __init__(self, owner, sonarPort, motorPort):
        Sonar.__init__(self, owner, sonarPort)

        self.motorPort = motorPort
        owner.interface.motorEnable(motorPort)
        # TODO: setup motor parameters

    def __str__(self):
        return 'SpinningSonar(owner = {}, sonarPort = {}, motorPort = {})'.format(self.owner, self.sonarPort, self.motorPort)


class Robot:
    K_u = [750.0, 750.0]
    P_u = [0.25, 0.25]

    TAU_TO_ANGLE = 36.2

    #                angle / distance
    METER_TO_ANGLE = 60. / 94.0

    TARGET_SONAR_VALUE = 34

    # BrickPi sensor and motor ports
    # http://www.dexterindustries.com/BrickPi/getting-started/attaching-lego/
    S1 = 0
    S2 = 1
    S3 = 2
    S4 = 3
    S5 = 4

    MA = 0
    MB = 1
    MC = 2
    MD = 3

    def __init__(self, use_spinning_sonar=False):
        self.interface = brickpi.Interface()
        self.interface.initialize()

        self.motors = [Robot.MA, Robot.MB]

        self.interface.motorEnable(self.motors[0])
        self.interface.motorEnable(self.motors[1])

        for motor in self.motors:
            k_p = 0.6 * Robot.K_u[motor]
            # TODO: hack to not die
            k_i = 2.0 * k_p / Robot.P_u[motor] * 0.05
            k_d = k_p * Robot.P_u[motor] / 8.0
            print('Motor {}: k_p = {:.2f} k_i = {:.2f} k_d = {:.2f}'.format(
                motor, k_p, k_i, k_d))
            motorParams = self.interface.MotorAngleControllerParameters()
            motorParams.maxRotationAcceleration = 6.0
            motorParams.maxRotationSpeed = 8.0
            motorParams.feedForwardGain = 255 / 20.0
            motorParams.minPWM = 30.0
            motorParams.pidParameters.minOutput = -255
            motorParams.pidParameters.maxOutput = 255
            motorParams.pidParameters.k_p = k_p
            motorParams.pidParameters.k_i = k_i
            motorParams.pidParameters.k_d = k_d

            self.interface.setMotorAngleControllerParameters(
                motor, motorParams)

        # setup bumper
        self.right_bumper = Bumper(self, Robot.S1)
        self.left_bumper = Bumper(self, Robot.S4)
        print('Bumpers: [{}, {}]'.format(self.left_bumper, self.right_bumper))

        # setup sonar
        if use_spinning_sonar:
            self.sonar = SpinningSonar(self, Robot.S3, Robot.MC)
        else:
            self.sonar = Sonar(self, Robot.S3)
        print('Sonar: {}'.format(self.sonar))

    def _angle_for_turn(self, turn_angle):
        return Robot.TAU_TO_ANGLE * turn_angle / (2 * pi)

    def _angle_for_distance(self, distance):
        return Robot.METER_TO_ANGLE * distance

    @wait_references_reached
    def _move_by_angle(self, angle):
        self.interface.increaseMotorAngleReferences(
            self.motors, [angle, angle])

    @wait_references_reached
    def _turn_by_angle(self, angle):
        self.interface.increaseMotorAngleReferences(
            self.motors, [angle, -angle])

    def wait_until_done(self):
        while not self.interface.motorAngleReferencesReached(self.motors):
            time.sleep(0.1)

    def turn(self, angle):
        self._turn_by_angle(self._angle_for_turn(angle))

    def left_90(self):
        self.turn(pi/2)

    def right_90(self):
        self.turn(-pi/2)

    def move_forward(self, distance):
        self._move_by_angle(self._angle_for_distance(distance))

    def move_backward(self, distance):
        self._move_by_angle(-self._angle_for_distance(distance))

    def implode(self):
        self.interface.terminate()

    def start_logging(self, path):
        print('START LOG ({})'.format(path))
        self.interface.startLogging(path)

    def stop_logging(self):
        self.interface.stopLogging()
        print('STOP LOG')

    def set_rotation_speed(self, speed, motors=None):
        if motors:
            self.interface.setMotorRotationSpeedReferences(motors, speed)
        else:
            self.interface.setMotorRotationSpeedReferences(
                self.motors, [speed, speed])
