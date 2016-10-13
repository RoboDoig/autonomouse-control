import pickle


class Experiment:
    def __init__(self):
        self.animal_list = {'default': Mouse('default', 0.15)}
        self.default_row = [['', '', '', '', '', '', '', '']]
        self.trials = self.default_row.copy()

        self.name = None
        self.save_path = None
        self.date = None

        self.last_data = None

    def add_mouse(self, id, water):
        if id in self.animal_list.keys():
            self.animal_list[id].water = water
        else:
            self.animal_list[id] = Mouse(id, water)

    def add_trial(self, animal_id, timestamp, schedule, trial, rewarded, response, correct, timeout):
        if self.trials == self.default_row.copy():
            self.trials[0] = [animal_id, timestamp, schedule, trial, rewarded, response, correct, timeout]
        else:
            self.trials.append([animal_id, timestamp, schedule, trial, rewarded, response, correct, timeout])

    def save(self):
        fname = self.save_path + self.name

        with open(fname, 'wb') as fn:
            pickle.dump(self, fn)


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

    @property
    def current_trial_idx(self):
        return self.schedule_list[self.current_schedule_idx].current_trial

    def advance_trial(self):
        # end of schedule and schedules available to move to? advance to the next
        if not self.schedule_list[self.current_schedule_idx].trials_left() and \
                (self.current_schedule_idx + 1) < len(self.schedule_list):
            self.current_schedule_idx += 1

        # still trials left? advance to the next?
        elif self.schedule_list[self.current_schedule_idx].trials_left():
            self.schedule_list[self.current_schedule_idx].current_trial += 1

        # else we have reached the end of available trials - add a repeat of the current schedule
        else:
            current_schedule = self.schedule_list[self.current_schedule_idx]
            fail_safe_schedule = Schedule(current_schedule.id, current_schedule.schedule_trials,
                                          current_schedule.schedule_headers, current_schedule.trial_params)
            self.schedule_list.append(fail_safe_schedule)
            self.current_schedule_idx += 1


class Schedule:
    def __init__(self, id, schedule_trials, schedule_headers, trial_params):
        self.id = id
        self.current_trial = 0
        self.schedule_trials = schedule_trials
        self.schedule_headers = schedule_headers
        self.trial_params = trial_params

        self.trial_list = list()

    def add_trial_data(self, timestamp, response, correct, timeout):
        self.trial_list.append(Trial(timestamp, response, correct, timeout))

    def n_trials(self):
        return len(self.schedule_trials)

    def trials_left(self):
        return self.current_trial < self.n_trials() - 1


class Trial:
    def __init__(self, timestamp, response, correct, timeout):
        self.timestamp = timestamp
        self.response = response
        self.correct = correct
        self.timeout = timeout
