import sys
sys.path.append('../lib')
import rocommon
import time

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
                    map=lab_map, starting_x=[84.0, 30.0, 0.0],
                    e_sigma=0.1, f_sigma=0.05, g_sigma=0.1)
        else:
            robot = rocommon.ProbabilisticRobot(
                    map=lab_map, starting_x=[84.0, 30.0, 0.0],
                    e_sigma=1.0, f_sigma=0.50, g_sigma=1.0)

        for wp in WAYPOINTS:
            robot.move_to_waypoint(wp)
            robot.draw_particles()
            time.sleep(2.0)
            robot.update_measurement()
            robot.draw_particles()
    except KeyboardInterrupt:
        pass
    robot.implode()
