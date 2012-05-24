import numpy as np
import pyopencl as cl

the_program = '''
__kernel void foo(__global float* y)
{
  // y[0] = x;
}
'''

def run():
    ctx = cl.create_some_context()

    program = cl.Program(ctx, the_program).build()

    queue = cl.CommandQueue(ctx)

    dest_buf = cl.Buffer(
        ctx,
        cl.mem_flags.WRITE_ONLY,
        4)

    program.foo(queue, (1,), None, dest_buf)

    arr = np.empty((1,), np.float32)
    cl.enqueue_read_buffer(
        queue,
        dest_buf,
        arr)

    print(arr[0])

if __name__ == '__main__':
    run()
