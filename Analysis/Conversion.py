import scipy.io as sio
from Models import Experiment
from PyPulse import PulseInterface
import os
import pickle


# def convert_experiment_to_matlab(experiment, path, name):
#     """
#     @type experiment: Experiment.Experiment
#     """
#     output = dict()
#     for animal_id in experiment.animal_list.keys():
#         this_animal = experiment.animal_list[animal_id]
#         rewarded = list()
#         correct = list()
#         for schedule in this_animal.schedule_list:
#             for t, trial in enumerate(schedule.trial_list):
#                 rewarded.append(schedule.schedule_trials[t][0])
#                 correct.append(trial.correct)
#
#         save_id = 'm_' + animal_id
#         output[save_id] = {'rewarded': rewarded, 'correct': correct}
#
#     output = {'data': output}
#
#     sio.savemat(path + '/' + name, output)


def load_experiment(path):
    data_files = list()
    for file in os.listdir(path):
        if file.endswith(".autmaus"):
            with open(path + file, 'rb') as fn:
                experiment = pickle.load(fn)

        if file.endswith(".mat"):
            data_files.append(path + file)

    return experiment, data_files


def convert_experiment_to_matlab(experiment, data_files, out_path, out_name):
    """
    @type experiment: Experiment.Experiment
    @type out_path: str
    @type out_name: str
    """
    output = dict()
    for animal_id in experiment.animal_list.keys():
        this_animal = experiment.animal_list[animal_id]
        save_id = 'maus' + this_animal.id
        output[save_id] = dict()

        for schedule in this_animal.schedule_list:
            sched_id = schedule.id.split('.')[0]
            output[save_id][sched_id] = {'rewarded': list(), 'correct': list(), 'licked': list(),
                                         'data_file': list(), 'timestamp': list(), 'analog_data': list()}

            for t, trial in enumerate(schedule.trial_list):
                time = str(trial.timestamp)
                time = time.replace(' ', '_')
                time = time.replace(':', '_')

                output[save_id][sched_id]['rewarded'].append(schedule.schedule_trials[t][0])
                output[save_id][sched_id]['correct'].append(trial.correct)
                output[save_id][sched_id]['licked'].append(trial.response)
                output[save_id][sched_id]['timestamp'].append(time)

                match_file = [file for file in data_files if time in file]

                if len(match_file) > 0:
                    output[save_id][sched_id]['data_file'].append(match_file)

                    output[save_id][sched_id]['analog_data'].append(sio.loadmat(match_file[0]))

    output = {out_name: output}

    sio.savemat(out_path + out_name, output)


e, data_files = load_experiment('G:/Automated Behaviour/Temp_FineToDelete/Final2HzControls/')
convert_experiment_to_matlab(e, data_files, 'C:/Users/erskina/PycharmProjects/AutonoMouseControl/TestFolder/', 'G1')
