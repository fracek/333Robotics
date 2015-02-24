import sys
sys.path.append('../lib')
import rocommon

WAYPOINTS = [
        [180, 30],
        [180, 54],
        [126, 54],
        [126, 168],
        [126, 126],
        [30, 54],
        [84, 54],
        [84, 30]]

GOOD_ODOMETRY = True

if __name__ == "__main__":
    try:
        lab_map = rocommon.LabMap()
        lab_map.draw()

        if GOOD_ODOMETRY:
            robot = rocommon.ProbabilisticRobot(
                    map=lab_map, starting_x=[84.0, 30.0, 0.0])
        else:
            robot = rocommon.ProbabilisticRobot(
                    map=lab_map, starting_x=[84.0, 30.0, 0.0],
                    e_sigma=0.15, f_sigma=0.05, g_sigma=0.15)

        for wp in WAYPOINTS:
            robot.move_to_waypoint_with_step(wp, 20.0)
    except KeyboardInterrupt:
        pass
    robot.implode()
