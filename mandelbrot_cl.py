import numpy as np
import pyopencl as cl

def load_program(ctx):
    with open('mandelbrot.cl', 'r') as f:
        return cl.Program(ctx, f.read()).build()

def mandelbrot(arr,
               x_lbound,
               x_ubound,
               y_lbound,
               y_ubound,
               max_iteration):
    size_x = arr.shape[0]
    size_y = arr.shape[1]

    ctx = cl.create_some_context()

    program = load_program(ctx)

    queue = cl.CommandQueue(ctx)

    dest_buf = cl.Buffer(
        ctx,
        cl.mem_flags.WRITE_ONLY,
        size_x * size_y * 4)

    new_arr = np.zeros(shape=(size_x * size_y,), dtype=np.float32)

    program.mandelbrot(
        queue,
        new_arr.shape,
        None,
        dest_buf,
        np.float32(x_lbound),
        np.float32(x_ubound),
        np.float32(y_lbound),
        np.float32(y_ubound),
        np.uint32(size_y),
        np.uint32(size_x),
        np.uint32(max_iteration))

    cl.enqueue_read_buffer(
        queue,
        dest_buf,
        new_arr).wait()

    arr[:][:] = new_arr.reshape((size_x, size_y))
    return new_arr

def test():
    arr = np.empty((100,100), dtype=np.uint32)

    mandelbrot(arr,
               -2.5,
               3.5,
               -1.0,
               2.0,
               1000)

if __name__ == '__main__':
    print('Testing load of mandelbrot opencl program')
    test()
