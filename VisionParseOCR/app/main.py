from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
import os, wx
import time
import threading

from app.ui.main_frame import MainFrame
from app.ui.splash_screen import SplashScreen
from app.services.pdf.pymupdf_service import PDFService
from app.services.ocr.ocr_service import OCRService
from app.controllers.app_controller import AppController

class App(wx.App):

    def OnInit(self):
        # self.app_path = os.path.dirname(os.path.abspath(__file__))
        # logger.debug("App Path: %s", self.app_path)

        self.splash = SplashScreen()
        self.splash.Show()

        threading.Thread(target=self.load_app).start()

        return True

    def load_app(self):
        steps = 2

        def step(i, msg=None):
            progress = int((i / steps) * 100)
            self.splash.update_progress(progress)
            time.sleep(1.0)

        # Simula carga (pode colocar inicializações reais aqui)
        step(1)
        pdf = PDFService()

        step(2)
        ocr = OCRService()

        services = {
            "pdf": pdf,
            "ocr": ocr
        }

        wx.CallAfter(self.start_main_app, services)

    def start_main_app(self, services):
        frame = MainFrame(None, title="Reconhecimento Ótico de Caracteres",size=(800,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        controller = AppController(frame, services['pdf'], services['ocr'])

        frame.Show()
        self.splash.Destroy()


if __name__ == "__main__":
    app = App()
    app.MainLoop()