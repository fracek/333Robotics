import numpy as np

# (x, y) coordinates of final positions
data = np.array([[0, 2],
                 [1, 1],
                 [2, 0],
                 [1, 1],
                 [2, 0],
                 [1, 1],
                 [2, 0],
                 [1, 1],
                 [2, 0],
                 [1, 1]]).T


print np.cov(data, bias=1)
