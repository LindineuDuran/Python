# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 10:11:48 2020

@author: lindineu.duran
"""
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    aplication_path = ''

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        """Guarda o Diretório da Aplicação"""
        self.aplication_path = os.getcwd()
        aqr_icon = os.path.join(self.aplication_path, 'images', 'icons', 'door-open-out.png')

        # exitAction = QAction(QIcon('datas/app/resources/images/exit.png'), '&Exit', self)
        exitAction = QAction(QIcon(aqr_icon), '&Exit', self)

        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QApplication.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
