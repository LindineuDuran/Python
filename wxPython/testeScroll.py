import wx
import wx.lib.scrolledpanel as scrolled

text = '''
        ScrolledPanel extends wx.ScrolledWindow, adding all
        the necessary bits to set up scroll handling for you.

        Here are three fixed size examples of its use. The
        demo panel for this sample is also using it -- the
        wx.StaticLine below is intentionally made too long so a scrollbar will be
        activated.

        ScrolledPanel extends wx.ScrolledWindow, adding all
        the necessary bits to set up scroll handling for you.

        Here are three fixed size examples of its use. The
        demo panel for this sample is also using it -- the
        wx.StaticLine below is intentionally made too long so a scrollbar will be
        activated.'''

class TestPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(1800,200), pos=(0,0))

        vbox = wx.BoxSizer(wx.VERTICAL)

        desc = wx.StaticText(self, -1, text)

        # img = wx.Image(r'C:\Users\lindineu.duran\Documents\Python\Scrollable QLabel image in PyQt5\Luminous Space.jpg', wx.BITMAP_TYPE_ANY)
        # self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

        vbox.Add(desc, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(wx.StaticLine(self, -1, size=(1024, -1)), 0, wx.ALL, 5)
        vbox.Add((20, 20))

        # vbox.Add(self.imageCtrl, 0, wx.ALL, 5)

        self.SetSizer(vbox)
        self.SetupScrolling()


app = wx.App(0)
frame = wx.Frame(None, wx.ID_ANY)
fa = TestPanel(frame)
frame.Show()
app.MainLoop()
