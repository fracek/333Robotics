import sys
sys.path.append('../lib/rocommon/')
import likelihood as lh
import numpy as np
import matplotlib.pyplot as plt

def likelihood(m, z):
    p = [lh.compute_likelihood(m, x) for x in z]
    return p

def plot(z, p, m):
    plt.plot(z, p)
    plt.axvline(x=m, color='r')

if __name__ == "__main__":
    z = np.linspace(0.0, 255.0, 400)
    for i, m in enumerate([15.0, 40.0, 60.0, 80.0, 150.0, np.nan]):
        p = likelihood(m, z)
        plt.subplot(3, 2, i)
        plt.plot(z, p, color='k')
        plt.fill_between(z, 0, p, facecolor=[0.8, 0.8, 0.8])
        plt.ylim([0, 1.5])
        plt.xlim([0, 255])
        plt.grid()
        plt.title('m = {}'.format(m))
        plt.xlabel('z')
        plt.ylabel('p(z|m)')
    plt.show()
