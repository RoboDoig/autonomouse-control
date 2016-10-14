# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/AnalysisWindow.ui'
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
        self.experimentStatsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.experimentStatsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.experimentStatsTable.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.experimentStatsTable.setObjectName("experimentStatsTable")
        self.experimentStatsTable.setColumnCount(2)
        self.experimentStatsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.experimentStatsTable, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Experiment Analysis"))
        item = self.experimentStatsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Animal"))
        item = self.experimentStatsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Total Trials"))

