import sys
import os
from PyQt5 import uic, QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PIL import Image  # Importando o módulo Pillow para abrir a imagem no script
import pytesseract  # Módulo para a utilização da tecnologia OCR

app_path = os.path.dirname(os.path.abspath(__file__))
tesseract_path = os.path.join(app_path, 'Tesseract-OCR', 'tesseract.exe')
tessdata = os.path.join(app_path, 'Tesseract-OCR', 'tessdata')

if os.path.exists(tesseract_path):
    #pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    #tessdata_dir_config = r'--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
    tessdata_dir_config = '--tessdata-dir ' + tessdata

class PythonOCR(qtw.QMainWindow):
    # Configura interface
    def __init__(self):
        super().__init__()

        width_tela = 800
        height_tela = 600
        self.setObjectName("PythonOCR")
        self.resize(width_tela, height_tela)
        self.setWindowTitle("PythonOCR")

        self.centralwidget = qtw.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        posX_img = 5
        posY_img = 0
        width_img = 790
        height_img = 300

        self.imageLbl = qtw.QLabel()
        self.imageLbl.setBackgroundRole(qtg.QPalette.Base)
        self.imageLbl.setGeometry(qtc.QRect(posX_img, posY_img, width_img, height_img))
        self.imageLbl.setSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Ignored)
        self.imageLbl.setScaledContents(True)
        self.imageLbl.setObjectName("imageLbl")

        self.scrollArea = qtw.QScrollArea(self.centralwidget)
        self.scrollArea.setBackgroundRole(qtg.QPalette.Dark)
        self.scrollArea.setGeometry(qtc.QRect(posX_img, posY_img, width_img, height_img))
        self.scrollArea.setWidget(self.imageLbl)
        self.scrollArea.setVisible(False)

        posX_txt = 5
        posY_txt = 305
        width_txt = 790
        height_txt = 270
        self.plainTextEditResult = qtw.QPlainTextEdit(self.centralwidget)
        self.plainTextEditResult.setGeometry(qtc.QRect(posX_txt, posY_txt, width_txt, height_txt))
        self.plainTextEditResult.setObjectName("plainTextEditResult")

        self.setCentralWidget(self.centralwidget)

        self.createActions()
        self.createMenus()

    def createActions(self):
        self.openAct = qtw.QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.exitAct = qtw.QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)

        self.getAct = qtw.QAction("&Get Text", self, shortcut="Ctrl+G", triggered=self.getText)
        self.cleanAct = qtw.QAction("C&lean Text", self, shortcut="Ctrl+.", triggered=self.clearText)

        self.zoomInAct = qtw.QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = qtw.QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = qtw.QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = qtw.QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        # self.aboutAct = qtw.QAction("&About", self, triggered=self.about)
        # self.aboutQtAct = qtw.QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = qtw.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = qtw.QMenu("&Edit", self)
        self.editMenu.addAction(self.getAct)
        self.editMenu.addAction(self.cleanAct)

        self.viewMenu = qtw.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = qtw.QMenu("&Help", self)
    #     # self.helpMenu.addAction(self.aboutAct)
    #     # self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.editMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def open(self):
        global image
        options = qtw.QFileDialog.Options()
        fileName, _ = qtw.QFileDialog.getOpenFileName(self, 'qtw.QFileDialog.getOpenFileName()', '',
                                                            'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            image = Image.open(fileName)
            pixMap = qtg.QPixmap(fileName)

            self.imageLbl.setPixmap(pixMap)  # Set the pixmap onto the label
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLbl.adjustSize()

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLbl.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLbl.resize(self.scaleFactor * self.imageLbl.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.1)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def getText(self):
        value = pytesseract.image_to_string(image)
        self.plainTextEditResult.insertPlainText(value + "\r\n")

    def clearText(self):
        self.plainTextEditResult.clear()  # Clear the text


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    pythonOCR = PythonOCR()
    pythonOCR.show()
    sys.exit(app.exec_())
    # TODO QScrollArea support mouse
