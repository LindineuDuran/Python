import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication)
import pandas as pd
import numpy as np
import PyQt5
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QGroupBox, QHBoxLayout, QMainWindow, QApplication, QLineEdit, QFileDialog,  QTableWidget,QTableWidgetItem, QTableView, QStyledItemDelegate
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtGui import QIcon
import re

def dataframe():
    lst = [['tom', 'reacher', 'True', 12, 4, 5, None, 1],
           ['krish', 'pete', 'True', 7, 2, 54, 3, None],
           ['nick', 'wilson', 'True', 20, 16, 11, 3, 8],
           ['juli', 'williams', 'True', 14, 3, None, 2, 6]]
    df = pd.DataFrame(lst, columns =['FName', 'LName', 'Student?','Nota1', 'Nota2', 'Nota3', 'Nota4', 'Nota5'])
    return df

class Delegate(QtWidgets.QItemDelegate):
    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices

    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QComboBox(parent)
        self.editor.currentIndexChanged.connect(self.commit_editor)
        self.editor.addItems(self.items)
        return self.editor

    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

    def commit_editor(self):      ####test
        editor = self.sender()
        self.commitData.emit(editor)


    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            row = index.row()
            col = index.column()
            self._data.iloc[row,col] = value
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))
            return True
        return False

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 200 ,480, 250)
        self.setWindowTitle('Test')
        self.initUI()

    def show_data(self):
        choices = ['True', 'False']
        self.model = PandasModel(dataframe())
        self.table_data.setModel(self.model)
        self.table_data.setItemDelegateForColumn(2, Delegate(self,choices))

        ##make combo boxes editable with a single-click:
        for row in range(5):
            self.table_data.openPersistentEditor(self.model.index(row, 2))

        self.table_data.resizeColumnsToContents()

    def print_data(self):
        # Print the DataFrame
        print(self.table_data.model()._data)

        # return the dtype of each column
        result = dataframe().dtypes

        # Print the result
        print(result)

    def initUI(self):

        welcom = QLabel('Welcome to my app!')

        self.btn_print_data = QPushButton('print data')
        self.btn_print_data.clicked.connect(self.print_data)  ##test

        self.btn_show_table = QPushButton('show data')
        self.btn_show_table.clicked.connect(self.show_data)

        self.table_data = QTableView()
        self.table_data.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(welcom)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.btn_show_table)
        vbox2.addWidget(self.btn_print_data) ####test

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.table_data)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox3)

        vbox1 = QVBoxLayout()
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)

        self.setLayout(vbox1)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())
