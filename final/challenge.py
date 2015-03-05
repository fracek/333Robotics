import sys
sys.path.append('../lib')
import rocommon
import numpy as np

STARTING_POINTS = [[21, 21], [273, 63], [525, 21]]
WAYPOINTS = np.array([
#    0                     1                     2
  [21, 63],            [273, 63],            [525, 63],
  [21, 21], [147, 21], [273, 21], [399, 21], [525, 21]
#    3          4          5          6          7
])

WAYPOINTS_FOR_STARTING_LOC = [
  [4, 5, 6, 7, 2, 7, 6, 5, 1, 5, 4, 3, 0], # loc = 0, we start in 3
  [5, 6, 7, 2, 7, 6, 5, 4, 3, 0, 3, 4, 5, 1], # loc = 1
  [6, 5, 4, 3, 0, 3, 4, 5, 1, 5, 6, 7, 2] # loc = 2, we start in 7
]

H_PI = 0.5 * np.pi

def wp_coincide(w1, w2):
    return np.all(w1 == w2)


def guess_starting_location(robot):
    # start by guessing where we are
    loc, angle = robot.guess_location()
    #print('loc = {}, angle = {}'.format(loc, angle))
    if loc is not 1:
        # WARNING: using different coordinates than the real map
        robot.set_starting_location([0.0, 0.0], angle)
        robot.move_to_waypoint([0.0, 21.0 - 63.0])
        robot.sonar.rotate_by(H_PI)
        sonar_value = robot.sonar.value()
        #print('Sonar reading = {}'.format(sonar_value))
        angle = -H_PI
        # TODO: check by loc, don't turn in 2
        robot.sonar.rotate_by(angle)
        if sonar_value < 50:
            loc = 0
        else:
            loc = 2
    return loc, angle

if __name__ == "__main__":
    try:
        ch_map = rocommon.ChallengeMap()
        ch_map.draw()

        robot = rocommon.FinalRobot(map=ch_map)
        robot.load_all_locations()

        loc, angle = guess_starting_location(robot)

        # rotate and set rotation
        waypoints = WAYPOINTS[WAYPOINTS_FOR_STARTING_LOC[loc]]

        robot.set_starting_location(STARTING_POINTS[loc], angle)
        prev_wp = [STARTING_POINTS[loc][0], STARTING_POINTS[loc][1]]

        for wp in waypoints:
            angle_offset = 0.0
            sign = 1.0

            if wp_coincide(wp, WAYPOINTS[5]):
                if wp_coincide(prev_wp, WAYPOINTS[4]):
                    angle_offset = H_PI
                    sign = -1.0
                elif wp_coincide(prev_wp, WAYPOINTS[6]):
                    angle_offset = H_PI

            if wp_coincide(wp, WAYPOINTS[3]):
                if wp_coincide(prev_wp, WAYPOINTS[4]):
                    angle_offset = H_PI

            if wp_coincide(wp, WAYPOINTS[7]):
                if wp_coincide(prev_wp, WAYPOINTS[6]):
                    angle_offset = H_PI
                    sign = -1.0

            if wp_coincide(wp, WAYPOINTS[4]):
                if wp_coincide(prev_wp, WAYPOINTS[3]):
                    angle_offset = -H_PI
                    sign = -1.0
                else:
                    angle_offset = -H_PI

            if wp_coincide(wp, WAYPOINTS[6]):
                if wp_coincide(prev_wp, WAYPOINTS[7]):
                    angle_offset = -H_PI
                    #sign = -1.0
                else:
                    angle_offset = -H_PI
                    sign = -1.0

            robot.move_to_waypoint(wp)

            robot.sonar.rotate_by(sign * angle_offset)
            robot.update_measurement(angle_offset)
            robot.sonar.rotate_by(- sign * angle_offset)

            robot.draw_particles()
            prev_wp = wp
    except KeyboardInterrupt:
        pass
    robot.implode()
