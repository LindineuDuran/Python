from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
import wx
from app.ui.menu_factory import MenuFactory
from app.ui.components import AdvancedImagePanel, ThumbnailPanel

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        # ensure the parent's __init__ is called
        super().__init__(*args, **kwargs)

        # Make the menu bar and add the menus to it.
        self.menu = MenuFactory(self)
        self.menu.create()
                
        # Make the status bar.
        self.CreateStatusBar(2)
        #self.SetStatusWidths([200, 500, 50, 50, 30])
        self.SetStatusWidths([200, 500])

        self.panel = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.thumbnail = ThumbnailPanel(self.panel, self.on_thumb)
        self.image_panel = AdvancedImagePanel(self.panel)

        sizer_1.Add(self.thumbnail, 0, wx.EXPAND)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        sizer_2.Add(self.image_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.txt_output = wx.TextCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        sizer_2.Add(self.txt_output, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(sizer_1)

        self.Layout()

    def set_status(self, message, field=0):
        self.SetStatusText(message, field)

    def set_status_temp(self, message, timeout=3000):
        self.SetStatusText(message, 0)
        wx.CallLater(timeout, lambda: self.SetStatusText("", 0))
        
    def on_thumb(self, index):
        pass