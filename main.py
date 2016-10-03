import sys
import os
import pickle

from PyQt5 import QtWidgets
from Designs import mainWindow
from Windows import AppWindows
from Models import Experiment
from Controllers import ExperimentControl


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.hardware_prefs = self.load_config_data()
        self.preferences = self.load_preferences_data()

        self.experiment = Experiment.Experiment()
        self.experiment_control = ExperimentControl.ExperimentController(self)

        # function bindings
        self.actionAnimal_List.triggered.connect(self.open_animal_window)
        self.actionHardware_Preferences.triggered.connect(self.open_hardware_window)
        self.actionPreferences.triggered.connect(self.open_preferences_window)

        self.startButton.clicked.connect(self.experiment_control.start)
        self.stopButton.clicked.connect(self.experiment_control.stop)

    @staticmethod
    def load_config_data():
        if os.path.exists('hardware.config'):
            with open('hardware.config', 'rb') as fn:
                return pickle.load(fn)
        else:
            return None

    @staticmethod
    def load_preferences_data():
        if os.path.exists('preferences.config'):
            with open('preferences.config', 'rb') as fn:
                return pickle.load(fn)
        else:
            return None

    def open_animal_window(self):
        animalWindow = AppWindows.AnimalWindow(self)
        animalWindow.show()

    def open_hardware_window(self):
        hardwareWindow = AppWindows.HardwareWindow(self)
        hardwareWindow.show()

    def open_preferences_window(self):
        preferencesWindow = AppWindows.PreferencesWindow(self)
        preferencesWindow.show()


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