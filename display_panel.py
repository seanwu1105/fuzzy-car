""" Define the contents of graphic panel. """

import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFormLayout, QVBoxLayout, QGroupBox,
                             QFrame, QLabel, QSizePolicy)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle


class DisplayFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__setGraphicUI()
        self.__setVariableDisplayUI()

    def __setGraphicUI(self):
        self.simulator = CarPlot()
        self.__layout.addWidget(self.simulator)

    def __setVariableDisplayUI(self):
        group_box = QGroupBox("Monitor")
        self.__layout.addWidget(group_box)
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.car_position = QLabel("(0, 0)")
        self.car_angle = QLabel("0")
        self.wheel_angle = QLabel("0")
        self.dist_front = QLabel("0")
        self.dist_left = QLabel("0")
        self.dist_right = QLabel("0")

        self.car_position.setAlignment(Qt.AlignCenter)
        self.car_angle.setAlignment(Qt.AlignCenter)
        self.wheel_angle.setAlignment(Qt.AlignCenter)
        self.dist_front.setAlignment(Qt.AlignCenter)
        self.dist_left.setAlignment(Qt.AlignCenter)
        self.dist_right.setAlignment(Qt.AlignCenter)

        inner_layout.addRow(QLabel("Car Position:"), self.car_position)
        inner_layout.addRow(QLabel("Car Angle:"), self.car_angle)
        inner_layout.addRow(QLabel("Wheel Angle:"), self.wheel_angle)
        inner_layout.addRow(QLabel("Front Distance:"), self.dist_front)
        inner_layout.addRow(QLabel("Left Distance:"), self.dist_left)
        inner_layout.addRow(QLabel("Right Distance:"), self.dist_right)

    def paint_map(self, data):
        self.simulator.paint_map(data)

    def paint_car(self, pos, angle):
        self.simulator.paint_car(pos, angle)


class CarPlot(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self):
        fig = Figure(figsize=(5, 5), dpi=100)
        self.axes = fig.add_subplot(111, aspect='equal')

        super().__init__(fig)

        self.setMinimumWidth(550)
        self.setMinimumHeight(550)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.__car = None
        self.__direction = None

    def paint_map(self, data):
        self.axes.cla()
        self.axes.plot(*zip(*data['route_edge']), color='saddlebrown')
        self.paint_car(data['start_pos'], data['start_angle'])

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
                                           length_includes_head=True)
        self.draw()
