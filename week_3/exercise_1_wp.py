import sys
sys.path.append('../lib')
import rocommon

STEP_DISTANCE = 10
WAYPOINTS = [
    [10, 0], [20, 0], [30, 0], [40, 0],  # first side
    [40, 10], [40, 20], [40, 30], [40, 40],  # second side
    [30, 40], [20, 40], [10, 40], [0, 40],  # third side
    [0, 30], [0, 20], [0, 10], [0, 0]]  # fourth side


if __name__ == "__main__":
    robot = rocommon.ProbabilisticRobot()

    try:
        for wp in WAYPOINTS:
            robot.move_to_waypoint(wp)
            robot.draw_particles()
    except KeyboardInterrupt:
        pass
    robot.implode()
