""" Define the contents of control panel. """

import collections
import itertools
import os

from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QFormLayout,
                               QComboBox, QDoubleSpinBox, QGroupBox,
                               QPushButton, QLabel, QRadioButton, QTextEdit,
                               QCheckBox, QStackedWidget, QTableWidget,
                               QTableWidgetItem, QHeaderView, QSpinBox,
                               QFileDialog)

from .display_panel import DisplayFrame
from .fuzzier_viewer import FuzzierViewer
from ..backend.fuzzy_system import (FuzzySystem, FuzzyVariable,
                                            get_gaussianf)
from ..backend.car import Car
from ..backend.run import RunCar
from . import src  # for pyinstaller to import the icons automatically


class ControlFrame(QFrame):

    def __init__(self, dataset, display_panel, threads):
        super().__init__()
        if isinstance(display_panel, DisplayFrame):
            self.display_panel = display_panel
        else:
            raise TypeError("'display_panel' must be the instance of "
                            "'DisplayFrame'")
        self.dataset = dataset
        self.threads = threads

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__set_running_options_ui()
        self.__set_fuzzy_set_operation_types_ui()
        self.__set_fuzzy_variables_ui()
        self.__set_fuzzy_rules_ui()
        self.__set_console_ui()

    def __set_running_options_ui(self):
        group_box = QGroupBox("Running Options")
        inner_layout = QHBoxLayout()
        group_box.setLayout(inner_layout)

        self.data_selector = QComboBox()
        self.data_selector.addItems(list(self.dataset.keys()))
        self.data_selector.setStatusTip("Select the road map case.")
        self.data_selector.currentIndexChanged.connect(self.__change_map)

        self.fps = QSpinBox()
        self.fps.setMinimum(1)
        self.fps.setMaximum(60)
        self.fps.setValue(20)
        self.fps.setStatusTip("The re-drawing rate for car simulator. High fps "
                              "may cause the plot shows discontinuously.")

        self.start_btn = QPushButton("Run")
        self.start_btn.setStatusTip("Run the car.")
        self.start_btn.clicked.connect(self.__run)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setStatusTip("Force the simulation stop running.")
        self.stop_btn.setDisabled(True)

        self.save_btn = QPushButton()
        self.save_btn.setIcon(QIcon(':/icons/save_icon.png'))
        self.save_btn.setStatusTip("Save every details for the last time "
                                   "running.")
        self.save_btn.clicked.connect(self.__save_results)
        self.save_btn.setDisabled(True)

        self.__change_map()
        inner_layout.addWidget(self.data_selector, 1)
        inner_layout.addWidget(QLabel("FPS:"))
        inner_layout.addWidget(self.fps)
        inner_layout.addWidget(self.start_btn)
        inner_layout.addWidget(self.stop_btn)
        inner_layout.addWidget(self.save_btn)

        self.__layout.addWidget(group_box)

    def __set_fuzzy_set_operation_types_ui(self):
        group_box = QGroupBox("Fuzzy Sets Operation Types")
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.implication_selections = RadioButtonSet([
            ("imp_dr", QRadioButton("Dienes-Rescher")),
            ("imp_l", QRadioButton("Lukasieweicz")),
            ("imp_z", QRadioButton("Zadel")),
            ("imp_g", QRadioButton("Godel")),
            ("imp_m", QRadioButton("Mamdani")),
            ("imp_p", QRadioButton("Product"))
        ])
        self.combination_vars_selections = RadioButtonSet([
            ("tn_min", QRadioButton("Minimum")),
            ("tn_ap", QRadioButton("Algebraic Product")),
            ("tn_bp", QRadioButton("Bounded Product")),
            ("tn_dp", QRadioButton("Drastic Product"))
        ])
        self.combination_rules_selections = RadioButtonSet([
            ("tc_max", QRadioButton("Maximum")),
            ("tc_as", QRadioButton("Algebraic Sum")),
            ("tc_bs", QRadioButton("Bounded Sum")),
            ("tc_ds", QRadioButton("Drastic Sum"))
        ])
        self.defuzzifier_selections = RadioButtonSet([
            ("gravity_center", QRadioButton("Center of Gravity")),
            ("maxima_mean", QRadioButton("Mean of Maxima")),
            ("modified_maxima_mean", QRadioButton("Modified Mean of Maxima"))
        ])

        self.implication_selections.set_selected('imp_m')
        self.combination_vars_selections.set_selected('tn_min')
        self.combination_rules_selections.set_selected('tc_max')
        self.defuzzifier_selections.set_selected('gravity_center')

        self.implication_selections.setStatusTip("Choose the method for fuzzy "
                                                 "implication.")
        self.combination_vars_selections.setStatusTip("Choose the method of "
                                                      "combination of multiple "
                                                      "fuzzy variables.")
        self.combination_rules_selections.setStatusTip("Choose the method of "
                                                       "combination of "
                                                       "multiple fuzzy rules.")
        self.defuzzifier_selections.setStatusTip("Choose the method for the "
                                                 "defuzifier.")

        inner_layout.addRow(QLabel("Implication:"),
                            self.implication_selections)
        inner_layout.addRow(QLabel("Combination of Variables:"),
                            self.combination_vars_selections)
        inner_layout.addRow(QLabel("Combination of Rules:"),
                            self.combination_rules_selections)
        inner_layout.addRow(QLabel("Defuzzifier:"),
                            self.defuzzifier_selections)

        self.__layout.addWidget(group_box)

    def __set_fuzzy_variables_ui(self):
        group_box = QGroupBox("Fuzzy Variables Settings")
        group_box.setStatusTip("Set the membership functions for each fuzzy "
                               "variable.")
        inner_layout = QVBoxLayout()
        self.fuzzyvar_setting_stack = QStackedWidget()
        self.fuzzyvar_ui_selection = RadioButtonSet([
            ("front", QRadioButton("Front Distance Radar")),
            ("lrdiff", QRadioButton("(Left-Right) Distance Radar")),
            ("consequence", QRadioButton("Consequence"))
        ])
        self.fuzzyvar_setting_dist_front = FuzzierVarSetting()
        self.fuzzyvar_setting_dist_front.small.mean.setValue(5)
        self.fuzzyvar_setting_dist_front.medium.mean.setValue(12)
        self.fuzzyvar_setting_dist_front.large.mean.setValue(20)

        self.fuzzyvar_setting_dist_lrdiff = FuzzierVarSetting()
        self.fuzzyvar_setting_dist_lrdiff.small.mean.setValue(-10)
        self.fuzzyvar_setting_dist_lrdiff.medium.mean.setValue(0)
        self.fuzzyvar_setting_dist_lrdiff.large.mean.setValue(10)

        self.fuzzyvar_setting_consequence = FuzzierVarSetting()
        self.fuzzyvar_setting_consequence.small.mean.setValue(-12)
        self.fuzzyvar_setting_consequence.small.sd.setValue(20)
        self.fuzzyvar_setting_consequence.medium.mean.setValue(0)
        self.fuzzyvar_setting_consequence.medium.sd.setValue(20)
        self.fuzzyvar_setting_consequence.large.mean.setValue(12)
        self.fuzzyvar_setting_consequence.large.sd.setValue(20)

        inner_layout.addWidget(self.fuzzyvar_ui_selection)
        inner_layout.addWidget(self.fuzzyvar_setting_stack)
        group_box.setLayout(inner_layout)

        self.fuzzyvar_setting_stack.addWidget(self.fuzzyvar_setting_dist_front)
        self.fuzzyvar_setting_stack.addWidget(
            self.fuzzyvar_setting_dist_lrdiff)
        self.fuzzyvar_setting_stack.addWidget(
            self.fuzzyvar_setting_consequence)

        self.fuzzyvar_ui_selection.sig_rbtn_changed.connect(
            self.__change_fuzzyvar_setting_ui_stack)

        self.__layout.addWidget(group_box)

    def __set_fuzzy_rules_ui(self):
        antecedents = ('small', 'medium', 'large')

        group_box = QGroupBox("Fuzzy Rules Setting")
        inner_layout = QVBoxLayout()
        group_box.setStatusTip("Set the rules for the fuzzy system.")

        self.rules_setting = FuzzyRulesSetting(
            [p for p in itertools.product(antecedents, repeat=2)])
        self.rules_setting.set_consequence_fuzzysets((
            'large', 'small', 'small',
            'large', 'small', 'small',
            'large', 'small', 'small'
        ))

        inner_layout.addWidget(self.rules_setting)
        group_box.setLayout(inner_layout)
        self.__layout.addWidget(group_box)

    def __set_console_ui(self):
        self.__console = QTextEdit()
        self.__console.setReadOnly(True)
        self.__console.setStatusTip("Show the logs of status changing.")
        self.__layout.addWidget(self.__console)

    @Slot(str)
    def __change_fuzzyvar_setting_ui_stack(self, name):
        if name == 'front':
            self.fuzzyvar_setting_stack.setCurrentIndex(0)
        elif name == 'lrdiff':
            self.fuzzyvar_setting_stack.setCurrentIndex(1)
        else:
            self.fuzzyvar_setting_stack.setCurrentIndex(2)

    @Slot()
    def __change_map(self):
        self.__current_data = self.dataset[self.data_selector.currentText()]
        self.__car = Car(self.__current_data['start_pos'],
                         self.__current_data['start_angle'],
                         3, self.__current_data['route_edge'])
        self.display_panel.change_map(self.__current_data)

    @Slot(str)
    def __print_console(self, text):
        self.__console.append(text)

    @Slot(list)
    def __get_results(self, results):
        """Get the results of last running and draw the path of it."""
        self.results = results
        self.display_panel.show_path([d['x'] for d in results],
                                     [d['y'] for d in results])

    @Slot()
    def __save_results(self):
        save_dir = QFileDialog.getExistingDirectory(self,
                                                    'Select Saving Directory')
        file4d_filepath = os.path.join(save_dir, 'train4D.txt')
        file6d_filepath = os.path.join(save_dir, 'train6D.txt')
        with open(file4d_filepath, 'w') as file4d:
            for result in self.results:
                file4d.write('{:.7f} {:.7f} {:.7f} {:.7f}\n'.format(
                    result['front_dist'], result['right_dist'],
                    result['left_dist'], result['wheel_angle']
                ))
        with open(file6d_filepath, 'w') as file6d:
            for result in self.results:
                file6d.write('{:.7f} {:.7f} {:.7f} {:.7f} {:.7f} {:.7f}\n'.format(
                    result['x'], result['y'],
                    result['front_dist'], result['right_dist'],
                    result['left_dist'], result['wheel_angle']
                ))
        self.__print_console('Note: Detailed results have been saved in both'
                             ' "%s" and "%s".' % (file4d_filepath, file6d_filepath))

    @Slot()
    def __init_widgets(self):
        self.start_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)
        self.save_btn.setDisabled(True)
        self.fps.setDisabled(True)
        self.data_selector.setDisabled(True)
        self.implication_selections.setDisabled(True)
        self.combination_vars_selections.setDisabled(True)
        self.combination_rules_selections.setDisabled(True)
        self.defuzzifier_selections.setDisabled(True)
        self.fuzzyvar_setting_dist_front.setDisabled(True)
        self.fuzzyvar_setting_dist_lrdiff.setDisabled(True)
        self.fuzzyvar_setting_consequence.setDisabled(True)
        self.rules_setting.setDisabled(True)

    @Slot()
    def __reset_widgets(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setDisabled(True)
        self.save_btn.setEnabled(True)
        self.fps.setEnabled(True)
        self.data_selector.setEnabled(True)
        self.implication_selections.setEnabled(True)
        self.combination_vars_selections.setEnabled(True)
        self.combination_rules_selections.setEnabled(True)
        self.defuzzifier_selections.setEnabled(True)
        self.fuzzyvar_setting_dist_front.setEnabled(True)
        self.fuzzyvar_setting_dist_lrdiff.setEnabled(True)
        self.fuzzyvar_setting_consequence.setEnabled(True)
        self.rules_setting.setEnabled(True)

    @Slot()
    def __run(self):
        # reset the map
        self.__change_map()
        # create a QThread
        self.thread = RunCar(self.__car,
                             self.__create_fuzzy_system(),
                             (self.__current_data['end_area_lt'],
                              self.__current_data['end_area_rb']),
                             self.fps.value())
        # Record the new created threads for the closeEvent in gui_base.py
        # By doing this, user can destroy the QMainWindow elegantly when there
        # are threads still running.
        self.threads.append(self.thread)
        self.stop_btn.clicked.connect(self.thread.stop)
        self.thread.started.connect(self.__init_widgets)
        self.thread.finished.connect(self.__reset_widgets)
        self.thread.sig_console.connect(self.__print_console)
        self.thread.sig_car.connect(self.display_panel.move_car)
        self.thread.sig_car_collided.connect(
            self.display_panel.show_car_collided)
        self.thread.sig_dists.connect(self.display_panel.show_dists)
        self.thread.sig_results.connect(self.__get_results)
        self.thread.start()

    def __create_fuzzy_system(self):
        """Create a fuzzy system with the parameter given in control panel."""
        dist_front = FuzzyVariable()
        dist_front.add_membershipf(
            'small', get_gaussianf(*self.fuzzyvar_setting_dist_front.small.get_values()))
        dist_front.add_membershipf(
            'medium', get_gaussianf(*self.fuzzyvar_setting_dist_front.medium.get_values()))
        dist_front.add_membershipf(
            'large', get_gaussianf(*self.fuzzyvar_setting_dist_front.large.get_values()))

        dist_lrdiff = FuzzyVariable()
        dist_lrdiff.add_membershipf(
            'small', get_gaussianf(*self.fuzzyvar_setting_dist_lrdiff.small.get_values()))
        dist_lrdiff.add_membershipf(
            'medium', get_gaussianf(*self.fuzzyvar_setting_dist_lrdiff.medium.get_values()))
        dist_lrdiff.add_membershipf(
            'large', get_gaussianf(*self.fuzzyvar_setting_dist_lrdiff.large.get_values()))

        consequence = FuzzyVariable()
        consequence.add_membershipf(
            'small', get_gaussianf(*self.fuzzyvar_setting_consequence.small.get_values()))
        consequence.add_membershipf(
            'medium', get_gaussianf(*self.fuzzyvar_setting_consequence.medium.get_values()))
        consequence.add_membershipf(
            'large', get_gaussianf(*self.fuzzyvar_setting_consequence.large.get_values()))

        fuzzy_system = FuzzySystem(consequence, dist_front, dist_lrdiff)
        fuzzy_system.set_operation_types(
            self.implication_selections.get_selected_name(),
            self.combination_vars_selections.get_selected_name(),
            self.combination_rules_selections.get_selected_name(),
            self.defuzzifier_selections.get_selected_name())

        for antecendent_names, consequence_name in self.rules_setting.rules.items():
            fuzzy_system.add_rule(consequence_name, antecendent_names)

        return fuzzy_system


class RadioButtonSet(QFrame):
    """A set of QRadioButton.

    Args:
        named_radiobtns (dict): a dictionary containing names (as key) for each
            QRadioButton. Use OrderedDict if you want to keep the set in order.
    """

    sig_rbtn_changed = Signal(str)

    def __init__(self, named_radiobtns):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.named_radiobtns = collections.OrderedDict(named_radiobtns)
        next(iter(self.named_radiobtns.values())).toggle()
        for radiobtn in self.named_radiobtns.values():
            radiobtn.toggled.connect(self.get_selected_name)
            layout.addWidget(radiobtn)

    @Slot()
    def get_selected_name(self):
        """Get which radio button is selected."""
        for name, btn in self.named_radiobtns.items():
            if btn.isChecked():
                self.sig_rbtn_changed.emit(name)
                return name

    def set_selected(self, name):
        """Set a radio button be selected by given name."""
        self.named_radiobtns[name].toggle()


class FuzzierVarSetting(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        layout = QFormLayout()
        self.setLayout(layout)

        # Create the fuzzy 3 sets with name and its membership function which is
        # Gaussian distribution.
        self.small = GaussianFuzzierSetting()
        self.medium = GaussianFuzzierSetting()
        self.large = GaussianFuzzierSetting()

        layout.addRow(QLabel("Small:"), self.small)
        layout.addRow(QLabel("Medium:"), self.medium)
        layout.addRow(QLabel("Large:"), self.large)

        self.viewer = FuzzierViewer()

        layout.addRow(self.viewer)

        self.small.descending.setChecked(True)
        self.large.ascending.setChecked(True)

        self.update_viewer()

        for var in (self.small, self.medium, self.large):
            var.mean.valueChanged.connect(self.update_viewer)
            var.sd.valueChanged.connect(self.update_viewer)
            var.ascending.stateChanged.connect(self.update_viewer)
            var.descending.stateChanged.connect(self.update_viewer)

    def setDisabled(self, boolean):
        self.small.setDisabled(boolean)
        self.medium.setDisabled(boolean)
        self.large.setDisabled(boolean)

    def setEnabled(self, boolean):
        self.small.setEnabled(boolean)
        self.medium.setEnabled(boolean)
        self.large.setEnabled(boolean)

    @Slot()
    def update_viewer(self):
        means = [self.small.mean.value(),
                 self.medium.mean.value(),
                 self.large.mean.value()]
        sds = [self.small.sd.value(),
               self.medium.sd.value(),
               self.large.sd.value()]
        ascendings = [self.small.ascending.isChecked(),
                      self.medium.ascending.isChecked(),
                      self.large.ascending.isChecked()]
        descendings = [self.small.descending.isChecked(),
                       self.medium.descending.isChecked(),
                       self.large.descending.isChecked()]
        self.viewer.remove_curves()
        self.viewer.add_curves(means, sds, ascendings, descendings)


class GaussianFuzzierSetting(QFrame):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.mean = QDoubleSpinBox()
        self.mean.setRange(-100, 100)
        self.mean.setStatusTip("The mean (mu) value for Gaussian function.")

        self.sd = QDoubleSpinBox()
        self.sd.setDecimals(3)
        self.sd.setValue(5)
        self.sd.setMinimum(0.1)
        self.sd.setStatusTip("The standard deviation (sigma) value for "
                             "Gaussian function.")

        self.ascending = QCheckBox()
        self.ascending.setIcon(QIcon(':/icons/ascending_icon.png'))
        self.ascending.setStatusTip("Make the fuzzier strictly ascending.")
        self.descending = QCheckBox()
        self.descending.setIcon(QIcon(':/icons/descending_icon.png'))
        self.descending.setStatusTip("Make the fuzzier strictly descending.")

        layout.addWidget(QLabel("Mean"))
        layout.addWidget(self.mean, 1)
        layout.addWidget(QLabel("Standard Deviation"))
        layout.addWidget(self.sd, 1)
        layout.addWidget(self.ascending)
        layout.addWidget(self.descending)

    def get_values(self):
        return (self.mean.value(), self.sd.value(),
                self.ascending.isChecked(), self.descending.isChecked())


class FuzzyRulesSetting(QTableWidget):
    def __init__(self, antecedent_product):
        super().__init__(
            len(antecedent_product[0]) + 1, len(antecedent_product))
        self.horizontalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setVerticalHeaderLabels(
            ['Front Dist.', '(Left-Right) Dist.', 'Consequence'])
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rules_selections = collections.OrderedDict()

        for col, antecedents in enumerate(antecedent_product):
            for row, antecedent in enumerate(antecedents):
                item = QTableWidgetItem(antecedent)
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row, col, item)
            combobox = QComboBox()
            combobox.addItems(['small', 'medium', 'large'])
            self.rules_selections[antecedents] = combobox

        for col, consequence in enumerate(self.rules_selections.values()):
            self.setCellWidget(2, col, consequence)

    @property
    def rules(self):
        rules = dict()
        for antecendent, consequence_selection in self.rules_selections.items():
            rules[antecendent] = consequence_selection.currentText()
        return rules

    def set_consequence_fuzzysets(self, name_list):
        """Set the consequence fuzzy sets in ORDER since the rules selections is
        a OrderedDict."""
        for name, consequence_selection in zip(name_list,
                                               self.rules_selections.values()):
            consequence_selection.setCurrentIndex(
                consequence_selection.findText(name))

    def setDisabled(self, boolean):
        for consequence_selection in self.rules_selections.values():
            consequence_selection.setDisabled(boolean)

    def setEnabled(self, boolean):
        for consequence_selection in self.rules_selections.values():
            consequence_selection.setEnabled(boolean)
