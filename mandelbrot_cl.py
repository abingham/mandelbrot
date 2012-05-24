def mandelbrot(arr,
               x_lbound,
               x_ubound,
               y_lbound,
               y_ubound,
               max_iteration):
    size_x = arr.shape[0]
    size_y = arr.shape[1]
    
    for row in range(arr.shape[0]):
        for col in range