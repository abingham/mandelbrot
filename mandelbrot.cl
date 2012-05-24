__kernel void 
mandelbrot(__global unsigned int* output,
           float xl,
           float xu,
           float yl,
           float yu,
           unsigned int rows,
           unsigned int cols,
           unsigned int max_iteration)
{
    unsigned int i, row, col, iteration;
    float x0, y0, x, y, xtemp;

    i = get_global_id(0);
    row = i / cols;
    col = row * cols + (i % cols);

    x0 = row / rows * (yu - yl) + yl;
    y0 = col / cols * (xu - xl) + xl;
        
    x = 0;
    y = 0;

    iteration = 0;

    while ((x*x + y*y) < 4 && (iteration < max_iteration)) {
        xtemp = x*x - y*y + x0;
        y = 2*x*y + y0;
        x = xtemp;
   
        iteration = iteration + 1;
    }
    
    output[i] = iteration;
}

// This is the algorithm using complex numbers
    /* double x0 = double(row) / size_x * (b.xu_ - b.xl_) + b.xl_; */
    /* double y0 = double(col) / size_y * (b.yu_ - b.yl_) + b.yl_; */
    
    /* // assert(x_lbound  <= x0 <= x_ubound) */
    /* // assert y_lbound <= y0 <= y_ubound */
    
    /* std::complex<double> c(x0, y0); */
    /* std::complex<double> z(0,0); */
    
    /* size_t iteration = 0; */
    /* size_t max_iteration = 1000; */
    
    /* while ((abs(z) < 2) && (iteration < max_iteration)) */
    /*     { */
    /*         z = z * z + c; */
    /*         iteration = iteration + 1; */
    /*     } */
    
    /* *static_cast<unsigned int*>(PyArray_GETPTR2(arr, row, col)) = iteration; */
