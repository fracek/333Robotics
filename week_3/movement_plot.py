import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

LOG_PATH = 'data/log_exercise_1.log'
ALPHA = 0.5
ARROW_WIDTH = 0.001
DATA_POINTS = 20
SQUARE_PATH = [[0, 40, 40, 0, 0], [0, 0, 40, 40, 0]]

XY_MIN = -10
XY_MAX = 50


def as_array(v):
    return np.squeeze(np.asarray(v))


if __name__ == "__main__":
    _, ax = plt.subplots()
    ax.set_title('Probabilistic Robot Position Estimates')

    cm = plt.get_cmap('gist_rainbow')
    cgen = [cm(1.0 * i / DATA_POINTS) for i in range(DATA_POINTS + 1)]

    ax.axis((XY_MIN, XY_MAX, XY_MIN, XY_MAX))
    # keep square aspect ratio
    ax.axes.set_aspect('equal', 'datalim')

    ax.grid()

    # draw big tick every 10 cm, small every 5
    major_locator = ticker.MultipleLocator(10.0)
    minor_locator = ticker.MultipleLocator(5.0)
    ax.xaxis.set_major_locator(major_locator)
    ax.yaxis.set_major_locator(major_locator)
    ax.xaxis.set_minor_locator(minor_locator)
    ax.yaxis.set_minor_locator(minor_locator)

    ax.set_xlabel('World X')
    ax.set_ylabel('World Y')

    # draw path
    ax.plot(SQUARE_PATH[0], SQUARE_PATH[1], color='black', linewidth=2,
            alpha=0.5)
    # starting point
    ax.plot(0, 0, 'o', color='white')
    # add particles
    with open(LOG_PATH, 'r') as f:
        for i, command in enumerate(f):
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

            ax.quiver(x, y, u, v,
                      color=cgen[i], alpha=ALPHA, width=ARROW_WIDTH,
                      scale=50.0)
            ax.plot(x, y, 'x', color=cgen[i])

            ax.plot(mean_x[0], mean_x[1], 'o', color=cgen[i])
            ax.quiver(as_array(mean_x[0]), as_array(mean_x[1]),
                      np.cos(as_array(mean_x[2])), np.sin(as_array(mean_x[2])),
                      color=cgen[i], width=5 * ARROW_WIDTH)
    plt.savefig('position_estimates.pdf')
