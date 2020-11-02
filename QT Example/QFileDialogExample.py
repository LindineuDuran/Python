# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 18:12:27 2020

@author: lindineu.duran
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
import os

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
     
    def initUI(self):
        qbtn = QPushButton('Selecionar Diretório', self)
        qbtn.clicked.connect(self.selectDir)
        qbtn.move(80, 50)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
     
    # Seleciona arquivo que será lido
    def selectDir(self):
        selected_dir = QFileDialog.getExistingDirectory(self, caption='Choose Directory', directory=os.getcwd())
        print(selected_dir)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
