
import wx
class ProgressBar(wx.Gauge):
    def __init__(self,parent):
        super().__init__(parent,range=100)
