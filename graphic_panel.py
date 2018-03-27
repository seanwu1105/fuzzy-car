""" Define the contents of graphic panel. """

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries

class GraphicFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        series = QLineSeries()

        series.append(0, 6)
        series.append(2, 7)
        series.append(3, 5)
        series.append(7, 3)
        series.append(9, 0)
        series.append(50, 8)
        series.append(13, 7)
        series.append(-1, 5)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumSize(400, 400)

        layout.addWidget(chart_view)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
