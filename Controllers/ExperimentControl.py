from PyQt5 import QtCore, QtGui
import numpy as np
from time import sleep
import sys


class ExperimentWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(None)
        self.parent = parent

        self.counter = 0

    def trial(self):
        while self.parent.should_run:
            print(self.counter)
            self.counter += 1
            sleep(0.1)
        self.finished.emit()


class ExperimentController():
    def __init__(self):
        self.thread = QtCore.QThread()
        self.trial_job = ExperimentWorker(self)
        self.trial_job.moveToThread(self.thread)

        self.thread.finished.connect(self.thread.quit)
        self.thread.started.connect(self.trial_job.trial)

        self.should_run = False

    def start(self):
        if not self.should_run:
            self.should_run = True
            self.thread.start()

    def stop(self):
        if self.should_run:
            self.should_run = False
            self.thread.terminate()
            self.thread.wait()