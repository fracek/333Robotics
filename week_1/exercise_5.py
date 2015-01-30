import numpy as np


DATA_PATH = "data/square_data.csv"

# (x, y) coordinates of final positions
if __name__ == '__main__':
    data = np.genfromtxt(DATA_PATH, delimiter=",")
    print np.cov(data.T, bias=1)
