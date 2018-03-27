import sys

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QChartView, QLineSeries, QChart

def main():
    a = QApplication(sys.argv)
    series = QLineSeries()
    series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6)

    chart = QChart()
    chart.legend().hide()
    chart.addSeries(series)
    chart.createDefaultAxes()
    chart.setTitle("FUCK!")

    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(400, 300)
    window.show()

    a.exec_()

if __name__ == '__main__':
    main()