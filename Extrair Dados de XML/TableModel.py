from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt as qt

class TableModel(qtc.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == qt.DisplayRole or role == qt.EditRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # secton is the index of the column/row.
        if role == qt.DisplayRole:
            if orientation == qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == qt.Vertical:
                return str(self._data.index[section])

    def flags(self, index):
        return qt.ItemIsEnabled | qt.ItemIsSelectable | qt.ItemIsEditable

    def setData(self, index, value, role=qt.EditRole):
        if index.isValid():
            row = index.row()
            col = index.column()
            self._data.iloc[row,col] = value
            self.dataChanged.emit(index, index, (qt.DisplayRole, ))
            return True
        return False
