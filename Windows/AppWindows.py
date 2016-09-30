import pickle
import os

from PyQt5 import QtWidgets, QtGui
from Designs import animalWindow
from Models import Experiment, GuiModels


class AnimalWindow(QtWidgets.QMainWindow, animalWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        self.populate_animal_table(parent.experiment.animal_list)

        # function bindings
        self.addRowButton.clicked.connect(self.add_row)
        self.removeRowButton.clicked.connect(self.remove_row)
        self.actionUpdate.triggered.connect(self.update_animals)
        self.addScheduleButton.clicked.connect(self.add_schedule)

        self.animalTable.selectionModel().selectionChanged.connect(self.animal_selected)
        self.scheduleTable.selectionModel().selectionChanged.connect(self.schedule_selected)

    def add_row(self):
        self.animalTable.insertRow(self.animalTable.rowCount())

    def remove_row(self):
        if self.animalTable.rowCount() > 1:
            self.animalTable.removeRow(self.animalTable.rowCount() - 1)

    def populate_animal_table(self, animal_list):
        self.animalTable.clear()

        self.animalTable.setRowCount(len(animal_list.keys()))
        self.animalTable.setColumnCount(2)

        for a, animal in enumerate(animal_list.keys()):
            id = QtWidgets.QTableWidgetItem(animal_list[animal].id)
            water = QtWidgets.QTableWidgetItem(str(animal_list[animal].water))
            self.animalTable.setItem(a, 0, id)
            self.animalTable.setItem(a, 1, water)

    def current_animal(self):
        try:
            row = self.animalTable.selectedIndexes()[0].row()
            animal = self.parent.experiment.animal_list[self.animalTable.item(row, 0).text()]
            return animal
        except:
            return None

    def current_sched_index(self):
        try:
            row = self.scheduleTable.selectedIndexes()[0].row()
            return row
        except:
            return 0

    def update_animals(self):
        for row in range(self.animalTable.rowCount()):
            id = self.animalTable.item(row, 0).text()
            water = float(self.animalTable.item(row, 1).text())

            self.parent.experiment.add_mouse(id, water)

    def animal_selected(self):
        animal = self.current_animal()
        if animal is not None:
            self.scheduleTable.setRowCount(len(animal.schedule_list))
            self.scheduleTable.setColumnCount(3)

            for s, schedule in enumerate(animal.schedule_list):
                sched_name = QtWidgets.QTableWidgetItem(schedule.id)
                n_trials = QtWidgets.QTableWidgetItem(str(len(schedule.schedule_trials)))

                self.scheduleTable.setItem(s, 0, sched_name)
                self.scheduleTable.setItem(s, 1, n_trials)

    def schedule_selected(self):
        animal = self.current_animal()
        schedule = animal.schedule_list[self.current_sched_index()]

        self.trialView.setModel(GuiModels.TableModel(schedule.schedule_headers, schedule.schedule_trials, parent=self))

    def add_schedule(self):
        animal = self.current_animal()
        if animal is not None:
            fname, suff = QtWidgets.QFileDialog.getOpenFileName(self, "Load Schedule", '', '*.schedule')
            with open(fname, 'rb') as fn:
                schedule_data = pickle.load(fn)

            animal.schedule_list.append(Experiment.Schedule(os.path.basename(fname), schedule_data['schedule'], schedule_data['headers']))

            self.animal_selected()
