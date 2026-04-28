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
        wx.MessageBox("OCR Pro - Arquitetura Profissional", "Sobre")