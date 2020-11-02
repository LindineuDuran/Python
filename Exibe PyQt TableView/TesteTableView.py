import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Table(QWidget):
    def __init__(self,parent=None):
        super(Table, self).__init__(parent)
        #Set title and initial size
        self.setWindowTitle('Example of QTableView table view')
        self.resize(500,300)

        #Set the data hierarchy, 4 rows and 4 columns
        self.model=QStandardItemModel(4,4)
        #Set the text content of the four header labels in the horizontal direction
        self.model.setHorizontalHeaderLabels(['Title 1','Title 2','Title 3','Title 4'])

        # #Todo optimization 2 add data
        # self.model.appendRow([
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        # ])

        for row in range(4):
            for column in range(4):
                if column == 0:
                    item=QStandardItem('row %s,column %sAAAAA'%(row,column))
                else:
                    item=QStandardItem('row %s,column %s'%(row,column))

                #Set the text value of each position
                self.model.setItem(row,column,item)

        #Instantiate the table view, set the model to a custom model
        self.tableView=QTableView()
        self.tableView.setModel(self.model)

        # #todo Optimization 1 Form fills the window
        # #Horizontal label expands the rest of the window and fills the form
        self.tableView.horizontalHeader().setStretchLastSection(True)

        # #Horizontal direction, the table size expands to the appropriate size
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #
        # #TODO Optimization 3 Delete the currently selected data
        # indexs=self.tableView.selectionModel().selection().indexes()
        # print(indexs)
        # if len(indexs)>0:
        #     index=indexs[0]
        #     self.model.removeRows(index.row(),1)

        #Set layout
        layout=QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    table=Table()
    table.show()
    sys.exit(app.exec_())
