import sys
sys.path.append('../lib')
import rocommon
import numpy as np


def learn_location(container, robot):
    ls = rocommon.LocationSignature()

    num_bins = len(ls.sig)
    for i in range(num_bins):
        # read a value from sonar
        robot.sonar.rotate_by(2.0 * np.pi / float(num_bins))
        sonar_value = robot.sonar.value()
        ls.sig[i] = sonar_value

    idx = container.get_free_index()
    if idx == -1:
        print('Warning: no more file available')
    container.save(ls, idx)
    print('Location {} learned and saved'.format(idx))

if __name__ == "__main__":
    try:
        robot = rocommon.ProbabilisticRobot(use_spinning_sonar=True)
        # starting_x=[84.0, 30.0, 0.0])
        container = rocommon.SignatureContainer(size=5)
        container.delete_loc_files()
        for _ in xrange(0, 5):
            learn_location(container, robot)
    except KeyboardInterrupt:
        pass
    robot.implode()
