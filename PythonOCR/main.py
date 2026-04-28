import wx
from ui.main_frame import MainFrame
from controllers.app_controller import AppController
from services.ocr_service import OCRService

app = wx.App()
frame = MainFrame(None, title="Reconhecimento Ótico de Caracteres",size=(800,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

ocr = OCRService()
controller = AppController(frame, ocr)

frame.Show()
app.MainLoop()