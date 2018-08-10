"""Define the previewer for the fuzzier variables, implemented with QtChart."""

import math

import numpy as np
from PySide2.QtCore import QPointF, QMargins
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QFrame, QHBoxLayout
from PySide2.QtCharts import QtCharts


class FuzzierViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(60)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setStatusTip("Display the fuzziers in plot.")

        self.chart = QtCharts.QChart()
        self.chart.legend().hide()
        self.chart.createDefaultAxes()
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setMargins(QMargins())
        self.chart.setBackgroundRoundness(2)

        chart_view = QtCharts.QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)
        layout.setContentsMargins(0, 0, 0, 0)

    def add_curves(self, means, sds, ascendings, descendings):
        self.__xmax = max(means) + 2 * sds[means.index(max(means))]
        self.__xmin = min(means) - 2 * sds[means.index(min(means))]
        series_list = [QtCharts.QLineSeries() for _ in range(len(means))]
        for idx, param in enumerate(zip(means, sds, ascendings, descendings)):
            series_list[idx].append(self.__generate_curve(*param))
            self.chart.addSeries(series_list[idx])
        self.chart.createDefaultAxes()
        self.chart.axisX().setTickCount(11)
        self.chart.removeAxis(self.chart.axisY())

    def remove_curves(self):
        self.chart.removeAllSeries()

    def __generate_curve(self, mean, sd, ascending, descending):
        if ascending and descending:
            return [QPointF(x, 0) for x in np.linspace(self.__xmin,
                                                       self.__xmax,
                                                       10,
                                                       endpoint=True)]
        points = list()
        for x in np.linspace(self.__xmin, self.__xmax, 400):
            if ascending and x > mean:
                points.append(QPointF(x, 1))
            elif descending and x < mean:
                points.append(QPointF(x, 1))
            else:
                points.append(QPointF(x, gaussian(x, mean, sd)))
        return points


def gaussian(var, mean, sig):
    return math.exp(-(var - mean)**2 / sig**2)
