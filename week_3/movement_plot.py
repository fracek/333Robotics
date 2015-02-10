import matplotlib.pyplot as plt
import numpy as np

DATA_PATH = 'data/ex_1_{}.log'
DATA_POINTS = 7
ALPHA = 0.3


if __name__ == "__main__":
    fig = plt.figure(1)
    cm = plt.get_cmap('gist_rainbow')
    cgen = [cm(1.0 * i / DATA_POINTS) for i in range(DATA_POINTS + 1)]
    for i in xrange(1, DATA_POINTS + 1):
        print('reading {}'.format(DATA_PATH.format(i)))
        data = np.genfromtxt(DATA_PATH.format(i))
        w = np.ones(len(data)) / len(data)
        data[:, 2] = np.radians(data[:, 2])
        mean_x = np.sum(data.T * w, axis=1)
        x = data[:, 0]
        y = data[:, 1]
        u = np.cos(data[:, 2])
        v = np.sin(data[:, 2])
        plt.quiver(x, y, u, v, color=cgen[i], alpha=ALPHA)
        plt.plot(mean_x[0], mean_x[1], 'o', color=cgen[i])
    plt.xlim([0, 60])
    plt.ylim([-30, 40])
    plt.show()
