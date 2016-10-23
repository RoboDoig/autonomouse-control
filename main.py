import sys
import os
import pickle
import datetime
import numpy as np

from PyQt5 import QtWidgets
from Designs import mainWindow
from Windows import AppWindows
from Models import Experiment, GuiModels
from Controllers import ExperimentControl
from PyPulse import PulseInterface


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.hardware_prefs = self.load_config_data()

        self.setup_experiment_bindings(Experiment.Experiment())

        # function bindings
        self.actionAnimal_List.triggered.connect(self.open_animal_window)
        self.actionHardware_Preferences.triggered.connect(self.open_hardware_window)
        self.actionAnalyse_Experiment.triggered.connect(self.open_analysis_window)
        self.actionSave_Experiment.triggered.connect(self.save_experiment)
        self.actionLoad_Experiment.triggered.connect(self.load_experiment)

    def setup_experiment_bindings(self, experiment):
        self.experiment = experiment
        self.experiment_control = ExperimentControl.ExperimentController(self)

        self.model = GuiModels.TableModel(['Animal ID', 'Time Stamp', 'Schedule Idx', 'Trial Idx', 'Rewarded',
                                           'Response', 'Correct', 'Timeout'],
                                            self.experiment.trials, parent=self)

        self.trialView.setModel(self.model)

        try:
            self.startButton.disconnect()
            self.stopButton.disconnect()
        except:
            pass
        self.startButton.clicked.connect(self.experiment_control.start)
        self.stopButton.clicked.connect(self.experiment_control.stop)

        self.experiment_control.trial_job.trial_end.connect(self.update_trial_view)
        self.experiment_control.trial_job.trial_end.connect(self.update_data_view)

        self.trialView.selectionModel().selectionChanged.connect(self.on_trial_selected)

    @staticmethod
    def load_config_data():
        if os.path.exists('hardware.config'):
            with open('hardware.config', 'rb') as fn:
                return pickle.load(fn)
        else:
            return None

    def open_animal_window(self):
        animal_window = AppWindows.AnimalWindow(self)
        animal_window.show()

    def open_hardware_window(self):
        hardware_window = AppWindows.HardwareWindow(self)
        hardware_window.show()

    def open_analysis_window(self):
        analysis_window = AppWindows.AnalysisWindow(self.experiment, parent=self)
        analysis_window.show()

    def update_trial_view(self):
        self.model.layoutChanged.emit()

    def update_data_view(self):
        self.dataView.plotItem.clear()
        self.dataView.plotItem.plot(np.arange(len(self.experiment.last_data)) / self.hardware_prefs['samp_rate'],
                                    np.array(self.experiment.last_data))
        self.dataView.setYRange(0, 6)

    def update_graphics_view(self, trial):
        animal = self.experiment.trials[trial][0]
        sched_idx = self.experiment.trials[trial][2]
        trial_idx = self.experiment.trials[trial][3]

        try:
            trial_data = self.experiment.animal_list[animal].schedule_list[sched_idx].trial_params[trial_idx]

            pulses, t = PulseInterface.make_pulse(self.hardware_prefs['samp_rate'], 0.0, 0.0, trial_data)

            self.graphicsView.plotItem.clear()
            for p, pulse in enumerate(pulses):
                self.graphicsView.plotItem.plot(t, np.array(pulse) - (p * 1.1))
        except:
            pass

    def on_trial_selected(self):
        try:
            selected_trial = self.trialView.selectionModel().selectedRows()[0].row()
        except:
            selected_trial = 0
        self.update_graphics_view(selected_trial)

    def update_experiment_info(self):
        self.experimentNameLabel.setText(self.experiment.name)
        self.experimentDateLabel.setText(self.experiment.date)
        self.savePathLabel.setText(self.experiment.save_path)

    def save_experiment(self):
        # TODO - bit messy, what if the experiment class changes, should rather be saving the data in the class
        fname, suff = QtWidgets.QFileDialog.getSaveFileName(self, "Save Experiment", '', "AutonoMouse Experiment (*.autmaus)")
        self.experiment.name = os.path.basename(fname)
        self.experiment.save_path = os.path.dirname(fname)

        # We don't change the original date of creation
        if self.experiment.date is None:
            self.experiment.date = str(datetime.datetime.now())

        self.update_experiment_info()

        with open(fname, 'wb') as fn:
            pickle.dump(self.experiment, fn)

    def load_experiment(self):
        fname, suff = QtWidgets.QFileDialog.getOpenFileName(self, "Open Experiment", '',
                                                            "AutonoMouse Experiment (*.autmaus)")

        if fname != '':
            with open(fname, 'rb') as fn:
                experiment = pickle.load(fn)

            self.setup_experiment_bindings(experiment)

            self.update_experiment_info()
            self.update_trial_view()


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()