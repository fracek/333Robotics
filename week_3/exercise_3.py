import brickpi
import sys
import time
sys.path.append('../lib')
import rocommon


class DummyRobot:

    def __init__(self):
        self.interface = brickpi.Interface()
        self.interface.initialize()
        self.sonar = rocommon.Sonar(self, 2)
        print('Sonar: {}'.format(self.sonar))

    def implode(self):
        self.interface.terminate()

if __name__ == "__main__":
    robot = DummyRobot()
    while True:
        print robot.sonar.value()
        time.sleep(0.1)
