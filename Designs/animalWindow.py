# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/AnimalWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(771, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.animalTable = QtWidgets.QTableWidget(self.centralwidget)
        self.animalTable.setObjectName("animalTable")
        self.animalTable.setColumnCount(2)
        self.animalTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.animalTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.animalTable.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.animalTable, 0, 0, 3, 1)
        self.addRowButton = QtWidgets.QPushButton(self.centralwidget)
        self.addRowButton.setObjectName("addRowButton")
        self.gridLayout.addWidget(self.addRowButton, 0, 1, 1, 1)
        self.removeRowButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeRowButton.setObjectName("removeRowButton")
        self.gridLayout.addWidget(self.removeRowButton, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 2, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 21))
        self.menubar.setObjectName("menubar")
        self.menuUpdate_List = QtWidgets.QMenu(self.menubar)
        self.menuUpdate_List.setObjectName("menuUpdate_List")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionUpdate = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.menuUpdate_List.addAction(self.actionUpdate)
        self.menubar.addAction(self.menuUpdate_List.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.animalTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.animalTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Water Reward"))
        self.addRowButton.setText(_translate("MainWindow", "+"))
        self.removeRowButton.setText(_translate("MainWindow", "-"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Schedule Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Number of Trials"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Progress"))
        self.menuUpdate_List.setTitle(_translate("MainWindow", "Update List"))
        self.actionUpdate.setText(_translate("MainWindow", "Confirm"))

