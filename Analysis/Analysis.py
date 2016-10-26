import Models.Experiment
import numpy as np
import datetime


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
    for i in range(1, len(all_correct) + 1):
        if i < bin_size:
            binned_correct.append(np.mean(all_correct[0:i]))
        else:
            binned_correct.append(np.mean(all_correct[i-bin_size:i]))

    return binned_correct


def weighted_binned_performance(mouse, bin_size):
    """
    @type mouse: Experiment.Mouse
    @type bin_size: int
    :return: list

    In this function we examine performance weighted by how many rewarded vs. unrewarded trials there were.
    """
    # first get all performed trials as vector
    all_correct = list()
    all_rewarded = list()
    for schedule in mouse.schedule_list:
        for t, trial in enumerate(schedule.trial_list):
            all_correct.append(trial.correct)
            all_rewarded.append(schedule.schedule_trials[t][0])

    # then bin according to bin_size
    binned_perf = list()
    for i in range(1, len(all_correct)):
        if i < bin_size:
            this_bin_correct = all_correct[0:i]
            this_bin_rewarded = all_rewarded[0:i]
        else:
            this_bin_correct = all_correct[i-bin_size:i]
            this_bin_rewarded = all_rewarded[i-bin_size:i]

        rewarded_count = np.sum(this_bin_rewarded)
        unrewarded_count = len(this_bin_rewarded) - rewarded_count

        sp_fraction = len([t for t, trial in enumerate(this_bin_correct) if this_bin_rewarded[t] + this_bin_correct[t] > 1]) / rewarded_count

        if unrewarded_count > 0:
            sm_fraction = len([t for t, trial in enumerate(this_bin_correct) if this_bin_rewarded[t] - this_bin_correct[t] < 0]) / unrewarded_count
        else:
            sm_fraction = 1

        binned_perf.append((sp_fraction + sm_fraction) / 2)

    return binned_perf


def n_trials_since(mouse, since):
    """
    @type mouse: Experiment.Mouse
    @type since: datetime.datetime
    :return: int
    """
    n_trials = 0

    for schedule in mouse.schedule_list:
        for trial in schedule.trial_list:
            if trial.timestamp > since:
                n_trials += 1

    return n_trials


def n_trials_last_24(mouse):
    return n_trials_since(mouse, datetime.datetime.now() - datetime.timedelta(days=1))
