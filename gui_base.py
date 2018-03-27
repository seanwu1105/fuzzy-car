""" Author: Sean Wu 104502551 NCU CSIE 3B

Define the GUI: main window.
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

import control_panel
import graphic_panel

class GUIBase(QMainWindow):
    """ The base of GUI, containing the status bar and menu. """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuzzy Car")
        self.statusBar()
        self.setCentralWidget(BaseWidget())

class BaseWidget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        ctrl_panel = control_panel.ControlFrame()
        layout.addWidget(ctrl_panel)
        gr_panel = graphic_panel.GraphicFrame()
        layout.addWidget(gr_panel)

        self.setLayout(layout)
