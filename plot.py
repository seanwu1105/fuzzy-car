import math

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Rectangle

from PyQt5.QtWidgets import QSizePolicy


class CarPlot(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self):
        fig = Figure(figsize=(5, 5), dpi=100)
        self.axes = fig.add_subplot(111, aspect='equal')

        super().__init__(fig)

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.__car = None
        self.__direction = None
        self.__dists = []

    def paint_map(self, data):
        self.axes.cla()
        self.axes.plot(*zip(*data['route_edge']), color='darkslategray')
        self.axes.add_artist(Rectangle(
            (data['end_area_lt'][0], data['end_area_rb'][1]),
            data['end_area_rb'][0] - data['end_area_lt'][0],
            data['end_area_lt'][1] - data['end_area_rb'][1],
            color='greenyellow'))

    def paint_car(self, pos, angle):
        try:
            self.__car.remove()
            self.__direction.remove()
        except (AttributeError, ValueError):
            pass
        self.__car = Circle(pos, radius=3, color='dodgerblue')
        self.axes.add_artist(self.__car)

        arrow_len = 5
        angle = math.radians(angle)
        self.__direction = self.axes.arrow(*pos,
                                           arrow_len * math.cos(angle),
                                           arrow_len * math.sin(angle),
                                           head_width=2,
                                           length_includes_head=True,
                                           fc='seagreen',
                                           ec='darkslategray')
        self.draw()

    def paint_car_collided(self):
        self.__car.set_color('tomato')
        self.draw()

    def paint_dist(self, pos, intersections):
        for dist in self.__dists:
            try:
                dist.remove()
            except ValueError:
                pass

        self.__dists = [Line2D(*zip(pos, i),
                               linestyle=':',
                               color='grey') for i in intersections if i is not None]
        for dist in self.__dists:
            self.axes.add_line(dist)
        self.draw()
