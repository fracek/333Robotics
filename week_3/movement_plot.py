import matplotlib.pyplot as plt
import numpy as np
import sys

DATA_PATH = 'data/ex_1_{}.log'
DATA_POINTS = 7
ALPHA = 0.3
ARROW_WIDTH = 0.002

SQUARE_PATH = [[0, 40, 40, 0, 0], [0, 0, 40, 40, 0]]

if __name__ == "__main__":
    fig = plt.figure(1)
    cm = plt.get_cmap('gist_rainbow')
    cgen = [cm(1.0 * i / DATA_POINTS) for i in range(DATA_POINTS + 1)]
    plt.plot(SQUARE_PATH[0], SQUARE_PATH[1], color='black', linewidth=2, alpha=0.5)
    plt.xlim([-10, 50])
    plt.ylim([-10, 50])
    plt.axes().set_aspect('equal', 'datalim')
    plt.grid()
    # add particles
    try:
        while True:
            command = sys.stdin.readline()
            # skip 'drawParticles: ' part
            data_as_str = command[15:]
            data = np.matrix(data_as_str)
            data = data.reshape((-1, 3))
            data = 0.5 * (data - [500.0, 250.0, 0.0])
            print('Read {}'.format(data))
            #for i in xrange(1, DATA_POINTS + 1):
            #    print('reading {}'.format(DATA_PATH.format(i)))
            w = np.ones([len(data), 1]) / len(data)
            data[:, 2] = np.radians(data[:, 2])
            mean_x = np.sum(data.T * w, axis=1)
            print('mean_x = {}'.format(mean_x))
            x = data[:, 0]
            y = data[:, 1]
            u = np.cos(data[:, 2])
            v = np.sin(data[:, 2])
            #plt.quiver(x, y, u, v, color=cgen[i], alpha=ALPHA, width=ARROW_WIDTH, scale=50.0)
            plt.plot(mean_x[0], mean_x[1], 'o', color=cgen[i])
    except KeyboardInterrupt:
        pass
    plt.savefig('movement.eps')
