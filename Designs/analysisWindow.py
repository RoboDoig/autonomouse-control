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
        self.animalPerformanceView = PlotWidget(self.centralwidget)
        self.animalPerformanceView.setObjectName("animalPerformanceView")
        self.gridLayout.addWidget(self.animalPerformanceView, 2, 0, 1, 1)
        self.groupPerformanceView = PlotWidget(self.centralwidget)
        self.groupPerformanceView.setObjectName("groupPerformanceView")
        self.gridLayout.addWidget(self.groupPerformanceView, 2, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.binSizeSpin = QtWidgets.QSpinBox(self.groupBox)
        self.binSizeSpin.setMinimum(1)
        self.binSizeSpin.setMaximum(200)
        self.binSizeSpin.setProperty("value", 20)
        self.binSizeSpin.setObjectName("binSizeSpin")
        self.gridLayout_2.addWidget(self.binSizeSpin, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)
        self.experimentStatsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.experimentStatsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.experimentStatsTable.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.experimentStatsTable.setObjectName("experimentStatsTable")
        self.experimentStatsTable.setColumnCount(3)
        self.experimentStatsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.experimentStatsTable, 0, 0, 1, 2)
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
        self.actionExport_To_MATLAB = QtWidgets.QAction(MainWindow)
        self.actionExport_To_MATLAB.setObjectName("actionExport_To_MATLAB")
        self.menuFile.addAction(self.actionExport_To_MATLAB)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Experiment Analysis"))
        self.groupBox.setTitle(_translate("MainWindow", "Parameters"))
        self.label.setText(_translate("MainWindow", "Bin Size"))
        item = self.experimentStatsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Animal"))
        item = self.experimentStatsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Total Trials"))
        item = self.experimentStatsTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Trials in Last 24hrs"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExport_To_MATLAB.setText(_translate("MainWindow", "Export To MATLAB"))

from pyqtgraph import PlotWidget
