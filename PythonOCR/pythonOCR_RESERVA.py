# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pythonOCR.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image # Importando o módulo Pillow para abrir a imagem no script
import pytesseract # Módulo para a utilização da tecnologia OCR


class Ui_PythonOCR(object):
    def setupUi(self, PythonOCR):
        PythonOCR.setObjectName("PythonOCR")
        PythonOCR.resize(400, 300)
        
        self.centralwidget = QtWidgets.QWidget(PythonOCR)
        self.centralwidget.setObjectName("centralwidget")
        
        self.imageLbl = QtWidgets.QLabel(self.centralwidget)
        self.imageLbl.setGeometry(QtCore.QRect(5, 0, 390, 150))
        self.imageLbl.setFrameShape(QtWidgets.QFrame.Box)
        self.imageLbl.setText("")
        self.imageLbl.setObjectName("imageLbl")
        
        self.plainTextEditResult = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEditResult.setGeometry(QtCore.QRect(5, 160, 390, 90))
        self.plainTextEditResult.setObjectName("plainTextEditResult")
        PythonOCR.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(PythonOCR)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 20))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        PythonOCR.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(PythonOCR)
        self.statusbar.setObjectName("statusbar")
        
        self._statusbar_label = QtWidgets.QLabel("status")
        self._statusbar_label.setText("")
        
        self.statusbar.addPermanentWidget(self._statusbar_label)
        PythonOCR.setStatusBar(self.statusbar)
        
        self.actionSelect_Image = QtWidgets.QAction(PythonOCR)
        self.actionSelect_Image.setObjectName("actionSelect_Image")
        self.actionGet_Text = QtWidgets.QAction(PythonOCR)
        self.actionGet_Text.setObjectName("actionGet_Text")
        self.actionExit = QtWidgets.QAction(PythonOCR)
        self.actionExit.setObjectName("actionExit")
        self.actionClear_Text = QtWidgets.QAction(PythonOCR)
        self.actionClear_Text.setObjectName("actionClear_Text")
        self.menu.addAction(self.actionSelect_Image)
        self.menu.addAction(self.actionGet_Text)
        self.menu.addAction(self.actionClear_Text)
        self.menu.addAction(self.actionExit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(PythonOCR)
        QtCore.QMetaObject.connectSlotsByName(PythonOCR)

        self.actionSelect_Image.triggered.connect(self.setImage)
        self.actionGet_Text.triggered.connect(self.getText)
        self.actionClear_Text.triggered.connect(self.clearText)

    def retranslateUi(self, PythonOCR):
        _translate = QtCore.QCoreApplication.translate
        PythonOCR.setWindowTitle(_translate("PythonOCR", "PythonOCR"))
        self.menu.setTitle(_translate("PythonOCR", "Actions"))
        self.actionSelect_Image.setText(_translate("PythonOCR", "Select Image"))
        self.actionGet_Text.setText(_translate("PythonOCR", "Get Text"))
        self.actionExit.setText(_translate("PythonOCR", "Exit"))
        self.actionClear_Text.setText(_translate("PythonOCR", "Clear Text"))

    def setImage(self):
        global image
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)") # Ask for file
        if fileName: # If the user gives a file
            self._statusbar_label.setText(fileName)
            image = Image.open(fileName)
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.imageLbl.width(), self.imageLbl.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.imageLbl.setPixmap(pixmap) # Set the pixmap onto the label
            self.imageLbl.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center

    def getText(self):
        value = pytesseract.image_to_string(image)
        self.plainTextEditResult.insertPlainText(value)

    def clearText(self):
        self.plainTextEditResult.clear() # Clear the text

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PythonOCR = QtWidgets.QMainWindow()
    ui = Ui_PythonOCR()
    ui.setupUi(PythonOCR)
    PythonOCR.show()
    sys.exit(app.exec_())
