import sys

from PyQt5 import QtWidgets
from Designs import mainWindow
from Windows import AppWindows
from Models import Experiment


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.experiment = Experiment.Experiment()

        # function bindings
        self.actionAnimal_List.triggered.connect(self.open_animal_window)

    def open_animal_window(self):
        animalWindow = AppWindows.AnimalWindow(self)
        animalWindow.show()


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