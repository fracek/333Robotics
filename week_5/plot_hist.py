import sys
sys.path.append('../lib/rocommon/')
from signature_container import *
import matplotlib.pyplot as plt


def read_histogram(path):
    c = SignatureContainer(size=5, path=path, no_bins=72)
    ls = []
    for idx in range(c.size):
        ls.append(c.read(idx))
    return ls

if __name__ == "__main__":
    test_h = read_histogram('test_data/')
    training_h = read_histogram('training_data/')

    for i, (hk, hm) in enumerate(zip(test_h, training_h)):
        f, ax = plt.subplots()
        plt.subplot(2, 1, 1)
        plt.hist(hk.sig, bins=len(hk.sig))
        plt.xlim([0, 260])
        plt.subplot(2, 1, 2)
        plt.hist(hk.sig, bins=len(hk.sig))
        plt.xlim([0, 260])
        f.suptitle('Point {}'.format(i + 1))
        plt.show()
