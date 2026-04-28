import os, wx
import time
import threading

from ui.main_frame import MainFrame
from ui.splash_screen import SplashScreen
from services.pdf.pymupdf_service import PDFService
from services.ocr.ocr_service import OCRService
from controllers.app_controller import AppController

# if __name__ == '__main__':
#     app_path = os.path.dirname(os.path.abspath(__file__))
#     #print("App Path:", app_path)

#     app = wx.App()
#     frame = MainFrame(None, title="Reconhecimento Ótico de Caracteres",size=(800,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
#     pdf = PDFService()
#     ocr = OCRService(app_path)
#     controller = AppController(frame, pdf, ocr)
#     frame.Show()
#     app.MainLoop()

class App(wx.App):

    def OnInit(self):

        self.splash = SplashScreen()
        self.splash.Show()

        threading.Thread(target=self.load_app).start()

        return True

    def load_app(self):
        steps = 5

        def step(i, msg=None):
            progress = int((i / steps) * 100)
            self.splash.update_progress(progress)
            time.sleep(0.3)

        # Simula carga (pode colocar inicializações reais aqui)
        step(1)
        pdf = PDFService()

        step(2)
        app_path = os.path.dirname(os.path.abspath(__file__))
        #print("App Path:", app_path)

        ocr = OCRService(app_path)

        services = {
            "pdf": pdf,
            "ocr": ocr
        }

        wx.CallAfter(self.start_main_app, services)

    def start_main_app(self, services):
        frame = MainFrame(None, title="Reconhecimento Ótico de Caracteres",size=(800,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        controller = AppController(frame, services['pdf'], services['ocr'])
        frame.set_controller(controller)

        frame.Show()
        self.splash.Destroy()


if __name__ == "__main__":
    app = App()
    app.MainLoop()