import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):
    application_path = ''

    def __init__(self):
        super().__init__()

        """Guarda o Diretório da Aplicação"""
        self.application_path = os.getcwd()

        self.table = QtWidgets.QTableView()

        # Read the CSV into a pandas data frame (df)
        #   With a df you can do many things
        #   most important: visualize data with Seaborn
        path_to_file = os.path.join(self.application_path, 'TextoExtraido.txt')
        df = pd.read_csv(path_to_file, delimiter=';')

        self.model = TableModel(df)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
