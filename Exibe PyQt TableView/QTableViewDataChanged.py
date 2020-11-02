import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QTableView):
    def __init__(self, model):

        super().__init__()
        self.setModel(model)

class Model(QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

        self.source_data = [[0, 0, 0], [10, 10, 10]]

    @pyqtSlot()
    def tick(self):

        self.source_data[0][0] += 1
        self.source_data[0][1] += 1
        self.source_data[0][2] += 10
        self.source_data[1][2] += 10

        # Test 1 - this asks for a single cell and seems to work - (but for all roles?)
        #index_1 = self.index(0, 0)
        #index_2 = self.index(0, 0)
        #self.dataChanged.emit(index_1, index_2, [Qt.DisplayRole])

        # Test 2 - this always seems to ask for all data to be refreshed not just the two cells I said (again all roles)
        index_1 = self.index(0, 0)
        index_2 = self.index(0, 1)
        self.dataChanged.emit(index_1, index_2, [Qt.DisplayRole])

    def rowCount(self, parent_index=None):
        return 2

    def columnCount(self, parent_index=None):
        return 3

    @pyqtSlot()
    def data(self, index, role):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        print("Called for (%s, %s, %s)" % (row, col, role))

        if role == Qt.DisplayRole:
            return self.source_data[row][col]

        return None

    def headerData(self, col, orientation, role):
        return None


def main():
    app = QApplication(sys.argv)

    m = Model()
    w = Window(m)
    w.resize(250, 150)
    w.move(300, 300)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
