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
        ch_map = rocommon.ChallengeMap()
        ch_map.draw()

        robot = rocommon.FinalRobot(map=ch_map)
        robot.load_all_locations()
        # start by guessing where we are
        loc, angle = robot.guess_location()
        print('loc = {}, angle = {}'.format(loc, angle))
        if loc is not 1:
            robot.set_starting_location([0.0, 0.0], angle)
            robot.move_to_waypoint([0.0, 21.0 - 63.0])
            robot.sonar.rotate_by(0.5 * np.pi)
            sonar_value = robot.sonar.value()
            print('Sonar reading = {}'.format(sonar_value))
            if sonar_value < 50:
                loc = 0
            else:
                loc = 2
        else:
            robot.set_starting_location(STARTING_POINTS[loc], angle)
        print('location = {}'.format(loc))

        # rotate and set rotation
        for wp in WAYPOINTS[loc]:
            robot.move_to_waypoint(wp)
            robot.update_measurement()
            robot.draw_particles()
    except KeyboardInterrupt:
        pass
    robot.implode()
