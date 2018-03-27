""" Author: Sean Wu 104502551 NCU CSIE 3B

An assignment of Neural Network in NCU, Taiwan
to implement the very simple fuzzy system with a car simulation.

This file is the entry point of whole project.

GitLab: https://gitlab.com/GLaDOS1105/fuzzy-car

"""

import sys

from PyQt5.QtWidgets import QApplication

import gui_base

def main():
    """ Create GUI application. """

    app = QApplication(sys.argv)
    window = gui_base.GUIBase()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
