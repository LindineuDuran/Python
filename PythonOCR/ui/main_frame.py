import wx
from ui.components import AdvancedImagePanel, ThumbnailPanel

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        self.thumbnail = ThumbnailPanel(panel, self.on_thumb)
        self.image_panel = AdvancedImagePanel(panel)
        self.txt_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        top = wx.BoxSizer(wx.HORIZONTAL)
        top.Add(self.thumbnail, 0, wx.EXPAND)
        top.Add(self.image_panel, 1, wx.EXPAND)

        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(top, 3, wx.EXPAND)
        main.Add(self.txt_output, 1, wx.EXPAND)

        panel.SetSizer(main)

    def on_thumb(self, index):
        pass