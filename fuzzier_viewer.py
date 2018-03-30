import math

import numpy as np
from PyQt5.QtCore import QPointF, QMargins
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QSizePolicy
from PyQt5.QtChart import QChart, QChartView, QLineSeries


class FuzzierViewer(QFrame):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setStatusTip("Display the fuzziers in plot.")

        self.max_realm = 0
        self.min_realm = 0
        self.means = None
        self.sds = None

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.createDefaultAxes()
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setMargins(QMargins())
        self.chart.setBackgroundRoundness(0)
        self.chart.setMinimumHeight(55)

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)
        layout.setContentsMargins(0, 0, 0, 0)

    def add_curves(self, means, sds):
        self.means, self.sds = means, sds
        self.max_realm = max(means) + 4 * sds[means.index(max(means))]
        self.min_realm = min(means) - 4 * sds[means.index(min(means))]
        series_list = [QLineSeries() for _ in range(len(self.means))]
        for curve in zip(series_list, self.means, self.sds):
            curve[0].append([QPointF(x, gaussian(x, curve[1], curve[2]))
                             for x in np.linspace(self.min_realm,
                                                  self.max_realm,
                                                  200)])
            self.chart.addSeries(curve[0])
        self.chart.createDefaultAxes()
        self.chart.removeAxis(self.chart.axisY())

    def remove_curves(self):
        self.chart.removeAllSeries()


def gaussian(var, mean, sig):
    return math.exp(-(var - mean)**2 / sig**2)
