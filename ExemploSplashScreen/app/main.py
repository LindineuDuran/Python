# app/main.py

import wx
import time
import threading

from app.ui.main_frame import MainFrame
from app.ui.splash_screen import SplashScreen
from app.controllers.app_controller import AppController
from app.services.pdf_service import PDFService
from app.services.ocr_service import OCRService
from app.services.classification_service import ClassificationService
from app.services.export_service import ExportService
from app.services.cache_service import CacheService


class App(wx.App):

    def OnInit(self):

        self.splash = SplashScreen()
        self.splash.Show()

        threading.Thread(target=self.load_app).start()

        return True

    def load_app(self):
        steps = 4

        def step(i, msg=None):
            progress = int((i / steps) * 100)
            self.splash.update_progress(progress)
            time.sleep(0.3)

        # Simula carga (pode colocar inicializações reais aqui)
        step(1)
        pdf = PDFService()

        step(2)
        ocr = OCRService()

        step(3)
        classifier = ClassificationService()

        step(4)
        export = ExportService()

        step(5)
        cache = CacheService()

        services = {
            "pdf": pdf,
            "ocr": ocr,
            "classifier": classifier,
            "export": export,
            "cache": cache
        }

        wx.CallAfter(self.start_main_app, services)

    def start_main_app(self, services):
        frame = MainFrame()

        controller = AppController(frame, services)
        frame.set_controller(controller)

        frame.Show()
        self.splash.Destroy()