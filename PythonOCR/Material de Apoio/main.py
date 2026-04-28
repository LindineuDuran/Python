import wx
from ui.main_frame import MainFrame
from controllers.app_controller import AppController
from services.ocr_service import OCRService
from services.image_service import ImageService

app = wx.App()

frame = MainFrame()

ocr = OCRService()
img_service = ImageService()

controller = AppController(frame, ocr, img_service)

frame.Show()
app.MainLoop()