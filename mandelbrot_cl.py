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
        size_x * size_y)

    program.mandelbrot(
        queue,
        size_x * size_y,
        None,
        dest_buf,
        x_lbound,
        x_ubound,
        y_lbound,
        y_ubound,
        size_y,
        size_x,
        max_iteration)

    cl.enqueue_read_buffer(
        self.queue,
        self.dest_buf,
        arr).wait()

def test():
    import numpy as np
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
