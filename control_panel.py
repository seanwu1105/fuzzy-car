""" Define the contents of control panel. """

from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QFormLayout, QComboBox, QDoubleSpinBox, QGroupBox,
                             QLabel, QLineEdit, QRadioButton,
                             QTextEdit)

from fuzzier_viewer import FuzzierViewer


class ControlFrame(QFrame):

    def __init__(self):
        super().__init__()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.setCaseComboboxUI()
        self.setFuzzySetOperationTypeUI()
        self.setFuzzyVariableUI()
        self.setConsoleDisplay()

    def setCaseComboboxUI(self):
        group_box = QGroupBox("Case Data Selection")
        inner_layout = QGridLayout()
        group_box.setLayout(inner_layout)

        self.data_selector = QComboBox(group_box)
        self.data_selector.addItems(["pseudocase0", "pseudocase"])
        self.data_selector.setStatusTip("Select the road map data.")
        inner_layout.addWidget(self.data_selector)

        self.__layout.addWidget(group_box)

    def setFuzzySetOperationTypeUI(self):
        group_box = QGroupBox("Fuzzy Sets Operation Types")
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.composition_tnorm_selection = RadioButtonSet({
            "tn_min": QRadioButton("Minimum"),
            "tn_ap": QRadioButton("Algebraic Product"),
            "tn_bp": QRadioButton("Bounded Product"),
            "tn_dp": QRadioButton("Drastic Product")
        })
        self.composition_tconorm_selection = RadioButtonSet({
            "tc_max": QRadioButton("Maximum"),
            "tc_as": QRadioButton("Algebraic Sum"),
            "tc_bs": QRadioButton("Bounded Sum"),
            "tc_ds": QRadioButton("Drastic Sum")
        })
        self.implication_selections = RadioButtonSet({
            "imp_dr": QRadioButton("Dienes-Rescher"),
            "imp_l": QRadioButton("Lukasieweicz"),
            "imp_z": QRadioButton("Zadel"),
            "imp_g": QRadioButton("Godel"),
            "imp_m": QRadioButton("Mamdani"),
            "imp_p": QRadioButton("Product")
        })
        self.vars_combine_selection = RadioButtonSet({
            "tn_min": QRadioButton("Minimum"),
            "tn_ap": QRadioButton("Algebraic Product"),
            "tn_bp": QRadioButton("Bounded Product"),
            "tn_dp": QRadioButton("Drastic Product")
        })
        self.rules_combine_selection = RadioButtonSet({
            "tc_max": QRadioButton("Maximum"),
            "tc_as": QRadioButton("Algebraic Sum"),
            "tc_bs": QRadioButton("Bounded Sum"),
            "tc_ds": QRadioButton("Drastic Sum")
        })

        self.composition_tnorm_selection.setStatusTip("Choose the method of "
                                                      "t-norm for fuzzy "
                                                      "composition.")
        self.composition_tconorm_selection.setStatusTip("Choose the method of "
                                                        "t-conorm for fuzzy "
                                                        "composition.")
        self.implication_selections.setStatusTip("Choose the methods for fuzzy "
                                                 "implication.")
        self.vars_combine_selection.setStatusTip("Choose the methods of "
                                                 "combination of multiple fuzzy "
                                                 "variables.")
        self.rules_combine_selection.setStatusTip("Choose the methods of "
                                                  "combination of multiple fuzzy "
                                                  "rules.")

        inner_layout.addRow(QLabel("Composition T-Norm:"),
                            self.composition_tnorm_selection)
        inner_layout.addRow(QLabel("Composition T-Conorm:"),
                            self.composition_tconorm_selection)
        inner_layout.addRow(QLabel("Implication:"),
                            self.implication_selections)
        inner_layout.addRow(QLabel("Combination of Variables:"),
                            self.vars_combine_selection)
        inner_layout.addRow(QLabel("Combination of Rules:"),
                            self.rules_combine_selection)

        self.__layout.addWidget(group_box)

    def setFuzzyVariableUI(self):
        self.in_fuzzyvar_setting = FuzzierVarSetting("Input Fuzzy Variables")
        self.out_fuzzyvar_setting = FuzzierVarSetting("Output Fuzzy Varaibles")
        self.__layout.addWidget(self.in_fuzzyvar_setting)
        self.__layout.addWidget(self.out_fuzzyvar_setting)

    def setConsoleDisplay(self):
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.__layout.addWidget(self.console)

class RadioButtonSet(QFrame):
    def __init__(self, named_radiobtns):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.named_radiobtns = named_radiobtns
        next(iter(self.named_radiobtns.values())).toggle()
        for radiobtn in self.named_radiobtns.values():
            layout.addWidget(radiobtn)

class FuzzierVarSetting(QGroupBox):
    def __init__(self, name):
        super().__init__(name)
        self.__layout = QFormLayout()
        self.setLayout(self.__layout)

        self.small = GaussianFuzzierSetting()
        self.medium = GaussianFuzzierSetting()
        self.large = GaussianFuzzierSetting()

        self.__layout.addRow(QLabel("Small:"), self.small)
        self.__layout.addRow(QLabel("Medium:"), self.medium)
        self.__layout.addRow(QLabel("Large:"), self.large)

        self.viewer = FuzzierViewer()

        self.__layout.addRow(self.viewer)

        self.update_viewer()

        self.small.mean.valueChanged.connect(self.update_viewer)
        self.small.sd.valueChanged.connect(self.update_viewer)
        self.medium.mean.valueChanged.connect(self.update_viewer)
        self.medium.sd.valueChanged.connect(self.update_viewer)
        self.large.mean.valueChanged.connect(self.update_viewer)
        self.large.sd.valueChanged.connect(self.update_viewer)

    def update_viewer(self):
        means = [self.small.mean.value(),
                 self.medium.mean.value(),
                 self.large.mean.value()]
        sds = [self.small.sd.value(),
               self.medium.sd.value(),
               self.large.sd.value()]
        self.viewer.remove_curves()
        self.viewer.add_curves(means, sds)

class GaussianFuzzierSetting(QFrame):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.mean = QDoubleSpinBox()
        self.mean.setMinimum(-100)
        self.mean.setStatusTip("The mean (mu) value for Gaussian function.")
        self.sd = QDoubleSpinBox()
        self.sd.setDecimals(3)
        self.sd.setValue(1)
        self.sd.setMinimum(0.001)
        self.sd.setStatusTip("The standard deviation (sigma) value for "
                             "Gaussian function.")
        layout.addWidget(QLabel("Mean"))
        layout.addWidget(self.mean)
        layout.addWidget(QLabel("Standard Deviation"))
        layout.addWidget(self.sd)
