# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/HardwareWindow.ui'
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
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.digitalOutputEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.digitalOutputEdit.setObjectName("digitalOutputEdit")
        self.gridLayout.addWidget(self.digitalOutputEdit, 1, 1, 1, 1)
        self.digitalChannelsSpin = QtWidgets.QSpinBox(self.centralwidget)
        self.digitalChannelsSpin.setMinimum(1)
        self.digitalChannelsSpin.setMaximum(32)
        self.digitalChannelsSpin.setProperty("value", 8)
        self.digitalChannelsSpin.setObjectName("digitalChannelsSpin")
        self.gridLayout.addWidget(self.digitalChannelsSpin, 1, 4, 1, 1)
        self.syncClockEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.syncClockEdit.setObjectName("syncClockEdit")
        self.gridLayout.addWidget(self.syncClockEdit, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.analogInputEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.analogInputEdit.setObjectName("analogInputEdit")
        self.gridLayout.addWidget(self.analogInputEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.analogChannelsSpin = QtWidgets.QSpinBox(self.centralwidget)
        self.analogChannelsSpin.setMinimum(1)
        self.analogChannelsSpin.setMaximum(10)
        self.analogChannelsSpin.setProperty("value", 4)
        self.analogChannelsSpin.setObjectName("analogChannelsSpin")
        self.gridLayout.addWidget(self.analogChannelsSpin, 0, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Hardware Preferences"))
        self.label_5.setText(_translate("MainWindow", "Synchronisation Clock"))
        self.label_4.setText(_translate("MainWindow", "Digital Output Channels"))
        self.digitalOutputEdit.setText(_translate("MainWindow", "dev2/port0/line0:7"))
        self.syncClockEdit.setText(_translate("MainWindow", "/dev2/ai/SampleClock"))
        self.label.setText(_translate("MainWindow", "Analog Input Device"))
        self.analogInputEdit.setText(_translate("MainWindow", "dev2/ai0:3"))
        self.label_2.setText(_translate("MainWindow", "Analog Input Channels"))
        self.label_3.setText(_translate("MainWindow", "Digital Output Device"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave_Preferences.setText(_translate("MainWindow", "Save Preferences"))

