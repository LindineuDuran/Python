# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frm_youtube_downloader.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 150)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Youtube.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("Youtube.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.linkLabel = QtWidgets.QLabel(self.centralwidget)
        self.linkLabel.setGeometry(QtCore.QRect(20, 10, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.linkLabel.setFont(font)
        self.linkLabel.setObjectName("linkLabel")
        self.urlText = QtWidgets.QLineEdit(self.centralwidget)
        self.urlText.setGeometry(QtCore.QRect(20, 30, 460, 20))
        self.urlText.setObjectName("urlText")
        self.destinyLabel = QtWidgets.QLabel(self.centralwidget)
        self.destinyLabel.setGeometry(QtCore.QRect(20, 60, 91, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.destinyLabel.setFont(font)
        self.destinyLabel.setLineWidth(17)
        self.destinyLabel.setObjectName("destinyLabel")
        self.destinyText = QtWidgets.QLineEdit(self.centralwidget)
        self.destinyText.setGeometry(QtCore.QRect(20, 80, 425, 20))
        self.destinyText.setObjectName("destinyText")
        self.folderButton = QtWidgets.QToolButton(self.centralwidget)
        self.folderButton.setGeometry(QtCore.QRect(455, 80, 25, 23))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderButton.setIcon(icon1)
        self.folderButton.setObjectName("folderButton")
        self.downloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton.setGeometry(QtCore.QRect(310, 115, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.downloadButton.setFont(font)
        self.downloadButton.setObjectName("downloadButton")
        self.videoButton = QtWidgets.QRadioButton(self.centralwidget)
        self.videoButton.setGeometry(QtCore.QRect(20, 118, 50, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.videoButton.setFont(font)
        self.videoButton.setChecked(True)
        self.videoButton.setObjectName("videoButton")
        self.audioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.audioButton.setGeometry(QtCore.QRect(105, 118, 51, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.audioButton.setFont(font)
        self.audioButton.setObjectName("audioButton")
        self.apagaVideoBox = QtWidgets.QCheckBox(self.centralwidget)
        self.apagaVideoBox.setGeometry(QtCore.QRect(190, 118, 95, 17))
        self.apagaVideoBox.setObjectName("apagaVideoBox")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(405, 115, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube Downloader"))
        self.linkLabel.setText(_translate("MainWindow", "URL link:"))
        self.destinyLabel.setText(_translate("MainWindow", "File Destination:"))
        self.folderButton.setText(_translate("MainWindow", "..."))
        self.downloadButton.setText(_translate("MainWindow", "Download"))
        self.videoButton.setText(_translate("MainWindow", "Video"))
        self.audioButton.setText(_translate("MainWindow", "Audio"))
        self.apagaVideoBox.setText(_translate("MainWindow", "Apagar Vídeo"))
        self.cancelButton.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())