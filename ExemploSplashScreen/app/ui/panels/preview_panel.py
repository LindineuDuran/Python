
import wx
class PreviewPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent)
        self.bmp=wx.StaticBitmap(self)
    def show_image(self,path):
        img=wx.Image(path).Scale(300,300)
        self.bmp.SetBitmap(wx.Bitmap(img))
