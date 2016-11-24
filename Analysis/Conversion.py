import scipy.io as sio
from Models import Experiment
from PyPulse import PulseInterface
import os
import pickle
import csv
import collections as col


def load_experiment(path):
    data_files = list()
    for file in os.listdir(path):
        if file.endswith(".autmaus"):
            with open(path + file, 'rb') as fn:
                experiment = pickle.load(fn)

        if file.endswith(".mat"):
            data_files.append(path + file)

        if file.endswith(".csv"):
            schedule_map = read_schedule_map(path + file)

    return experiment, data_files, schedule_map


def read_schedule_map(path):
    schedule_map = dict()
    with open(path, 'rt') as sched:
        reader = csv.reader(sched)
        for row in reader:
            schedule_map[row[0]] = row[1]
    return schedule_map


def batch_convert(paths, out_path, out_name, trial_parameter):
    output = dict()
    for path in paths:
        experiment, data_files, schedule_map = load_experiment(path)

        for animal_id in experiment.animal_list.keys():
            this_animal = experiment.animal_list[animal_id]
            save_id = 'maus' + this_animal.id
            if save_id not in output.keys():
                output[save_id] = col.OrderedDict()

            for schedule in this_animal.schedule_list:
                sched_id = schedule.id.split('.')[0]
                sched_id = schedule_map[sched_id]
                match_sched = [sched for sched in output[save_id].keys() if sched_id in sched]
                sched_id = sched_id + '_' + str(len(match_sched) + 1)

                output[save_id][sched_id] = {'rewarded': list(), 'correct': list(), 'licked': list(),
                                             'data_file': list(), 'timestamp': list(),
                                             'schedule_name': schedule.id.split('.')[0],
                                             'schedule_params': list()}

                for t, trial in enumerate(schedule.trial_list):
                    time = str(trial.timestamp)
                    time = time.replace(' ', '_')
                    time = time.replace(':', '_')

                    output[save_id][sched_id]['rewarded'].append(schedule.schedule_trials[t][0])
                    output[save_id][sched_id]['correct'].append(trial.correct)
                    output[save_id][sched_id]['licked'].append(trial.response)
                    output[save_id][sched_id]['timestamp'].append(time)

                    if len(schedule.schedule_trials[t]) > trial_parameter:
                        output[save_id][sched_id]['schedule_params'].append(schedule.schedule_trials[t][trial_parameter])

                    match_file = [file for file in data_files if time in file]

                    if len(match_file) > 0:
                        output[save_id][sched_id]['data_file'].append(match_file)

    output = {out_name: output}

    sio.savemat(out_path + out_name, output)


def convert():
    batch_convert(['G:/Automated Behaviour/Temp_FineToDelete/InitialCorrDiscrimination/',
                   'G:/Automated Behaviour/Temp_FineToDelete/InitialCorrDiscriminationControls_UPDATE/',
                   'G:/Automated Behaviour/Temp_FineToDelete/Final2HzControls/',
                   'G:/Automated Behaviour/Temp_FineToDelete/ValveSwitchControl12Hz/',
                   'G:/Automated Behaviour/Temp_FineToDelete/FrequencyRange/',
                   'G:/Automated Behaviour/Temp_FineToDelete/FrequencyRange2/',
                   'G:/Automated Behaviour/Temp_FineToDelete/FrequencyRange3/'],
                   'C:/Users/erskina/PycharmProjects/AutonoMouseControl/TestFolder/', 'G1', 8)

if __name__ == '__main__':
    convert()
