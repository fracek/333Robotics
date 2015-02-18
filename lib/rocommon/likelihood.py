import numpy as np


def compute_expected_depth(pos, walls):
    [x, y, theta] = pos

    def compute_distance_from_wall(wall):
        (Ax, Ay, Bx, By) = wall

        # Check angle beta between sonar and the normal to the wall
        num = np.cos(theta) * (Ay - By) + np.sin(theta) * (Bx - Ax)
        den = np.sqrt(np.square(Ay - By) + np.square(Bx - Ax))
        beta = np.arccos(num / den)
        if np.abs(beta) > np.pi / 4.0:
            return np.inf

        # Compute distanec between sonar and wall
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
            return m

        return np.inf

    distances = [compute_distance_from_wall(w) for w in walls]
    # TODO: check for crap values
    return np.min(distances)


def compute_likelihood(x, z, walls):
    m = compute_expected_depth(x, walls)
    # TODO: USE REAL CONSTANTS NOT THIS CRAP
    sigma = 0.5
    k = 0.1
    p = np.exp(-np.square(z - m) / (2.0 * np.square(sigma))) + k
    print('m = {}, z = {}, p = {}'.format(m, z, p))
    return p
