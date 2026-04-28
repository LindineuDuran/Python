import os
import wx
from core.commands import *
from ui.menu_factory import MenuFactory
from ui.drag_drop import FileDropTarget

class AppController:
    def __init__(self, frame, ocr):
        self.frame = frame
        self.ocr = ocr

        self.menu = MenuFactory(frame)
        self.menu.create()

        self.commands = {
            "open": OpenDirectoryCommand(self),
            "save": SaveOCRResultCommand(self),
            "exit": ExitCommand(frame),
            "ocr": OCRCommand(self),
            "clear": ClearTextCommand(frame),
            "rotate_left": RotateLeftCommand(frame),
            "rotate_right": RotateRightCommand(frame),
            "zoom_in": ZoomInCommand(frame),
            "zoom_out": ZoomOutCommand(frame),
            "about": AboutCommand()
        }

        self.menu.bind(self.commands)

        self.frame.thumbnail.callback = self.on_thumbnail
        self.frame.image_panel.on_selection = self.on_selection
        self.frame.image_panel.on_image_change = self.on_thumbnail

        self.frame.on_thumb = self.on_thumbnail

        drop = FileDropTarget(self.on_drop)
        self.frame.SetDropTarget(drop)

    def load_directory(self, directory):
        self.directory = directory

        self.images = [
            f for f in os.listdir(directory)
            if f.lower().endswith(('png','jpg','jpeg','bmp'))
        ]

        self.frame.image_panel.load_directory(directory)
        self.frame.thumbnail.load_images(directory, self.images)

        if self.images:
            self.frame.thumbnail.select(0)

    def on_thumbnail(self, index):
        # muda índice
        self.frame.image_panel.imageIndx = index

        # carrega imagem
        self.frame.image_panel.scale = 1.0
        self.frame.image_panel.rotation = 0
        self.frame.image_panel.load_current_image()

        # atualiza seleção visual
        self.frame.thumbnail.select(index)

    def on_drop(self, files):
        if len(files) == 1 and os.path.isdir(files[0]):
            self.load_directory(files[0])
        else:
            self.directory = os.path.dirname(files[0])
            self.images = [os.path.basename(f) for f in files]

            self.frame.image_panel.imageList = self.images
            self.frame.image_panel.directory = self.directory
            self.frame.image_panel.imageIndx = 0

            # 🔥 RESET
            self.frame.image_panel.scale = 1.0
            self.frame.image_panel.rotation = 0

            self.frame.image_panel.load_current_image()

            self.frame.thumbnail.load_images(self.directory, self.images)

            if self.images:
                self.frame.thumbnail.select(0)

    def run_ocr(self):
        path = self.frame.image_panel.get_current_image_path()
        if not path:
            return

        text = self.frame.txt_output.GetValue()
        text += self.ocr.extract_text(path, rotation=self.frame.image_panel.rotation)
        wx.CallAfter(self.frame.txt_output.SetValue, text)

    def on_selection(self, rect):
        path = self.frame.image_panel.get_current_image_path()
        text = self.frame.txt_output.GetValue()
        text += self.ocr.extract_region(path, rect, rotation=self.frame.image_panel.rotation)
        self.frame.txt_output.SetValue(text)