# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:48:23 2020

@author: lindineu.duran
"""

import os
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        """Guarda o Diretório da Aplicação"""
        self.aplication_path = os.getcwd()
        aqr_icon = os.path.join(self.aplication_path, 'images', 'icons', 'door-open-out.png')

        qbtn = QPushButton(QIcon(aqr_icon), 'Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.move(80, 50)

        self.setGeometry(300, 300, 250, 150)
        self.show()


def fun():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

fun()
