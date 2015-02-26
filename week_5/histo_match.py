import sys
sys.path.append('../lib/rocommon/')
from signature_container import *
import numpy as np

def distance_histogram_error(hm, hk):
    (hm_h, _) = np.histogram(hm, bins=256, range=(0, 255))
    (hk_h, _) = np.histogram(hk, bins=256, range=(0, 255))

    return np.sum((hm_h - hk_h) ** 2.0)


def histogram_error(hm, hk, shift=0):
    s = 0.0
    for idx in xrange(len(hm)):
        s = s + (hm[idx] - hk[(shift + idx) % len(hm)])**2
    return s


def read_histogram(path):
    c = SignatureContainer(size=5, path=path, no_bins=72)
    ls = []
    for idx in range(c.size):
        ls.append(c.read(idx))
    return ls

def simple_test(test_h, training_h):
    for hk in test_h:
        min_err = np.inf
        min_hm = None
        for hm in training_h:
            for shift in xrange(len(hm.sig)):
                err = histogram_error(hm.sig, hk.sig, shift)
                if err < min_err:
                    min_err = err
                    min_hm = hm
                    min_shift = shift
        print('Best match for {} is {}, err = {}, shift = {}'.format(hk.idx, min_hm.idx, min_err, min_shift))

def advanced_test(test_h, training_h):
    for hk in test_h:
        min_err = np.inf
        min_hm = None
        for hm in training_h:
            err = distance_histogram_error(hm.sig, hk.sig)
            if err < min_err:
                min_err = err
                min_hm = hm
        min_shift_err = np.inf
        for shift in xrange(len(min_hm.sig)):
            err = histogram_error(min_hm.sig, hk.sig, shift)
            if err < min_shift_err:
                min_shift_err = err
                min_shift = shift
        print('Best match for {} is {}, err = {}, {}, shift = {}'.format(hk.idx, min_hm.idx, min_err, min_shift_err, min_shift))

if __name__ == "__main__":
    test_h = read_histogram('test_data/')
    training_h = read_histogram('training_data/')
    simple_test(test_h, training_h)

    print
    advanced_test(test_h, training_h)
