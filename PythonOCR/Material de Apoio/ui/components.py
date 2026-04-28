import wx
import os

class AdvancedImagePanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        self.image = None
        self.bitmap = None
        self.scale = 1.0

        self.imageList = []
        self.imageIndx = 0
        self.directory = ""

        self.start_pos = None
        self.end_pos = None
        self.selecting = False

        self.on_image_change = None
        self.on_selection = None  # callback OCR

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)

    # =========================
    # LOAD IMAGENS
    # =========================
    def load_directory(self, directory):
        self.directory = directory

        self.imageList = [
            f for f in os.listdir(directory)
            if f.lower().endswith(('jpg','png','jpeg','bmp'))
        ]

        self.imageIndx = 0
        self.load_current_image()

    def load_current_image(self):
        path = self.get_current_image_path()
        if not path:
            return

        img = wx.Image(path)

        # aplica zoom
        w = int(img.GetWidth() * self.scale)
        h = int(img.GetHeight() * self.scale)

        img = img.Scale(w, h)

        self.image = img
        self.bitmap = wx.Bitmap(img)

        self.Refresh()

    def get_current_image_path(self):
        if not self.imageList:
            return None
        return os.path.join(self.directory, self.imageList[self.imageIndx])

    # =========================
    # NAV
    # =========================
    def next(self, evt=None):
        if not self.imageList:
            return

        self.imageIndx = (self.imageIndx + 1) % len(self.imageList)
        self.load_current_image()

        if self.on_image_change:
            self.on_image_change(self.imageIndx)

    def prev(self, evt=None):
        if not self.imageList:
            return

        self.imageIndx = (self.imageIndx - 1) % len(self.imageList)
        self.load_current_image()

        if self.on_image_change:
            self.on_image_change(self.imageIndx)

    # =========================
    # SELEÇÃO DE ÁREA
    # =========================
    def on_mouse_down(self, event):
        self.start_pos = event.GetPosition()
        self.selecting = True

    def on_mouse_move(self, event):
        if self.selecting:
            self.end_pos = event.GetPosition()
            self.Refresh()

    def on_mouse_up(self, event):
        self.selecting = False
        self.end_pos = event.GetPosition()

        rect = self.get_selection_rect()

        if self.on_selection and rect:
            self.on_selection(rect)

    def get_selection_rect(self):
        if not self.start_pos or not self.end_pos:
            return None

        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x1 - x2)
        h = abs(y1 - y2)

        return (x, y, w, h)

    # =========================
    # RENDER
    # =========================
    def on_paint(self, event):
        dc = wx.PaintDC(self)

        if self.bitmap:
            dc.DrawBitmap(self.bitmap, 0, 0)

        # desenha seleção
        if self.selecting and self.start_pos and self.end_pos:
            dc.SetPen(wx.Pen(wx.RED, 2))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)

            rect = self.get_selection_rect()
            if rect:
                dc.DrawRectangle(*rect)

    def zoom_in(self):
        self.scale *= 1.25
        self.load_current_image()

    def zoom_out(self):
        self.scale *= 0.8
        self.load_current_image()


class ThumbnailPanel(wx.ScrolledWindow):

    def __init__(self, parent, callback):
        super().__init__(parent, size=(200, -1), style=wx.VSCROLL)

        self.callback = callback
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.thumbs = []
        self.selected = None

        self.SetSizer(self.sizer)
        self.SetScrollRate(5, 5)

    def load_images(self, directory, images):
        import os

        self.sizer.Clear(True)
        self.thumbs.clear()

        for i, img_name in enumerate(images):
            path = os.path.join(directory, img_name)

            img = wx.Image(path).Scale(120, 90)
            bmp = wx.Bitmap(img)

            panel = wx.Panel(self)
            box = wx.BoxSizer(wx.VERTICAL)

            thumb = wx.StaticBitmap(panel, bitmap=bmp)

            thumb.Bind(wx.EVT_LEFT_DOWN, lambda evt, idx=i: self.on_click(idx))

            box.Add(thumb, 0, wx.ALL, 2)
            panel.SetSizer(box)

            self.sizer.Add(panel, 0, wx.ALL, 5)

            self.thumbs.append(panel)

        self.Layout()
        self.FitInside()

    def on_click(self, index):
        self.select(index)
        self.callback(index)

    def select(self, index):
        # remove seleção anterior
        if self.selected is not None:
            self.thumbs[self.selected].SetBackgroundColour(wx.NullColour)

        # aplica seleção
        self.thumbs[index].SetBackgroundColour(wx.Colour(0, 120, 215))

        self.selected = index
        self.Refresh()