import matplotlib.pyplot as plt
import numpy as np

LOG_PATH = 'data/log_exercise_1.log'
ALPHA = 0.5
ARROW_WIDTH = 0.001
DATA_POINTS = 20
SQUARE_PATH = [[0, 40, 40, 0, 0], [0, 0, 40, 40, 0]]


def as_array(v):
    return np.squeeze(np.asarray(v))


if __name__ == "__main__":
    fig = plt.figure(1)
    cm = plt.get_cmap('gist_rainbow')
    cgen = [cm(1.0 * i / DATA_POINTS) for i in range(DATA_POINTS + 1)]
    plt.plot(SQUARE_PATH[0], SQUARE_PATH[1],
             color='black', linewidth=2, alpha=0.5)
    plt.xlim([-10, 50])
    plt.ylim([-10, 50])
    plt.axes().set_aspect('equal', 'datalim')
    plt.grid()
    # starting point
    plt.plot(0, 0, 'o', color='white')
    # add particles
    try:
        with open(LOG_PATH, 'r') as f:
            i = 0
            for command in f:
                # skip 'drawParticles: ' part
                data_as_str = command[15:]
                data = np.matrix(data_as_str)
                data = data.reshape((-1, 3))
                # undo transformation to make data visible on web
                data = 0.5 * (data - [500.0, 250.0, 0.0])
                w = np.ones([len(data), 1]) / len(data)
                mean_x = np.sum(data.T * w, axis=1)

                # convert to arrays to avoid errors in plt.quiver
                x = as_array(data[:, 0])
                y = as_array(data[:, 1])
                a = as_array(data[:, 2])
                u = np.cos(a)
                v = np.sin(a)

                plt.quiver(x, y, u, v,
                           color=cgen[i], alpha=ALPHA, width=ARROW_WIDTH,
                           scale=50.0)
                plt.plot(x, y, 'x', color=cgen[i])

                plt.plot(mean_x[0], mean_x[1], 'o', color=cgen[i])
                plt.quiver(as_array(mean_x[0]), as_array(mean_x[1]),
                           np.cos(as_array(mean_x[2])), np.sin(as_array(mean_x[2])),
                           color=cgen[i], width=5 * ARROW_WIDTH)
                i = i + 1
    except KeyboardInterrupt:
        pass
    plt.savefig('position_estimates.eps')
