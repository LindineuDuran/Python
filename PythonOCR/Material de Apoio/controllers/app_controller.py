import os
import wx
from core.commands import *
from ui.menu_factory import MenuFactory
from ui.drag_drop import FileDropTarget

class AppController:

    def __init__(self, frame, ocr, img):
        self.frame = frame
        self.ocr = ocr

        self.directory = ""
        self.images = []

        self.menu = MenuFactory(frame)
        self.menu.create()

        self.commands = {
            "open": OpenDirectoryCommand(self),
            "ocr": OCRCommand(self),
            "clear": ClearTextCommand(frame),
            "zoom_in": ZoomInCommand(frame),
            "zoom_out": ZoomOutCommand(frame),
            "about": AboutCommand()
        }

        self.menu.bind(self.commands)

        self.frame.on_thumb = self.on_thumbnail
        self.frame.image_panel.on_selection = self.on_selection
        self.frame.image_panel.on_image_change = self.on_thumbnail

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

        # 🔥 seleciona primeiro thumbnail
        if self.images:
            self.frame.thumbnail.select(0)

    def on_selection(self, rect):
        path = self.frame.image_panel.get_current_image_path()

        text = self.ocr.extract_from_region(path, rect)

        self.frame.txt_output.SetValue(text)

    def on_thumbnail(self, index):
        self.frame.image_panel.imageIndx = index
        self.frame.image_panel.load_current_image()

        self.frame.thumbnail.select(index)

    def on_drop(self, files):
        if len(files) == 1 and os.path.isdir(files[0]):
            # pasta
            self.load_directory(files[0])
        else:
            # múltiplas imagens
            self.directory = os.path.dirname(files[0])
            self.images = [os.path.basename(f) for f in files]

            self.frame.image_panel.imageList = self.images
            self.frame.image_panel.directory = self.directory
            self.frame.image_panel.imageIndx = 0

            # ✅ NOVO MÉTODO
            self.frame.image_panel.load_current_image()

            self.frame.thumbnail.load_images(self.directory, self.images)

            # 🔥 sincroniza seleção
            if self.images:
                self.frame.thumbnail.select(0)

    def run_ocr(self):
        path = self.frame.image_panel.get_current_image_path()
        if not path:
            return

        text = self.ocr.extract_text(path)
        wx.CallAfter(self.frame.txt_output.SetValue, text)