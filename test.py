from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton

import sys


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.form_widget = FormWidget(self)
        self.statusBar()
        self.setCentralWidget(self.form_widget)


class FormWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.button1 = QPushButton("Button 1")
        self.button1.setStatusTip("The button 1")
        self.layout.addWidget(self.button1)

        self.button2 = QPushButton("Button 2")
        self.layout.addWidget(self.button2)

        self.setLayout(self.layout)


app = QApplication([])
foo = MyMainWindow()
foo.show()
sys.exit(app.exec_())
