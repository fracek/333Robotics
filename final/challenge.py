import sys
sys.path.append('../lib')
import rocommon
import numpy as np

STARTING_POINTS = [[21, 63], [273, 63], [525, 63]]
WAYPOINTS = [
        # starting in 0
        [[21, 21], [273, 21], [525, 21], [525, 63], [525, 21],
        [273, 21], [273, 63], [273, 21], [21, 21], [21, 63]],
        # starting in 1
        [],
        # starting in 2
        []
]

if __name__ == "__main__":
    try:
        robot = rocommon.FinalRobot()
        robot.load_all_locations()
        # start by guessing where we are
        #loc, angle = robot.guess_location()
        loc = 0
        angle = -np.pi/2.0
        robot.set_starting_location(STARTING_POINTS[loc], angle)
        # rotate and set rotation
        for wp in WAYPOINTS[loc]:
            robot.move_to_waypoint(wp)
            robot.update_measurement()
            robot.draw_particles()
    except KeyboardInterrupt:
        pass
    robot.implode()
