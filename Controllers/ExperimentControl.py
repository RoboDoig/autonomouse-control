from PyQt5 import QtCore, QtGui
import numpy as np
from time import sleep
import sys
import random
from PyPulse import PulseInterface
import daqface.DAQ as daq


class ExperimentWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(None)
        self.parent = parent
        self.hardware_prefs = self.parent.parent.hardware_prefs
        self.experiment = self.parent.parent.experiment

    def trial(self):
        while self.parent.should_run:
            """ Is there an animal present? """
            if self.animal_present():
                """ Check which animal is present and get a reference to it """
                animal = self.get_present_animal()

                """ Look up current trial for this mouse """
                current_trial = animal.current_trial()

                """ Parse this trial into a set of DAQ commands """
                current_trial_pulse = animal.current_trial_pulse()
                pulses, t = PulseInterface.make_pulse(self.hardware_prefs['samp_rate'], 0.0, 0.0, current_trial_pulse)

                """ Send the data to the DAQ """
                trial_daq = daq.DoAiMultiTask(self.hardware_prefs['analog_input'],
                                                self.hardware_prefs['analog_channels'],
                                                self.hardware_prefs['digital_output'],
                                                self.hardware_prefs['samp_rate'],
                                                len(t) / self.hardware_prefs['samp_rate'],
                                                pulses, self.hardware_prefs['sync_clock'])

                analog_data = trial_daq.DoTask()

                print(analog_data)


        self.finished.emit()

    def animal_present(self):
        # checks whether animal is present in the port - DEBUG
        return np.random.rand() > 0.999999

    def get_present_animal(self):
        # returns the animal in the port - DEBUG just chooses a random animal
        animals = list(self.experiment.animal_list.keys())
        random_animal = random.choice(animals)
        return self.experiment.animal_list[random_animal]


class ExperimentController():
    def __init__(self, parent):
        self.parent = parent
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