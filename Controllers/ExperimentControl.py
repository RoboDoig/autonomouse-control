from PyQt5 import QtCore, QtWidgets
from time import sleep, time
from PyPulse import PulseInterface
import daqface.DAQ as daq
from TrialLogic import TrialConditions
import datetime
import scipy.io as sio
import HelperFunctions.RFID as rfid
import HelperFunctions.Reward as reward
import HelperFunctions.BeamCheck as beam


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
                self.experiment.last_data = lick_data

                """ Analyse the lick response """
                rewarded = current_trial[0]
                # TODO - reference to rewarded (current_trial[0]) and lick fraction are bug prone here.
                # TODO - A little too inflexible
                response = TrialConditions.lick_detect(lick_data, 2, float(current_trial_pulse[0]['lick_fraction']))
                result, correct, timeout = TrialConditions.trial_result(rewarded, response)

                """ Update database """
                timestamp = datetime.datetime.now()
                animal.schedule_list[animal.current_schedule_idx].add_trial_data(timestamp, response, correct, timeout)
                self.experiment.add_trial(animal.id, timestamp, animal.current_schedule_idx, animal.current_trial_idx,
                                          rewarded, response, correct, timeout)

                """ Determine reward conditions and enact """
                if result == TrialConditions.TrialResult.correct_response:
                    self.reward(animal)
                elif result == TrialConditions.TrialResult.false_alarm:
                    self.timeout()

                """ Advance animal to next trial """
                animal.advance_trial()

                """ Save bulkiest part of data to disk and save experiment if necessary """
                self.save_data(animal.id, timestamp, analog_data, rewarded, response, correct, timeout, pulses, t)
                if len(self.experiment.trials) % 20 == 0:
                    self.experiment.save()

                """ Signal that trial has finished """
                print(time() - start)
                self.trial_end.emit()

            sleep(3.0)

        self.finished.emit()

    def animal_present(self):
        # checks whether animal is present in the port - DEBUG
        # return np.random.rand() > 0.999999

        return beam.check_beam(self.hardware_prefs['analog_input'], self.hardware_prefs['analog_channels'],
                               self.hardware_prefs['beam_channel'])

    def get_present_animal(self):
        # returns the animal in the port - DEBUG just chooses a random animal
        # animals = list(self.experiment.animal_list.keys())
        # animal = random.choice(animals)

        animal = rfid.check_rfid(self.hardware_prefs['rfid_port'], 10)
        try:
            if animal in self.experiment.animal_list.keys():
                return self.experiment.animal_list[animal]
            else:
                return self.experiment.animal_list['default']
        except:
            return self.experiment.animal_list['default']

    def reward(self, animal):
        # TODO - "dev2/ai0" here is a dummy analog input channel, so that analog output can borrow the analog input...
        # TODO - ...clock - should be changed to be customisable in hardware_prefs before release
        reward.deliver_reward("dev2/ai0", self.hardware_prefs['analog_output'], self.hardware_prefs['sync_clock'],
                              self.hardware_prefs['samp_rate'], animal.water)

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


class ExperimentController:
    def __init__(self, parent):
        self.parent = parent
        self.thread = QtCore.QThread()
        self.trial_job = ExperimentWorker(self)
        self.trial_job.moveToThread(self.thread)

        self.thread.finished.connect(self.thread.quit)
        self.thread.started.connect(self.trial_job.trial)

        self.should_run = False

    def start(self):
        if self.parent.experiment.save_path is not None:
            if not self.should_run:
                self.should_run = True
                self.thread.start()
        else:
            QtWidgets.QMessageBox.about(self.parent, "Error", "Experiment not saved! Please save before starting.")

    def stop(self):
        if self.should_run:
            self.should_run = False
            self.thread.terminate()
            self.thread.wait()
