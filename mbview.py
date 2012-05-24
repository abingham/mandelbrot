from enthought.traits.api import HasTraits, Instance, Float
from enthought.traits.ui.api import Group, Item, View
from enthought.chaco.api import Plot, ArrayPlotData, jet
from enthought.enable.component_editor import ComponentEditor

import numpy
from numpy import linspace, sin

from mandelbrot_bp import mandelbrot

class LinePlot(HasTraits):
    plot = Instance(Plot)

    x_lbound = Float(-2.5)
    x_ubound = Float(1)
    y_lbound = Float(-1)
    y_ubound = Float(1)

    traits_view = View(
        Item('plot',editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Chaco Plot")

    traits_view = View(
        Group(Item('x_lbound', label="X lower bound"),
              Item('x_ubound', label="X upper bound"),
              Item('y_lbound', label="Y lower bound"),
              Item('y_ubound', label="Y upper bound"),
              Item('plot', editor=ComponentEditor(), show_label=False),
                   orientation = "vertical"),
              width=800, height=600, resizable=True, title="Chaco Plot")

    def __init__(self):
        super(LinePlot, self).__init__()

        self.size_x = 800
        self.size_y = 600
        self.num_threads = 2

        arr = numpy.zeros(dtype=numpy.uint32, shape=(self.size_x, self.size_y))
        rslt = mandelbrot(
            arr,
            self.x_lbound,
            self.x_ubound,
            self.y_lbound,
            self.y_ubound,
            1000,
            self.num_threads)

        self.plotdata = ArrayPlotData(imagedata=self._get_image())

        plot = Plot(self.plotdata)
        plot.img_plot("imagedata", colormap=jet)

        self.plot = plot

    def _get_image(self):
        arr = numpy.zeros(
            dtype=numpy.uint32, 
            shape=(self.size_x, self.size_y))

        rslt = mandelbrot(
            arr,
            self.x_lbound,
            self.x_ubound,
            self.y_lbound,
            self.y_ubound,
            1000,
            self.num_threads)

        return arr

    def _rerender(self):
        self.plotdata.set_data(
            "imagedata",
            self._get_image())

    def _x_lbound_changed(self):
        self._rerender()

    def _x_ubound_changed(self):
        self._rerender()

    def _y_lbound_changed(self):
        self._rerender()

    def _y_ubound_changed(self):
        self._rerender()

if __name__ == "__main__":
    LinePlot().configure_traits()
