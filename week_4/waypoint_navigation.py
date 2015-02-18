import sys
sys.path.append('../lib')
import rocommon

STEP_DISTANCE = 10
WAYPOINTS = [
        [180, 30],
        [180, 54],
        [126, 54],
        [126, 168],
        [126, 126],
        [30, 54],
        [84, 54],
        [84, 30]]

if __name__ == "__main__":
    try:
        lab_map = rocommon.LabMap()
        lab_map.draw()
        robot = rocommon.ProbabilisticRobot(
                map=lab_map, starting_x=[84.0, 30.0, 0.0])
        for wp in WAYPOINTS:
            robot.move_to_waypoint(wp)
            robot.update_measurement()
            robot.draw_particles()
    except KeyboardInterrupt:
        pass
    robot.implode()
