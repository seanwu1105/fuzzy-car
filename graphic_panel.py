""" Define the contents of graphic panel. """

import math

import numpy as np

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGroupBox
from PyQt5.QtChart import QChart, QChartView, QLineSeries


class GraphicFrame(QFrame):

    def __init__(self):
        super().__init__()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.setContentsMargins(0, 0, 0, 0)

        mu, sig = 0, 3
        series = QLineSeries()

        series.append([QPointF(x, gaussian(x, mu, sig)) for x in np.linspace(mu - 4 * sig, mu + 4 * sig, 200)])

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setMinimumWidth(500)
        chart.setMaximumHeight(500)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStatusTip("Shows the simulation of fuzzy-automated car.")

        self.__layout.addWidget(chart_view)

        self.setVariableDisplay()

    def setVariableDisplay(self):
        group_box = QGroupBox("Monitor")
        self.__layout.addWidget(group_box)

def gaussian(x, mu, sig):
    return math.exp(-(x - mu)**2 / sig**2)
