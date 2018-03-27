""" Define the contents of control panel. """

from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QFormLayout, QComboBox, QGroupBox, QRadioButton,
                             QLabel, QPushButton)


class ControlFrame(QFrame):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setCaseComboboxUI()
        self.setCompositionTypeUI()
        self.setRuleTypeUI()

    def setCaseComboboxUI(self):
        group_box = QGroupBox("Case Data Selection")
        inner_layout = QGridLayout()
        group_box.setLayout(inner_layout)

        self.data_selector = QComboBox(group_box)
        self.data_selector.addItems(["pseudocase0", "pseudocase"])
        inner_layout.addWidget(self.data_selector)

        self.layout.addWidget(group_box)

    def setCompositionTypeUI(self):
        group_box = QGroupBox("Composition Type")
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.composition_tn_type = TNormsSelections()
        self.composition_tc_type = TConormsSelections()
        inner_layout.addRow(QLabel("T-Norm: "), self.composition_tn_type)
        inner_layout.addRow(QLabel("T-Conorm: "), self.composition_tc_type)

        self.layout.addWidget(group_box)

    def setRuleTypeUI(self):
        group_box = QGroupBox("Rule Type")
        inner_layout = QHBoxLayout()
        group_box.setLayout(inner_layout)

        rules_rb = {
            "rule_dr": QRadioButton("Dienes-Rescher"),
            "rule_l": QRadioButton("Lukasieweicz"),
            "rule_z": QRadioButton("Zadel"),
            "rule_g": QRadioButton("Godel"),
            "rule_m": QRadioButton("Mamdani"),
            "rule_p": QRadioButton("Product")
        }

        for widget in rules_rb.values():
            inner_layout.addWidget(widget)

        self.layout.addWidget(group_box)


class FuzzyTSelections(QFrame):
    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)


class TNormsSelections(FuzzyTSelections):

    def __init__(self):
        super().__init__()
        tnorms_rb = {
            "tn_min": QRadioButton("Minimum"),
            "tn_ap": QRadioButton("Algebraic Product"),
            "tn_bp": QRadioButton("Bounded Product"),
            "tn_dp": QRadioButton("Drastic Product")
        }
        for widget in tnorms_rb.values():
            self._layout.addWidget(widget)


class TConormsSelections(FuzzyTSelections):

    def __init__(self):
        super().__init__()
        tconorms_rb = {
            "tc_max": QRadioButton("Maximum"),
            "tc_as": QRadioButton("Algebraic Sum"),
            "tc_bs": QRadioButton("Bounded Sum"),
            "tc_ds": QRadioButton("Drastic Sum")
        }
        for widget in tconorms_rb.values():
            self._layout.addWidget(widget)
