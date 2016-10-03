import sys
import os
import pickle
import datetime

from PyQt5 import QtWidgets
from Designs import mainWindow
from Windows import AppWindows
from Models import Experiment, GuiModels
from Controllers import ExperimentControl


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.hardware_prefs = self.load_config_data()

        self.experiment = Experiment.Experiment()
        self.experiment_control = ExperimentControl.ExperimentController(self)

        # function bindings
        self.actionAnimal_List.triggered.connect(self.open_animal_window)
        self.actionHardware_Preferences.triggered.connect(self.open_hardware_window)
        self.actionSave_Experiment.triggered.connect(self.save_experiment)

        self.startButton.clicked.connect(self.experiment_control.start)
        self.stopButton.clicked.connect(self.experiment_control.stop)

        self.experiment_control.trial_job.trial_end.connect(self.update_trial_view)

        # trial view model
        self.model = GuiModels.TableModel(['Animal ID', 'Time Stamp', 'Schedule Idx', 'Trial Idx', 'Rewarded',
                                           'Response', 'Correct', 'Timeout'],
                                          self.experiment.trials, parent=self)

        self.trialView.setModel(self.model)

    @staticmethod
    def load_config_data():
        if os.path.exists('hardware.config'):
            with open('hardware.config', 'rb') as fn:
                return pickle.load(fn)
        else:
            return None

    @staticmethod
    def load_preference_data():
        if os.path.exists('preferences.config'):
            with open('preferences.config', 'rb') as fn:
                return pickle.load(fn)
        else:
            return None

    def open_animal_window(self):
        animal_window = AppWindows.AnimalWindow(self)
        animal_window.show()

    def open_hardware_window(self):
        hardware_window = AppWindows.HardwareWindow(self)
        hardware_window.show()

    def update_trial_view(self):
        self.model.layoutChanged.emit()

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
        fname, suff = QtWidgets.QFileDialog.getOpenFileName(self, "Open Experiment", '', "AutonoMouse Experiment (*.autmaus)")
        self.experiment = None
        self.experiment_control = None

        with open(fname, 'rb') as fn:
            self.experiment = pickle.load(fn)

        self.experiment_control = ExperimentControl.ExperimentController(self)

        self.update_experiment_info()


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