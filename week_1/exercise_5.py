import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = "data/square_data.csv"

# (x, y) coordinates of final positions
if __name__ == '__main__':
    data = np.genfromtxt(DATA_PATH, delimiter=",")
    print np.cov(data.T, bias=1)

    plt.scatter(data.T[0], data.T[1])
    plt.grid()
    plt.show()
