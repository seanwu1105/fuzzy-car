""" Author: Sean Wu 104502551 NCU CSIE 3B

Define the GUI: main window.
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from control_panel import ControlFrame
from display_panel import DisplayFrame

class GUIBase(QMainWindow):
    """ The base of GUI, containing the status bar and menu. """

    def __init__(self, dataset):
        super().__init__()
        self.setWindowTitle("IT'S SO FUZZY")
        self.statusBar()
        self.setCentralWidget(BaseWidget(dataset))

class BaseWidget(QWidget):

    def __init__(self, dataset):
        super().__init__()
        layout = QHBoxLayout()
        disp_panel = DisplayFrame()
        ctrl_panel = ControlFrame(dataset, disp_panel)
        layout.addWidget(ctrl_panel)
        layout.addWidget(disp_panel)

        self.setLayout(layout)
