import sys
sys.path.append('../lib')
import rocommon

STEP_DISTANCE = 10

if __name__ == "__main__":
    try:
        lab_map = rocommon.LabMap()
        lab_map.draw()
        robot = rocommon.ProbabilisticRobot(map=lab_map)
    except KeyboardInterrupt:
        pass
    robot.implode()
