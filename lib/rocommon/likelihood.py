import numpy as np


def compute_expected_depth(pos, walls):
    [x, y, theta] = pos

    def compute_distance_from_wall(wall):
        (Ax, Ay, Bx, By) = wall

        # Check angle beta between sonar and the normal to the wall
        num = np.cos(theta) * (Ay - By) + np.sin(theta) * (Bx - Ax)
        den = np.sqrt(np.square(Ay - By) + np.square(Bx - Ax))
        beta = np.arccos(num / den)

        # Compute distance between sonar and wall
        num = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
        den = (By - Ay) * np.cos(theta) - (Bx - Ax) * np.sin(theta)
        m = num / den

        # Check hit point on the wall
        # SEE: http://www.lucidarme.me/?p=1952
        C = np.array([x + m * np.cos(theta), y + m * np.sin(theta)])
        AB = [Bx - Ax, By - Ay]
        AC = C - [Ax, Ay]
        K_ac = np.dot(AB, AC)
        K_ab = np.dot(AB, AB)
        if (0 < K_ac < K_ab) and m >= 0:
            return m, beta

        return np.inf, beta

    distances_and_angles = [compute_distance_from_wall(w) for w in walls]
    return min(distances_and_angles, key=lambda e: e[0])


def compute_likelihood(m, a, z):
    K = 0.1

    sigma = 3.5
    p = np.exp(-np.square(z - m) / (2.0 * np.square(sigma))) + K

    # The likelihood of getting bad readings is greater when outside the optimal
    # sensor range (20 < m < 120). This means that getting a bad reading is not
    # necessarily a bad thing, and could be a good sign if the nearest wall is
    # very close or very far away.
    MIN_RANGE = 20.0
    MAX_RANGE = 120.0
    if m < MIN_RANGE and z == 255:
        p += 0.8
    elif m > MAX_RANGE and z == 255:
        p += 0.8

    # In the case when the sonar angle is not optimal (a > pi/4) it is very likely
    # to get a bad reading from the sonar (z == 255)
    if np.abs(a) > np.pi / 4:
        if z == 255:
            p = 0.8
        else:
            p = K

    return p
