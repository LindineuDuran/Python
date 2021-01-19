# https://stackoverflow.com/questions/52184558/scale-python-ui-image-without-downrezing-it-with-wxpython-pil-or-other
import wx

class MyFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Resize This Window", size = wx.Size( 500,300 ))
        bSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.img1=wx.Image("Luminous Space.png", wx.BITMAP_TYPE_PNG)
        self.img2=wx.Image("fantasy-landscape.png", wx.BITMAP_TYPE_PNG)

        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(self.img1))
        self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(self.img2))

        bSizer.Add( self.m_bitmap1, 1, wx.EXPAND|wx.ALL, 0 )
        bSizer.Add( self.m_bitmap2, 1, wx.EXPAND|wx.ALL, 0 )

        self.Bind(wx.EVT_SIZE, self.onResize)

        self.SetSizer( bSizer )
        self.Layout()
        self.Centre(wx.BOTH)

    def onResize(self, event):
        frame_size = self.GetSize()

        frame_h = (frame_size[0]-10) / 2
        frame_w = (frame_size[1]-10) / 2

        img1 = self.img1.Scale(round(frame_h), round(frame_w), quality=wx.IMAGE_QUALITY_HIGH)
        img2 = self.img2.Scale(round(frame_h), round(frame_w), quality=wx.IMAGE_QUALITY_HIGH)

        self.m_bitmap1.SetBitmap(wx.Bitmap(img1))
        self.m_bitmap2.SetBitmap(wx.Bitmap(img2))

        self.Refresh()
        self.Layout()

app = wx.App()
MyFrame(None).Show()
app.MainLoop()
