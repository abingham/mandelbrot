import numpy as np
cimport numpy as np
DTYPE = np.uint8
ctypedef np.uint8_t DTYPE_t

def mandelbrot(int size_x, int size_y):
    cdef int row, col, iteration, max_iteration, color
    cdef float x0, y0

    # These define the bounds of the complex plan in which we're
    # interested.  
    # max reasonable x bounds: (-2.5 to 1)
    cdef float x_lbound = -2.5
    cdef float x_ubound = 1.0

    # max reasonable y bounds: (-1, 1)
    cdef float y_lbound = -1.0
    cdef float y_ubound = 1.0

    cdef np.ndarray[DTYPE_t, ndim=3] arr = np.zeros(
        dtype=DTYPE, 
        shape=(size_x, size_y, 3))

    # This is what we're iterating over
    # z[n+1] = z[n]^2 + c

    # For each pixel
    for row in range(size_x):
        for col in range(size_y):
            # scale pixels to a point in the area of the complex plane
            # in which we're looking.
            x0 = float(row) / size_x * (x_ubound - x_lbound) + x_lbound
            y0 = float(col) / size_y * (y_ubound - y_lbound) + y_lbound

            #assert x_lbound  <= x0 <= x_ubound
            #assert y_lbound <= y0 <= y_ubound

            c = complex(x0, y0)
            z = complex(0,0)
            
            iteration = 0
            max_iteration = 1000
            
            while (abs(z) < 2) and (iteration < max_iteration):
                z = z * z + c
                iteration = iteration + 1
            
            color = iteration % 255
            #print(iteration, color)
            arr[row, col, 0] = color
            arr[row, col, 1] = (color + 75) % 255
            arr[row, col, 2] = (color + 150) % 255

    return arr
