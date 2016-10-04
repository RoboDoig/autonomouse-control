from PyQt5 import QtCore, QtGui
import numpy as np
from time import sleep, time
import sys
import random
from PyPulse import PulseInterface
import daqface.DAQ as daq
from TrialLogic import TrialConditions
import datetime
import scipy.io as sio


class ExperimentWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    trial_end = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(None)
        self.parent = parent
        self.hardware_prefs = self.parent.parent.hardware_prefs
        self.experiment = self.parent.parent.experiment

    def trial(self):
        while self.parent.should_run:
            start = time()
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
                lick_data = analog_data[self.hardware_prefs['lick_channel']]

                """ Analyse the lick response """
                rewarded = current_trial[0]
                # TODO - reference to rewarded (current_trial[0]) and lick fraction are bug prone here.
                #  A little too inflexible
                response = TrialConditions.lick_detect(lick_data, 2, float(current_trial_pulse[0]['lick_fraction']))
                result, correct, timeout = TrialConditions.trial_result(rewarded, response)

                """ Update database """
                timestamp = datetime.datetime.now()
                animal.schedule_list[animal.current_schedule_idx].add_trial_data(timestamp, response, correct, timeout)
                self.experiment.add_trial(animal.id, timestamp, animal.current_schedule_idx, animal.current_trial_idx,
                                          rewarded, response, correct, timeout)

                """ Determine reward conditions and enact """
                if result == TrialConditions.TrialResult.correct_response:
                    self.reward()
                elif result == TrialConditions.TrialResult.false_alarm:
                    self.timeout()

                """ Advance animal to next trial """
                animal.advance_trial()

                """ Save bulkiest part of data to disk and save experiment if necessary """
                self.save_data(animal.id, timestamp, analog_data, rewarded, response, correct, timeout, pulses, t)

                """ Signal that trial has finished """
                print(time() - start)
                self.trial_end.emit()

        self.finished.emit()

    def animal_present(self):
        # checks whether animal is present in the port - DEBUG
        return np.random.rand() > 0.999999

    def get_present_animal(self):
        # returns the animal in the port - DEBUG just chooses a random animal
        animals = list(self.experiment.animal_list.keys())
        random_animal = random.choice(animals)
        return self.experiment.animal_list[random_animal]

    def reward(self):
        print('not implemented')

    def timeout(self):
        sleep(self.hardware_prefs['timeout'])

    def save_data(self, animal_id, timestamp, analog_data, rewarded, response, correct, timeout, pulses, time_axis):

        timestamp = str(timestamp)
        timestamp = timestamp.replace(' ', '_')
        timestamp = timestamp.replace(':', '_')

        file_name = self.experiment.save_path + '/' + str(len(self.experiment.trials)) + '_' + timestamp + '_' + animal_id

        sio.savemat(file_name + '.mat', {'animal_id': animal_id,
                                         'timestamp': timestamp,
                                         'analog_data': analog_data,
                                         'rewarded': rewarded,
                                         'response': response,
                                         'correct': correct,
                                         'timeout': timeout,
                                         'pulses': pulses,
                                         'time_axis': time_axis})


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