import os, wx

class ImageViewerDrawRetangle(wx.Frame):
    images_path = os.path.abspath(r'.')

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(ImageViewerDrawRetangle, self).__init__(*args, **kw)

        self.imageBox = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.img = wx.Image(240,240)

        self.imageBox.SetSizer(self.vbox)
        self.Show()

        self.createWidgets()
        # self.drawRec(None)

    def createWidgets(self):
        self.img = wx.Image(os.path.join(self.images_path, 'Luminous Space.png'), wx.BITMAP_TYPE_ANY)

        width = self.img.GetWidth()
        height = self.img.GetHeight()

        imgRatio    = 1.0*width/height
        xWin        = self.imageBox.Size[0]
        yWin        = self.imageBox.Size[1]

        factor = 1
        width  = factor*xWin
        height = factor*xWin/imgRatio

        self.img = self.img.Scale(round(width),round(height))

        self.imageCtrl = wx.StaticBitmap(self.imageBox, wx.ID_ANY, wx.Bitmap(self.img))
        self.vbox.Add(self.imageCtrl, 0, wx.ALL, 5)

        # self.imageCtrl.Bind(wx.EVT_PAINT, self.OnPaint)
        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.imageCtrl.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.imageCtrl.Bind(wx.EVT_MOTION, self.OnMouseMove)

        self.startPos = None
        self.overlay = wx.Overlay()

    def drawRec(self, event):
        bmp = wx.Bitmap(self.img)
        dc = wx.MemoryDC(bmp)
        dc.SetPen(wx.Pen('green', 5, wx.SOLID))
        dc.SetBrush(wx.Brush('green', wx.TRANSPARENT))
        dc.DrawRectangle(20, 20, 60, 60)
        del dc
        self.imageCtrl.SetBitmap(bmp)

    # def OnPaint(self, evt):
    #     # Just some simple stuff to paint in the window for an example
    #     dc = wx.PaintDC(self.imageCtrl)
    #     coords = ((40,40),(200,220),(210,120),(120,300))
    #     dc.SetBackground(wx.Brush("sky blue"))
    #     dc.Clear()
    #
    #     dc.SetPen(wx.Pen("red", 2))
    #     dc.SetBrush(wx.CYAN_BRUSH)
    #     dc.DrawPolygon(coords)
    #     dc.DrawLabel("Draw the mouse across this window to see \n"
    #                 "a rubber-band effect using wx.Overlay",
    #                 (140, 50, -1, -1))


    def OnLeftDown(self, evt):
        # Capture the mouse and save the starting posiiton for the
        # rubber-band
        self.CaptureMouse()
        self.startPos = evt.GetPosition()
        print(self.startPos)

    def OnMouseMove(self, evt):
        print(evt.GetPosition())

        if not self.HasCapture():
            return

        print("Testa Desenho")

        rect = wx.Rect(self.startPos, evt.GetPosition())
        # Draw the rubber-band rectangle using an overlay so it
        # will manage keeping the rectangle and the former window
        # contents separate.
        dc = wx.ClientDC(self.imageCtrl)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()

        pen = wx.Pen("black", 2)
        brush = wx.Brush(wx.Colour(192,192,192,128))
        if "wxMac" in wx.PlatformInfo:
            dc.SetPen(pen)
            dc.SetBrush(brush)
            dc.DrawRectangleRect(rect)
        else:
            # use a GC on Windows (and GTK?)
            # this crashed on the Mac
            ctx = wx.GraphicsContext.Create(dc)
            ctx.SetPen(pen)
            ctx.SetBrush(brush)
            ctx.DrawRectangle(*rect)

        del odc # work around a bug in the Python wrappers to make
                # sure the odc is destroyed before the dc is.


    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        self.startPos = None

        # When the mouse is released we reset the overlay and it
        # restores the former content to the window.
        #dc = wx.ClientDC(self)
        #odc = wx.DCOverlay(self.overlay, dc)
        #odc.Clear()
        #del odc
        self.overlay.Reset()

if __name__ == '__main__':
    app = wx.App()
    frm = ImageViewerDrawRetangle(None, title='Image Viewer',size=(800,441), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

    if "wxMSW" in wx.PlatformInfo:
        frm.SetTransparent(254)

    frm.Show()
    app.MainLoop()
