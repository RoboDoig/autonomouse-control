class Experiment:
    def __init__(self):
        self.animal_list = {'default': Mouse('default', 15.0)}

    def add_mouse(self, id, water):
        if id in self.animal_list.keys():
            self.animal_list[id].water = water
        else:
            self.animal_list[id] = Mouse(id, water)


class Mouse:
    def __init__(self, id, water):
        self.id = id
        self.water = water
        self.current_schedule_idx = 0
        self.schedule_list = list()

    def add_schedule(self, schedule_name, schedule_data, schedule_headers, trial_parameters):
        self.schedule_list.append(Schedule(schedule_name, schedule_data, schedule_headers, trial_parameters))

    def current_trial(self):
        current_schedule = self.schedule_list[self.current_schedule_idx]
        current_trial = current_schedule.schedule_trials[current_schedule.current_trial]
        return current_trial

    def current_trial_pulse(self):
        current_schedule = self.schedule_list[self.current_schedule_idx]
        pulse_params = current_schedule.trial_params[current_schedule.current_trial]
        return pulse_params


class Schedule:
    def __init__(self, id, schedule_trials, schedule_headers, trial_params):
        self.id = id
        self.current_trial = 0
        self.schedule_trials = schedule_trials
        self.schedule_headers = schedule_headers
        self.trial_params = trial_params


class Trial:
    def __init__(self, parameters):
        self.parameters = parameters