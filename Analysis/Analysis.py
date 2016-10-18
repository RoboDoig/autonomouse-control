import Models.Experiment
import numpy as np


def n_trials_performed(mouse):
    """
    @type mouse: Experiment.Mouse
    :return: int
    """
    total_trials = 0
    for schedule in mouse.schedule_list:
        total_trials += schedule.current_trial

    return total_trials


def binned_performance(mouse, bin_size):
    """
    @type mouse: Experiment.Mouse
    @type bin_size: int
    :return: list
    """
    # first get all performed trials as vector
    all_correct = list()
    for schedule in mouse.schedule_list:
        for trial in schedule.trial_list:
            all_correct.append(trial.correct)

    # then bin according to bin_size
    binned_correct = list()
    for i in range(1, len(all_correct)):
        if i < bin_size:
            binned_correct.append(np.mean(all_correct[0:i]))
        else:
            binned_correct.append(np.mean(all_correct[i-bin_size:i]))

    return binned_correct
