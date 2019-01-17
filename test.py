import numpy as np
import matplotlib.pyplot as plt
a = np.array([[16, 31, 15, 4, 10, 28],
              [17, 27, 25, 20, 35, 21],
              [14,  3, 19, 29,  1, 11],
              [0,  6,  5, 13,  2,  8],
              [24, 30, 32, 12, 26,  9],
              [18, 22, 34, 33,  7, 23]])
b = np.argsort(a, axis=None)[::-1]
# idx_list = np.unravel_index(np.argsort(a, axis=None), (36,))
# k = idx_list.reshape((6,6))
for idx in b:
	x = int(idx / 6)
	y = int(idx % 6)
	print(a[x, y])
print(a)
print(b)
 