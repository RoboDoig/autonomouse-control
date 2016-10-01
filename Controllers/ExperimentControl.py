from PyQt5 import QtCore


class ExperimentLoop(QtCore.QThread):
    def __init__(self, parent=None):
        """
        @type parent: ExperimentController
        """
        QtCore.QThread.__init__(self)
        self.parent = parent

    trigger = QtCore.pyqtSignal()

    def run(self):
        print('not implemented')


class ExperimentController():
    def __init__(self, parent):
        self.thread = ExperimentLoop(self)
        self.thread.trigger.connect(self.finish_trial)
        self.should_run = False

    def start_experiment(self):
        print('not implemented')

    def stop_experiment(self):
        print('not implemented')

    def finish_trial(self):
        print('not implemented')