""" Define the contents of graphic panel. """


from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QFormLayout, QVBoxLayout, QGroupBox, QFrame, QLabel

from .plot import CarPlot


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
        self.simulator.setStatusTip("Show the graphic of the car controled by "
                                    "fuzzy system in mazz.")
        self.__layout.addWidget(self.simulator)

    def __setVariableDisplayUI(self):
        group_box = QGroupBox("Monitor")
        self.__layout.addWidget(group_box)
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.car_position = QLabel("(0, 0)")
        self.car_angle = QLabel("0")
        self.wheel_angle = QLabel("0.0")
        self.dist_front = QLabel("--")
        self.dist_left = QLabel("--")
        self.dist_right = QLabel("--")
        self.dist_lrdiff = QLabel("--")

        self.car_position.setAlignment(Qt.AlignCenter)
        self.car_angle.setAlignment(Qt.AlignCenter)
        self.wheel_angle.setAlignment(Qt.AlignCenter)
        self.dist_front.setAlignment(Qt.AlignCenter)
        self.dist_left.setAlignment(Qt.AlignCenter)
        self.dist_right.setAlignment(Qt.AlignCenter)
        self.dist_lrdiff.setAlignment(Qt.AlignCenter)

        self.car_angle_label = QLabel("Car Angle:")
        self.wheel_angle_label = QLabel("Wheel Angle:")
        self.car_angle_label.setStatusTip("The angle (degree) of car between "
                                          "x-axis.")
        self.wheel_angle_label.setStatusTip("The angle (degree) of the wheel "
                                            "of car between x-axis, which "
                                            "will determine the next position "
                                            "of the car.")

        inner_layout.addRow(QLabel("Car Position:"), self.car_position)
        inner_layout.addRow(self.car_angle_label, self.car_angle)
        inner_layout.addRow(self.wheel_angle_label, self.wheel_angle)
        inner_layout.addRow(QLabel("Front Distance:"), self.dist_front)
        inner_layout.addRow(QLabel("Left Distance:"), self.dist_left)
        inner_layout.addRow(QLabel("Right Distance:"), self.dist_right)
        inner_layout.addRow(
            QLabel("(Left - Right) Distance:"), self.dist_lrdiff)

    @Slot(dict)
    def change_map(self, data):
        self.simulator.paint_map(data)
        self.move_car(data['start_pos'], data['start_angle'])
        self.show_dists(data['start_pos'], [data['start_pos']] * 3, ['--'] * 3)

    @Slot(list, float, float)
    def move_car(self, pos, angle, wheel_angle=0.0):
        self.simulator.paint_car(pos, angle)
        self.car_position.setText("({:.7f}, {:.7f})".format(*pos))
        self.car_angle.setText(str(angle))
        self.wheel_angle.setText(str(wheel_angle))

    @Slot(list, list, list)
    def show_dists(self, pos, intersections, dists):
        self.simulator.paint_dist(pos, intersections)
        self.dist_front.setText(str(dists[0]))
        self.dist_left.setText(str(dists[1]))
        self.dist_right.setText(str(dists[2]))
        try:
            lrdiff = float(dists[1]) - float(dists[2])
        except ValueError:
            self.dist_lrdiff.setText('--')
        else:
            self.dist_lrdiff.setText(str(lrdiff))

    @Slot()
    def show_car_collided(self):
        self.simulator.paint_car_collided()

    def show_path(self, xdata, ydata):
        self.simulator.paint_path(xdata, ydata)
