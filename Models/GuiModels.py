from PyQt5 import QtCore, QtGui


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, headerdata, arraydata, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.headerdata = headerdata
        self.arraydata = arraydata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.BackgroundRole:
            row = index.row()
            if self.arraydata[row][6]:
                return QtGui.QBrush(QtCore.Qt.green)
            else:
                return QtGui.QBrush(QtCore.Qt.red)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(str(self.arraydata[index.row()][index.column()]))

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return int(col)
        return QtCore.QVariant()