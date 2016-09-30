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


class Schedule:
    def __init__(self, id):
        self.id = id
        self.current_trial = 0
        self.trial_list = list()


class Trial:
    def __init__(self, parameters):
        self.parameters = parameters