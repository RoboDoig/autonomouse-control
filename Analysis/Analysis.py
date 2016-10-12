import Models.Experiment


def n_trials_performed(mouse):
    """
    @type mouse: Experiment.Mouse
    :return: int
    """
    total_trials = 0
    for schedule in mouse.schedule_list:
        total_trials += schedule.current_trial

    return total_trials
