import sys, os, subprocess
from PyQt5 import uic, QtWidgets as qtw
from PyQt5.QtCore import Qt
from pytube import YouTube

app_path = os.path.dirname(os.path.abspath(__file__))
ffmpeg = os.path.join(app_path, 'ffmpeg-2022-12-21-git-eef763c705-full_build', 'bin', 'ffmpeg.exe')

class Ui_MainWindow(qtw.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.showdialog("Info!!!", "Diretório do App: " + app_path)
        uic.loadUi(os.path.join(app_path,'frm_youtube_downloader.ui'), self)

        # File destination
        self.destinyText.setText("D:\\Downloads")

        # buttons
        self.folderButton.clicked.connect(self.selectDir)
        self.downloadButton.clicked.connect(self.download)
        self.cancelButton.clicked.connect(qtw.QApplication.quit)    

    def showdialog(self, title, mensagem):
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Information)
        
        msg.setText(mensagem)
        msg.setWindowTitle(title)
        msg.setStandardButtons(qtw.QMessageBox.Ok)
        msg.buttonClicked.connect(self.msgbtn)

        retval = msg.exec_()

    def msgbtn(self, i):
        print ("Button pressed is:",i.text())

    # Seleciona local aonde arquivo será salvo
    def selectDir(self):
        selected_dir = qtw.QFileDialog.getExistingDirectory(self, caption='Choose Directory', directory=os.getcwd())

        if selected_dir != '':
            self.destinyText.setText(selected_dir)

    def obtem_path(self):
        path = self.destinyText.text()
        return path

    def downloadVideo(self, link):
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_highest_resolution()

        try:
            path = self.obtem_path()
            video_name = youtubeObject.default_filename
            youtubeObject.download(output_path=path)
        except:
            self.showdialog("Except!!!", "There has been an error in downloading your youtube video")

        return video_name

    def downloadAudio(self, link):
        youtubeObject = YouTube(link)
        path = self.obtem_path()
        audio = youtubeObject.streams.get_audio_only()
        audio.download(output_path=path)
        
        audio_name = audio.default_filename
        return audio_name

    def normaliza_file_name(self, file_name):
        if ' ' in file_name:
            file_name = file_name.replace(' ','_')

        return file_name

    def audioToMp3(self, audio_name):
        path = self.obtem_path()
        source =  os.path.join(path, audio_name)

        if ' ' in audio_name:
            os.rename(source, source.replace(' ', '_'))
            audio_name = self.normaliza_file_name(source)

        file_without_ext = os.path.splitext(audio_name)[0]

        result = subprocess.run([ffmpeg, '-i', audio_name, file_without_ext + '.mp3'], shell = True, check = True)

    def download(self):
        link = self.urlText.text()

        if self.videoButton.isChecked():
            video_name = self.downloadVideo(link)

            self.showdialog("Info!!!", "Fim do processo!")
            
            return video_name

        audio_name = self.downloadAudio(link)
        self.audioToMp3(audio_name)

        if self.audioButton.isChecked() and self.apagaVideoBox.isChecked():
            path = self.obtem_path()
            audio_name = self.normaliza_file_name(audio_name)
            os.remove(os.path.join(path, audio_name))        

        self.showdialog("Info!!!", "Fim do processo!")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
