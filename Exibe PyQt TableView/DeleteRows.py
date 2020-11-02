#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QDialog, QComboBox, QApplication, QHeaderView
from PyQt5.QtCore import QPersistentModelIndex

class GUI(QDialog):

    def __init__(self):
        super(GUI, self).__init__()
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname,'DeleteRows.ui'), self)
        # buttons
        self.btnPopulate.clicked.connect(self.populate)
        self.btnDelete.clicked.connect(self.delete)
        self.btnExit.clicked.connect(QApplication.quit)

        # table model
        self.header = ['col1', 'col2', 'col3']
        self.QSModel = QStandardItemModel()
        self.QSModel.setColumnCount(3)
        self.QSModel.setHorizontalHeaderLabels(self.header)
        self.tableView.setModel(self.QSModel)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def populate(self):
        row = self.QSModel.rowCount()
        for x in range(7):
            self.QSModel.insertRow(row)
            self.QSModel.setData(self.QSModel.index(row, 0), 'data' + str(x))
            self.QSModel.item(row, 0).setEditable(True)
            self.QSModel.setData(self.QSModel.index(row, 1), 'data' + str(x))
            self.QSModel.item(row, 1).setEditable(True)
            self.QSModel.setData(self.QSModel.index(row, 2), 'data' + str(x))
            self.QSModel.item(row, 1).setEditable(True)

    def delete(self):
        if self.tableView.selectionModel().hasSelection():
            indexes =[QPersistentModelIndex(index) for index in self.tableView.selectionModel().selectedRows()]
            for index in indexes:
                print('Deleting row %d...' % index.row())
                self.QSModel.removeRow(index.row())
        else:
            print('No row selected!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
