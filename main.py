""" Author: Sean Wu 104502551 NCU CSIE 3B

An assignment of Neural Network in NCU, Taiwan
to implement the very simple fuzzy system with a car simulation.

This file is the entry point of whole project.

GitLab: https://gitlab.com/GLaDOS1105/fuzzy-car

"""

import collections
import pathlib
import sys

from PyQt5.QtWidgets import QApplication

import gui_base


def main():
    """ Create GUI application and read testing case data. """

    app = QApplication(sys.argv)
    window = gui_base.GUIBase(read_case_file())
    window.show()
    sys.exit(app.exec_())


def read_case_file(folderpath='data'):
    """ Read every data of testing case in "folderpath" folder. Return the
    dictionary containing dataset.
    """
    dataset = {}
    folderpath = pathlib.Path(folderpath)
    for filepath in folderpath.glob("*.txt"):
        with filepath.open() as casefile:
            contents = [tuple(map(float, line.split(',')))
                        for line in casefile]
        dataset[filepath.stem] = {
            "start_pos": (contents[0][0], contents[0][1]),
            "start_angle": contents[0][2],
            "end_area_lt": contents[1],  # ending area - left-top
            "end_area_rb": contents[2],  # ending area - right-bottom
            "route_edge": contents[3:]
        }
    return collections.OrderedDict(sorted(dataset.items()))


if __name__ == '__main__':
    main()
