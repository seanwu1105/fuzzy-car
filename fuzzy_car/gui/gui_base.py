""" Author: Sean Wu 104502551 NCU CSIE 3B

Define the GUI: main window.
"""

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from .control_panel import ControlFrame
from .display_panel import DisplayFrame


class GUIBase(QMainWindow):
    """ The base of GUI, containing the status bar and menu. """

    def __init__(self, dataset):
        super().__init__()
        self.setWindowTitle("It is So Fuzzy")
        self.statusBar()

        # a container for threads created in GUI classes.
        # For more details:
        # https://stackoverflow.com/questions/28714630/qthread-destroyed-while-thread-is-still-running-on-quit
        self.threads = []

        self.setCentralWidget(BaseWidget(dataset, self.threads))

    def closeEvent(self, _):
        """ Stop the new created threads and wait till them terminate. """
        for thread in self.threads:
            thread.stop()
            thread.wait()


class BaseWidget(QWidget):

    def __init__(self, dataset, threads):
        super().__init__()
        layout = QHBoxLayout()
        disp_panel = DisplayFrame()
        ctrl_panel = ControlFrame(dataset, disp_panel, threads)
        layout.addWidget(ctrl_panel)
        layout.addWidget(disp_panel)

        self.setLayout(layout)
