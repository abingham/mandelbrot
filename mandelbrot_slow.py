def slow_mandelbrot(size_x, size_y):
    arr = numpy.zeros(dtype=numpy.int8, shape=(size_x, size_y, 3))

    for row in range(size_x):
        for col in range(size_y):
    #         if row == col:
    #             arr[row, col, 0] = 255
    # return arr
            
    # for x in []:        
            x0 = float(row) / size_x * 3.5 - 2.5
            y0 = float(col) / size_y * 2.0 - 1.0

            assert -2.5 <= x0 <= 1
            assert -1 <= y0 <= 1

            x = 0
            y = 0

            iteration = 0
            max_iteration = 1000

            while (x*x + y*y) < 4 and (iteration < max_iteration):
                xtemp = x*x - y*y + x0
                y = 2*x*y + y0
                x = xtemp
   
                iteration = iteration + 1
            
            color = iteration % 255
            #print(iteration, color)
            arr[row, col, 0] = color
            arr[row, col, 1] = (color + 75) % 255
            arr[row, col, 2] = (color + 150) % 255
    return arr
