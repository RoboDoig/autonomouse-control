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


def batch_convert(paths, out_path, out_name):
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
                                             'schedule_name': schedule.id.split('.')[0]}

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

    output = {out_name: output}

    sio.savemat(out_path + out_name, output)

<<<<<<< HEAD

def convert():
    batch_convert(['G:/Automated Behaviour/Temp_FineToDelete/InitialCorrDiscrimination/',
                   'G:/Automated Behaviour/Temp_FineToDelete/InitialCorrDiscriminationControls_UPDATE/',
                   'G:/Automated Behaviour/Temp_FineToDelete/Final2HzControls/',
                   'G:/Automated Behaviour/Temp_FineToDelete/ValveSwitchControl12Hz/'],
                   'C:/Users/erskina/PycharmProjects/AutonoMouseControl/TestFolder/', 'G1')

if __name__ == '__main__':
    convert()
=======
# schedule_map = {'Sm_FrontValves_Short': '2Hz_100_12',
#                 'Sm_BackValves_Short': '2Hz_100_12',
#                 'Sp_FrontValves_Short': '2Hz_100_12',
#                 'Sp_BackValves_Short': '2Hz_100_12',
#                 'Sm_FrontValves_12hz': '12Hz_300_12',
#                 'Sm_BackValves_12hz': '12Hz_300_12',
#                 'Sp_FrontValves_12hz': '12Hz_300_12',
#                 'Sp_BackValves_12hz': '12Hz_300_12',
#                 'Pretrain_3': 'Pretrain'}
#
# e, data_files = load_experiment('G:/Automated Behaviour/Temp_FineToDelete/Final2HzControls/')
# convert_experiment_to_matlab(e, data_files, schedule_map, 'C:/Users/erskina/PycharmProjects/AutonoMouseControl/TestFolder/', 'G1')

# batch_convert(['G:/Automated Behaviour/Temp_FineToDelete/InitialCorrDiscrimination/',
#                'G:/Automated Behaviour/Temp_FineToDelete/InitialCorrDiscriminationControls_UPDATE/',
#                'G:/Automated Behaviour/Temp_FineToDelete/Final2HzControls/'],
#                'C:/Users/erskina/PycharmProjects/AutonoMouseControl/TestFolder/', 'G1')
>>>>>>> 744664ba67eabb66be8951c8150178c54975dc59
