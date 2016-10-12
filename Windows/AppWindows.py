import pickle
import os

from PyQt5 import QtWidgets, QtGui
from Designs import animalWindow, hardwareWindow, prefsWindow, analysisWindow
from Models import Experiment, GuiModels
from Analysis import Analysis


class AnimalWindow(QtWidgets.QMainWindow, animalWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        self.populate_animal_table(parent.experiment.animal_list)

        # function bindings
        self.addRowButton.clicked.connect(self.add_row)
        self.removeRowButton.clicked.connect(self.remove_row)
        self.actionUpdate.triggered.connect(self.update_animals)
        self.addScheduleButton.clicked.connect(self.add_schedule)

        self.animalTable.selectionModel().selectionChanged.connect(self.animal_selected)
        self.scheduleTable.selectionModel().selectionChanged.connect(self.schedule_selected)

    def add_row(self):
        self.animalTable.insertRow(self.animalTable.rowCount())

    def remove_row(self):
        if self.animalTable.rowCount() > 1:
            self.animalTable.removeRow(self.animalTable.rowCount() - 1)

    def populate_animal_table(self, animal_list):
        self.animalTable.clear()

        self.animalTable.setRowCount(len(animal_list.keys()))
        self.animalTable.setColumnCount(2)

        for a, animal in enumerate(animal_list.keys()):
            id = QtWidgets.QTableWidgetItem(animal_list[animal].id)
            water = QtWidgets.QTableWidgetItem(str(animal_list[animal].water))
            self.animalTable.setItem(a, 0, id)
            self.animalTable.setItem(a, 1, water)

    def current_animal(self):
        try:
            row = self.animalTable.selectedIndexes()[0].row()
            animal = self.parent.experiment.animal_list[self.animalTable.item(row, 0).text()]
            return animal
        except:
            return None

    def current_sched_index(self):
        try:
            row = self.scheduleTable.selectedIndexes()[0].row()
            return row
        except:
            return 0

    def update_animals(self):
        for row in range(self.animalTable.rowCount()):
            id = self.animalTable.item(row, 0).text()
            water = float(self.animalTable.item(row, 1).text())

            self.parent.experiment.add_mouse(id, water)

    def animal_selected(self):
        animal = self.current_animal()
        if animal is not None:
            self.scheduleTable.setRowCount(len(animal.schedule_list))
            self.scheduleTable.setColumnCount(3)

            for s, schedule in enumerate(animal.schedule_list):
                sched_name = QtWidgets.QTableWidgetItem(schedule.id)
                n_trials = QtWidgets.QTableWidgetItem(str(len(schedule.schedule_trials)))
                perc_complete = round(((schedule.current_trial) / (len(schedule.schedule_trials) - 1)) * 100, 2)
                progress = QtWidgets.QTableWidgetItem(str(perc_complete))

                self.scheduleTable.setItem(s, 0, sched_name)
                self.scheduleTable.setItem(s, 1, n_trials)
                self.scheduleTable.setItem(s, 2, progress)

    def schedule_selected(self):
        animal = self.current_animal()
        schedule = animal.schedule_list[self.current_sched_index()]

        self.trialView.setModel(GuiModels.TableModel(schedule.schedule_headers, schedule.schedule_trials, parent=self))

    def add_schedule(self):
        animal = self.current_animal()
        if animal is not None:
            fname, suff = QtWidgets.QFileDialog.getOpenFileName(self, "Load Schedule", '', '*.schedule')
            with open(fname, 'rb') as fn:
                schedule_data = pickle.load(fn)

            animal.add_schedule(os.path.basename(fname), schedule_data['schedule'], schedule_data['headers'],
                                schedule_data['params'])

            self.animal_selected()


class HardwareWindow(QtWidgets.QMainWindow, hardwareWindow.Ui_MainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        if self.parent.hardware_prefs is not None:
            self.set_preferences(self.parent.hardware_prefs)

        self.actionSave_Preferences.triggered.connect(self.save_preferences)

    def set_preferences(self, prefs):
        self.analogInputEdit.setText(prefs['analog_input'])
        self.analogChannelsSpin.setValue(prefs['analog_channels'])
        self.digitalOutputEdit.setText(prefs['digital_output'])
        self.syncClockEdit.setText(prefs['sync_clock'])
        self.digitalChannelsSpin.setValue(prefs['digital_channels'])
        self.analogOutputEdit.setText(prefs['analog_output'])
        self.analogOutChannelsSpin.setValue(prefs['analog_out_channels'])
        self.rfidPortEdit.setText(prefs['rfid_port'])
        self.samplingRateEdit.setText(str(prefs['samp_rate']))
        self.lickChannelSpin.setValue(prefs['lick_channel'])
        self.timeoutEdit.setText(str(prefs['timeout']))
        self.beamChannelSpin.setValue(prefs['beam_channel'])
        self.rewardChannelSpin.setValue(prefs['reward_channel'])

    def save_preferences(self):
        prefs = {'analog_input': self.analogInputEdit.text(),
                 'analog_channels': int(self.analogChannelsSpin.value()),
                 'digital_output': self.digitalOutputEdit.text(),
                 'digital_channels': int(self.digitalChannelsSpin.value()),
                 'analog_output': self.analogOutputEdit.text(),
                 'analog_out_channels': int(self.analogOutChannelsSpin.text()),
                 'sync_clock': self.syncClockEdit.text(),
                 'rfid_port': self.rfidPortEdit.text(),
                 'samp_rate': int(self.samplingRateEdit.text()),
                 'lick_channel': int(self.lickChannelSpin.value()),
                 'timeout': int(self.timeoutEdit.text()),
                 'beam_channel': int(self.beamChannelSpin.value()),
                 'reward_channel': int(self.rewardChannelSpin.value())}

        self.parent.hardware_prefs = prefs

        with open('hardware.config', 'wb') as fn:
            pickle.dump(prefs, fn)


class PreferencesWindow(QtWidgets.QMainWindow, prefsWindow.Ui_MainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        if self.parent.preferences is not None:
            self.set_preferences(self.parent.preferences)

        self.actionSave_Preferences.triggered.connect(self.save_preferences)
        self.savePathButton.clicked.connect(self.select_save_path)

    def set_preferences(self, prefs):
        self.savePathEdit.setText(prefs['save_path'])
        self.experimentNameEdit.setText(prefs['experiment_name'])

    def save_preferences(self):
        prefs = {'save_path': self.savePathEdit.text(),
                 'experiment_name': self.experimentNameEdit.text()}

        self.parent.preferences = prefs

        with open('preferences.config', 'wb') as fn:
            pickle.dump(prefs, fn)

    def select_save_path(self):
        save_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose Save Folder')
        self.savePathEdit.setText(save_path)


class AnalysisWindow(QtWidgets.QMainWindow, analysisWindow.Ui_MainWindow):
    def __init__(self, experiment, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.experiment = experiment

        self.populate_stats_table()

    def populate_stats_table(self):
        self.experimentStatsTable.setRowCount(len(self.experiment.animal_list.keys()))

        for m, mouse in enumerate(self.experiment.animal_list.keys()):
            id = QtWidgets.QTableWidgetItem(self.experiment.animal_list[mouse].id)
            total_trials = QtWidgets.QTableWidgetItem(str(Analysis.n_trials_performed(self.experiment.animal_list[mouse])))
            self.experimentStatsTable.setItem(m, 0, id)
            self.experimentStatsTable.setItem(m, 1, total_trials)