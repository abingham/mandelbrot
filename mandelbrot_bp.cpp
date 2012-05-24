#include <Python.h>

#include <complex>

#include <boost/bind.hpp>
#include <boost/python.hpp>
#include <boost/thread/thread.hpp>

#include <numpy/arrayobject.h>

struct Bounds
{
    double xl_, xu_, yl_, yu_;

    Bounds(double xl, double xu, double yl, double yu) :
        xl_ (xl),
        xu_ (xu),
        yl_ (yl),
        yu_ (yu)
        {}
};

void mandelbrot_section(
    PyArrayObject* arr,
    const Bounds& b,
    size_t max_iteration,
    size_t row_start,
    size_t num_rows,
    size_t col_start,
    size_t num_cols)
{
    npy_intp * dims = PyArray_DIMS(arr);
    npy_intp size_x = dims[0];
    npy_intp size_y = dims[1];

    for (size_t row = row_start; row < row_start + num_rows; ++row)
    {
        for (size_t col = col_start; col < col_start+ num_cols; ++col)
        {
            double x0 = double(row) / size_x * (b.xu_ - b.xl_) + b.xl_;
            double y0 = double(col) / size_y * (b.yu_ - b.yl_) + b.yl_;

            // assert(x_lbound  <= x0 <= x_ubound)
            // assert y_lbound <= y0 <= y_ubound

            std::complex<double> c(x0, y0);
            std::complex<double> z(0,0);
            
            size_t iteration = 0;
            size_t max_iteration = 1000;
            
            while ((abs(z) < 2) && (iteration < max_iteration))
            {
                z = z * z + c;
                iteration = iteration + 1;
            }

            *static_cast<unsigned int*>(PyArray_GETPTR2(arr, row, col)) = iteration;
        }
    }
    
}

int mandelbrot(boost::python::object obj,
               double x_lbound,
               double x_ubound,
               double y_lbound,
               double y_ubound,
               size_t max_iteration,
               size_t num_threads)
{
    PyArrayObject* arr = reinterpret_cast<PyArrayObject*>(
        obj.ptr());

    if (!arr) return 0;

    npy_intp * dims = PyArray_DIMS(arr);

    // TODO: check dimensionality...
    // TODO: check datatype...npy_unit8? I think so.

    npy_intp size_x = dims[0];
    npy_intp size_y = dims[1];

    boost::thread_group threads;

    Bounds b(x_lbound,
             x_ubound,
             y_lbound,
             y_ubound);

    for (size_t i = 0; i < num_threads; ++i)
    {
        threads.create_thread(
            boost::bind(
                &mandelbrot_section,
                arr,
                b,
                max_iteration,
                size_x / num_threads * i, // TODO: make this more correct.
                size_x / num_threads,
                0,
                size_y));
    }
    threads.join_all();
                

    return 1;
}

BOOST_PYTHON_MODULE(mandelbrot_bp)
{
    def("mandelbrot", &mandelbrot);
}
