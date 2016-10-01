# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/PrefsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.savePathEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.savePathEdit.setObjectName("savePathEdit")
        self.gridLayout.addWidget(self.savePathEdit, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.savePathButton = QtWidgets.QPushButton(self.centralwidget)
        self.savePathButton.setObjectName("savePathButton")
        self.gridLayout.addWidget(self.savePathButton, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.experimentNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.experimentNameEdit.setObjectName("experimentNameEdit")
        self.gridLayout.addWidget(self.experimentNameEdit, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_Preferences = QtWidgets.QAction(MainWindow)
        self.actionSave_Preferences.setObjectName("actionSave_Preferences")
        self.menuFile.addAction(self.actionSave_Preferences)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Preferences"))
        self.label.setText(_translate("MainWindow", "Save Path"))
        self.savePathButton.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "Experiment Name"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave_Preferences.setText(_translate("MainWindow", "Save Preferences"))

