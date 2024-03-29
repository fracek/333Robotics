import sys
sys.path.append('../lib')
import rocommon

SPEED = 4.0


if __name__ == "__main__":
    robot = rocommon.Robot()

    try:
        while True:
            v = -(robot.TARGET_SONAR_VALUE - robot.sonar.value())
            robot.set_rotation_speed(v)
    except KeyboardInterrupt:
        robot.implode()
