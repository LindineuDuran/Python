import wx
import threading

class Command:
    def execute(self):
        pass


class OpenDirectoryCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        dlg = wx.DirDialog(self.controller.frame, "Escolha pasta")
        if dlg.ShowModal() == wx.ID_OK:
            self.controller.load_directory(dlg.GetPath())

class SaveOCRResultCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        """Pega texto obtido"""
        value = self.controller.frame.txt_output.GetValue()

        """Browse for directory"""
        fdlg = wx.FileDialog(None, "Entre com o caminho para o arquivo de resultado", "", "", "text files(*.txt)|*.*", wx.FD_SAVE)

        if fdlg.ShowModal() == wx.ID_OK:
            self.save_path = fdlg.GetPath() + ".txt"

            ocrFile = open(self.save_path, 'w', encoding="utf-8")
            ocrFile.write(value+'\r\n')
            ocrFile.close()

        fdlg.Destroy()

class ExitCommand(Command):
    def __init__(self, frame):
        self.frame = frame

    def execute(self):
        """Close the frame, terminating the application."""
        self.frame.Close(True)


class OCRCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        threading.Thread(target=self.controller.run_ocr).start()


class ClearTextCommand(Command):
    def __init__(self, frame):
        self.frame = frame

    def execute(self):
        self.frame.txt_output.SetValue("")

class RotateRightCommand(Command):
    def __init__(self, frame):
        self.frame = frame

    def execute(self):
        self.frame.image_panel.rotate_right()


class RotateLeftCommand(Command):
    def __init__(self, frame):
        self.frame = frame

    def execute(self):
        self.frame.image_panel.rotate_left()

class ZoomInCommand(Command):
    def __init__(self, frame):
        self.frame = frame

    def execute(self):
        self.frame.image_panel.zoom_in()


class ZoomOutCommand(Command):
    def __init__(self, frame):
        self.frame = frame

    def execute(self):
        self.frame.image_panel.zoom_out()


class AboutCommand(Command):
    def execute(self):
        wx.MessageBox("OCR Pro - versão profissional", "Sobre")