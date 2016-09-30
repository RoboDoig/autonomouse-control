from PyQt5 import QtWidgets, QtGui
from Designs import animalWindow


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

        self.animalTable.selectionModel().selectionChanged.connect(self.animal_selected)

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

    def update_animals(self):
        for row in range(self.animalTable.rowCount()):
            id = self.animalTable.item(row, 0).text()
            water = float(self.animalTable.item(row, 1).text())

            self.parent.experiment.add_mouse(id, water)

    def animal_selected(self):
        try:
            row = self.animalTable.selectedIndexes()[0].row()
            animal = self.parent.experiment.animal_list[self.animalTable.item(row, 0).text()]
            print(animal)
        except:
            pass
