'''
FILL A NUMPY ARRAY USING THE MULTIPROCESSING MODULE
https://jonasteuwen.github.io/numpy/python/multiprocessing/2017/01/07/multiprocessing-numpy-array.html

In the example we fill a square array where each of the values can be computed independently of each other.

The approach taken here is to split the larger array into smaller squares and run a process on each square.

Because we want to side step the Global Interpreter Lock we need to share the memory of the array somehow.

Here is where the sharedctypes comes in.This allows us to access the array as if it were a C array.

Because C is not dynamically typed as python is, we need to properly declare the type of the array.

Numpy provides a convenient function to read in the C array as a numpy array.
'''

import numpy as np
import itertools
from multiprocessing import Pool
from multiprocessing import sharedctypes

size = 100
block_size = 4

X = np.random.random((size, size)) # a random 100 x 100 matrix
result = np.ctypeslib.as_ctypes(np.zeros((size,size)))
shared_array = sharedctypes.RawArray(result._type_, result)
tmp = np.zeros((100,100)) # placeholder

def fill_per_window(args):
    window_x, window_y = args
    tmp = np.ctypeslib.as_array(shared_array)

    for idx_x in range(window_x, window_x + block_size):
        for idx_y in range(window_y, window_y + block_size):
            print 'idx_x:{} idx_y:{}'.format(idx_x,idx_y)
            tmp[idx_x, idx_y] = X[idx_x, idx_y]

window_idxs = [(i,j) for i,j in itertools.product(range(0,size,block_size), range(0,size,block_size))]

p = Pool()
res = p.map(fill_per_window, window_idxs)
result = np.ctypeslib.as_array(shared_array)

print(np.array_equal(X, result))
