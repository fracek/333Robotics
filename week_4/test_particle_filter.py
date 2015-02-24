import sys
sys.path.append('../lib/rocommon/')
import particles
import numpy as np


def count_equal(x, e):
    """count number of rows of x equal to vector e"""
    return np.sum(np.all(x == e, axis=1))


# The idea behind this test is to have a limited number of points that have a big
# weight. After resampling we expect this points to be the only present in the
# new particle set.
if __name__ == "__main__":
    n = 100
    ps = particles.ParticleSet([0, 0, 0], n, 0.03, 0.01, 0.03)
    ps.w = np.zeros(n)
    ps.x[1, :] = [1.0, 1.0, 1.0]
    ps.w[1] = 5

    ps.x[2, :] = [2.0, 2.0, 2.0]
    ps.w[2] = 2.5

    ps.x[-2, :] = [-2.0, -2.0, -2.0]
    ps.w[-2] = 2.5

    # Probably never picked
    ps.x[5, :] = [5.0, 5.0, 5.0]
    ps.w[5] = 0.1

    ps.normalize()

    ps.resample()

    print('x == [ 1.,  1.,  1.] = {}'.format(count_equal(ps.x, [1., 1., 1.])))
    print('x == [ 2.,  2.,  2.] = {}'.format(count_equal(ps.x, [2., 2., 2.])))
    print('x == [-2., -2., -2.] = {}'.format(count_equal(ps.x, [-2., -2., -2.])))
    print('x == [ 5.,  5.,  5.] = {}'.format(count_equal(ps.x, [5., 5., 5.])))
