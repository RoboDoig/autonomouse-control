# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1123, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHardware = QtWidgets.QMenu(self.menubar)
        self.menuHardware.setObjectName("menuHardware")
        self.menuAnimals = QtWidgets.QMenu(self.menubar)
        self.menuAnimals.setObjectName("menuAnimals")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHardware_Preferences = QtWidgets.QAction(MainWindow)
        self.actionHardware_Preferences.setObjectName("actionHardware_Preferences")
        self.actionAnimal_List = QtWidgets.QAction(MainWindow)
        self.actionAnimal_List.setObjectName("actionAnimal_List")
        self.actionSave_Experiment = QtWidgets.QAction(MainWindow)
        self.actionSave_Experiment.setObjectName("actionSave_Experiment")
        self.actionLoad_Experiment = QtWidgets.QAction(MainWindow)
        self.actionLoad_Experiment.setObjectName("actionLoad_Experiment")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFile.addAction(self.actionSave_Experiment)
        self.menuFile.addAction(self.actionLoad_Experiment)
        self.menuFile.addAction(self.actionPreferences)
        self.menuHardware.addAction(self.actionHardware_Preferences)
        self.menuAnimals.addAction(self.actionAnimal_List)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHardware.menuAction())
        self.menubar.addAction(self.menuAnimals.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutonoMouse"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHardware.setTitle(_translate("MainWindow", "Hardware"))
        self.menuAnimals.setTitle(_translate("MainWindow", "Animals"))
        self.actionHardware_Preferences.setText(_translate("MainWindow", "Hardware Preferences"))
        self.actionAnimal_List.setText(_translate("MainWindow", "Animal List"))
        self.actionSave_Experiment.setText(_translate("MainWindow", "Save Experiment"))
        self.actionLoad_Experiment.setText(_translate("MainWindow", "Load Experiment"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))

