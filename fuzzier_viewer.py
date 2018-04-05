import math

import numpy as np
from PyQt5.QtCore import QPointF, QMargins
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries


class FuzzierViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(55)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setStatusTip("Display the fuzziers in plot.")

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.createDefaultAxes()
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setMargins(QMargins())
        self.chart.setBackgroundRoundness(0)
        

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)
        layout.setContentsMargins(0, 0, 0, 0)

    def add_curves(self, means, sds, ascendings, descendings):
        self.__xmax = max(means) + 4 * sds[means.index(max(means))]
        self.__xmin = min(means) - 4 * sds[means.index(min(means))]
        series_list = [QLineSeries() for _ in range(len(means))]
        for idx, param in enumerate(zip(means, sds, ascendings, descendings)):
            series_list[idx].append(self.__generate_curve(*param))
            self.chart.addSeries(series_list[idx])
        self.chart.createDefaultAxes()
        self.chart.removeAxis(self.chart.axisY())

    def remove_curves(self):
        self.chart.removeAllSeries()

    def __generate_curve(self, mean, sd, ascending, descending):
        if ascending and descending:
            return [QPointF(x, 0) for x in np.linspace(self.__xmin,
                                                       self.__xmax,
                                                       10)]
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
