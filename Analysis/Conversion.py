import scipy.io as sio
from Models import Experiment


def convert_experiment_to_matlab(experiment, path, name):
    """
    @type experiment: Experiment.Experiment
    """
    output = dict()
    for animal_id in experiment.animal_list.keys():
        this_animal = experiment.animal_list[animal_id]
        rewarded = list()
        correct = list()
        for schedule in this_animal.schedule_list:
            for t, trial in enumerate(schedule.trial_list):
                rewarded.append(schedule.schedule_trials[t][0])
                correct.append(trial.correct)

        save_id = 'm_' + animal_id
        output[save_id] = {'rewarded': rewarded, 'correct': correct}

    output = {'data': output}

    sio.savemat(path + '/' + name, output)
