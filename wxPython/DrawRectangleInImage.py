import wx

class window (wx.Frame):
    def __init__ (self, parent, id):
        wx.Frame.__init__ (self, parent, id, "Solitair", size = (1200, 800))
        self.panel = wx.Panel(self)
        img = r'C:\Users\lindineu.duran\Documents\Python\Scrollable QLabel image in PyQt5\Luminous Space.jpg'
        self.bmp = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self.panel, -1, self.bmp)
        self.drowRec(None)

    def drowRec(self, event):
        dc = wx.MemoryDC(self.bmp)
        dc.SetPen(wx.Pen('green', 5, wx.SOLID))
        dc.SetBrush(wx.Brush('green', wx.TRANSPARENT))
        dc.DrawRectangle(20, 20, 60, 60)
        del dc
        self.bitmap.SetBitmap(self.bmp)

app = wx.App(False)
frame = window(None, -1)
frame.Show()
app.MainLoop()
