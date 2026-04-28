import wx
import os

class AdvancedImagePanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        self.directory = ""
        self.imageList = []
        self.imageIndx = 0

        self.scale = 1.0
        self.rotation = 0  # graus

        self.image = None
        self.bitmap = None

        self.start_pos = None
        self.end_pos = None
        self.selecting = False

        self.on_selection = None
        self.on_image_change = None

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_zoom)

    # ===== LOAD =====
    def load_directory(self, directory):
        self.directory = directory

        self.imageList = [
            f for f in os.listdir(directory)
            if f.lower().endswith(('jpg','png','jpeg','bmp'))
        ]

        # 🔥 RESET ESTADO
        self.imageIndx = 0
        self.scale = 1.0
        self.rotation = 0

        self.load_current_image()

    def get_current_image_path(self):
        if not self.imageList:
            return None
        return os.path.join(self.directory, self.imageList[self.imageIndx])

    def load_current_image(self):
        path = self.get_current_image_path()
        if not path:
            return

        img = wx.Image(path)

        # 🔥 ROTAÇÃO
        if self.rotation != 0:
            img = img.Rotate90(clockwise=True) if self.rotation == 90 else img.Rotate90(clockwise=False)

            if self.rotation == 180:
                img = img.Rotate90()
                img = img.Rotate90()

        # 🔥 FIT automático
        panel_w, panel_h = self.GetSize()
        img_w, img_h = img.GetWidth(), img.GetHeight()

        scale_w = panel_w / img_w
        scale_h = panel_h / img_h

        self.fit_scale = min(scale_w, scale_h)

        # 🔥 escala final (fit + zoom)
        final_scale = self.fit_scale * self.scale

        new_w = int(img_w * final_scale)
        new_h = int(img_h * final_scale)

        img = img.Scale(new_w, new_h)

        self.image = img
        self.bitmap = wx.Bitmap(img)

        self.Refresh()

    # ===== NAV =====
    def next(self, evt=None):
        if not self.imageList:
            return

        self.imageIndx = (self.imageIndx + 1) % len(self.imageList)

        # 🔥 RESET
        self.scale = 1.0
        self.rotation = 0

        self.load_current_image()

        if self.on_image_change:
            self.on_image_change(self.imageIndx)

    def prev(self, evt=None):
        if not self.imageList:
            return

        self.imageIndx = (self.imageIndx - 1) % len(self.imageList)

        # 🔥 RESET
        self.scale = 1.0
        self.rotation = 0

        self.load_current_image()

        if self.on_image_change:
            self.on_image_change(self.imageIndx)

    # ===== ROTATE =====
    def rotate_right(self):
        self.rotation = (self.rotation + 90) % 360
        self.load_current_image()

    def rotate_left(self):
        self.rotation = (self.rotation - 90) % 360
        self.load_current_image()

    # ===== ZOOM =====
    def zoom_in(self):
        self.scale *= 1.25
        self.load_current_image()

    def zoom_out(self):
        self.scale *= 0.8
        self.load_current_image()

    def on_zoom(self, evt):
        if evt.GetWheelRotation() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    # ===== SELECTION =====
    def on_mouse_down(self, evt):
        self.start_pos = evt.GetPosition()
        self.selecting = True

    def on_mouse_move(self, evt):
        if self.selecting:
            self.end_pos = evt.GetPosition()
            self.Refresh()  # 🔥 ESSENCIAL

    def on_mouse_up(self, evt):
        self.selecting = False
        self.end_pos = evt.GetPosition()

        rect = self.get_rect()

        if self.on_selection and rect:
            self.on_selection(rect)

        # limpa seleção
        self.start_pos = None
        self.end_pos = None
        self.Refresh()

    def get_rect(self):
        if not self.start_pos or not self.end_pos:
            return None

        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x1 - x2)
        h = abs(y1 - y2)

        # 🔥 escala TOTAL (fit + zoom)
        total_scale = self.fit_scale * self.scale

        if total_scale != 0:
            x = int(x / total_scale)
            y = int(y / total_scale)
            w = int(w / total_scale)
            h = int(h / total_scale)

        return (x, y, w, h)
    
    def get_rect_screen(self):
        if not self.start_pos or not self.end_pos:
            return None

        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        return (
            min(x1, x2),
            min(y1, y2),
            abs(x1 - x2),
            abs(y1 - y2)
        )

    # ===== DRAW =====
    def on_paint(self, evt):
        dc = wx.PaintDC(self)

        if self.bitmap:
            dc.DrawBitmap(self.bitmap, 0, 0)

        if self.selecting and self.start_pos and self.end_pos:
            dc.SetPen(wx.Pen(wx.RED, 2))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)

            rect = self.get_rect_screen()
            if rect:
                dc.DrawRectangle(*rect)


class ThumbnailPanel(wx.ScrolledWindow):

    def __init__(self, parent, callback):
        super().__init__(parent, size=(200, -1))

        self.callback = callback
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.thumbs = []
        self.selected = None

        self.SetSizer(self.sizer)
        self.SetScrollRate(5,5)

    def load_images(self, directory, images):
        self.sizer.Clear(True)
        self.thumbs.clear()

        # 🔥 RESET ESSENCIAL
        self.selected = None

        for i, img_name in enumerate(images):
            path = os.path.join(directory, img_name)

            img = wx.Image(path).Scale(120,90)
            bmp = wx.Bitmap(img)

            panel = wx.Panel(self)
            box = wx.BoxSizer(wx.VERTICAL)

            thumb = wx.StaticBitmap(panel, bitmap=bmp)
            thumb.Bind(wx.EVT_LEFT_DOWN, lambda e, idx=i: self.on_click(idx))

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
        # 🔥 valida índice antigo
        if self.selected is not None and self.selected < len(self.thumbs):
            self.thumbs[self.selected].SetBackgroundColour(wx.NullColour)

        # 🔥 valida novo índice
        if index < len(self.thumbs):
            self.thumbs[index].SetBackgroundColour(wx.Colour(0,120,215))
            self.selected = index

        self.Refresh()