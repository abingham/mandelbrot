all:
	g++ -O3 -I/usr/include/python2.7 -shared -fPIC -lboost_python -lboost_thread -o mandelbrot_bp.so mandelbrot_bp.cpp