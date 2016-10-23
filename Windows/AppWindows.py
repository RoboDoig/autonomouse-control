import pickle
import os
import numpy as np
import datetime

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

        for a, animal in enumerate(sorted(list(animal_list.keys()))):
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

        self.experimentStatsTable.selectionModel().selectionChanged.connect(self.on_animal_selected)

    def populate_stats_table(self):
        self.experimentStatsTable.setRowCount(len(self.experiment.animal_list.keys()))

        for m, mouse in enumerate(sorted(list(self.experiment.animal_list.keys()))):
            this_mouse = self.experiment.animal_list[mouse]

            id = QtWidgets.QTableWidgetItem(this_mouse.id)
            total_trials = QtWidgets.QTableWidgetItem(str(Analysis.n_trials_performed(this_mouse)))
            trials_last24h = QtWidgets.QTableWidgetItem(str(Analysis.n_trials_last_24(this_mouse)))

            self.experimentStatsTable.setItem(m, 0, id)
            self.experimentStatsTable.setItem(m, 1, total_trials)
            self.experimentStatsTable.setItem(m, 2, trials_last24h)

    def on_animal_selected(self):
        self.display_animal_performance()
        self.display_group_performance()

    def display_animal_performance(self):
        animal = self.current_animal()
        if animal is not None:
            # binned_correct = Analysis.binned_performance(animal, int(self.binSizeSpin.value())) -
            # Non-weighted performance

            binned_correct = Analysis.weighted_binned_performance(animal, int(self.binSizeSpin.value()))

            self.animalPerformanceView.plotItem.clear()
            self.animalPerformanceView.plotItem.plot(binned_correct)

            # Guide lines
            self.animalPerformanceView.plotItem.plot(np.ones(len(binned_correct)) * 0.5, pen='r')
            self.animalPerformanceView.plotItem.plot(np.ones(len(binned_correct)) * 0.8, pen='g')

            self.animalPerformanceView.setYRange(-0.1, 1.1)

    def display_group_performance(self):
        n_longest = 0
        all_performance = list()
        bin_size = int(self.binSizeSpin.value())
        for animal_id in self.parent.experiment.animal_list.keys():
            animal = self.parent.experiment.animal_list[animal_id]
            if animal_id != 'default':
                this_performance = Analysis.binned_performance(animal, bin_size)
                all_performance.append(this_performance)
                if len(this_performance) > n_longest:
                    n_longest = len(this_performance)

        performance_matrix = np.empty((len(self.parent.experiment.animal_list)-1, n_longest))
        performance_matrix[:] = np.nan

        for p, perf in enumerate(all_performance):
            performance_matrix[p][0:len(perf)] = perf

        av_performance = np.nanmean(performance_matrix, 0)
        std_performance = np.nanstd(performance_matrix, 0)

        self.groupPerformanceView.plotItem.clear()
        self.groupPerformanceView.plotItem.plot(av_performance)
        self.groupPerformanceView.plotItem.plot(av_performance + std_performance, pen='m')
        self.groupPerformanceView.plotItem.plot(av_performance - std_performance, pen='m')
        # Guide lines
        self.groupPerformanceView.plotItem.plot(np.ones(len(av_performance)) * 0.5, pen='r')
        self.groupPerformanceView.plotItem.plot(np.ones(len(av_performance)) * 0.8, pen='g')


    def current_animal(self):
        try:
            row = self.experimentStatsTable.selectedIndexes()[0].row()
            animal = self.parent.experiment.animal_list[self.experimentStatsTable.item(row, 0).text()]
            return animal
        except:
            return None

