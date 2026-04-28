from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
import wx
import os, io
from app.core.entities.image_entity import ImageEntity

class AdvancedImagePanel(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_SIMPLE | wx.VSCROLL | wx.HSCROLL)

        self.SetScrollRate(10, 10)  # velocidade do scroll
        self.SetBackgroundColour(wx.Colour(30, 30, 30))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)

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
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)

    def reset_state(self):
        self.imageList = []
        self.imageIndx = 0
        self.scale = 1.0
        self.rotation = 0

        self.original_image = None
        self.bitmap = None

        self.start_pos = None
        self.end_pos = None
        self.selecting = False

        self.SetVirtualSize((0, 0))
        self.Refresh()

    # ===== LOAD =====
    def load_directory(self, directory):
        self.reset_state()  # 🔥 ESSENCIAL

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

    def load_current_image(self, image=None):
        # 🔥 Caso PDF (ImageEntity)
        if self.imageList and isinstance(self.imageList[0], ImageEntity):
            entity = self.imageList[self.imageIndx]

            if not entity.bytes:
                return

            stream = io.BytesIO(entity.bytes)
            self.original_image = wx.Image(stream)

        # 🔥 Caso diretório
        elif self.imageList:
            path = self.get_current_image_path()
            if not path:
                return

            self.original_image = wx.Image(path)

        else:
            return

        if not hasattr(self, "original_image") or self.original_image is None:
            return

        img = self.original_image.Copy()

        # ===== ROTAÇÃO =====
        if self.rotation == 90:
            img = img.Rotate90(clockwise=True)
        elif self.rotation == 270:
            img = img.Rotate90(clockwise=False)
        elif self.rotation == 180:
            img = img.Rotate90().Rotate90()

        # ===== FIT =====
        panel_w, panel_h = self.GetSize()
        img_w, img_h = img.GetWidth(), img.GetHeight()

        scale_w = panel_w / img_w
        scale_h = panel_h / img_h

        self.fit_scale = min(scale_w, scale_h)
        final_scale = self.fit_scale * self.scale

        new_w = int(img_w * final_scale)
        new_h = int(img_h * final_scale)

        img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

        self.bitmap = wx.Bitmap(img)
        self.SetVirtualSize((new_w, new_h))

        self.Refresh()

    def load_pdf_images(self, image_entities):
        self.reset_state()  # 🔥 AQUI resolve seu bug

        self.imageList = image_entities
        self.imageIndx = 0

        if self.imageList:
            self.load_current_image()

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
        self.start_pos = self.CalcUnscrolledPosition(evt.GetPosition())
        self.selecting = True

    def on_mouse_move(self, evt):
        if self.selecting:
            self.end_pos = self.CalcUnscrolledPosition(evt.GetPosition())
            self.Refresh()

    def on_mouse_up(self, evt):
        self.selecting = False
        self.end_pos = self.CalcUnscrolledPosition(evt.GetPosition())

        rect = self.get_rect()

        if self.on_selection and rect:
            self.on_selection(rect)

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

        # 🔥 compensar CENTRALIZAÇÃO
        panel_w, panel_h = self.GetClientSize()
        bmp_w, bmp_h = self.bitmap.GetSize()

        offset_x = max(0, (panel_w - bmp_w) // 2)
        offset_y = max(0, (panel_h - bmp_h) // 2)

        x -= offset_x
        y -= offset_y

        # 🔥 converter para coordenada ORIGINAL
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
        dc = wx.AutoBufferedPaintDC(self)
        self.PrepareDC(dc)

        panel_w, panel_h = self.GetClientSize()

        # 🔥 FUNDO QUADRICULADO
        self.draw_checkerboard(dc, panel_w, panel_h)

        if self.bitmap:
            bmp_w, bmp_h = self.bitmap.GetSize()

            x = max(0, (panel_w - bmp_w) // 2)
            y = max(0, (panel_h - bmp_h) // 2)

            # 🔥 SOMBRA
            self.draw_shadow(dc, x, y, bmp_w, bmp_h)

            # 🔥 IMAGEM
            dc.DrawBitmap(self.bitmap, x, y)

            # 🔥 BORDA
            self.draw_border(dc, x, y, bmp_w, bmp_h)

        # 🔥 SELEÇÃO
        if self.selecting and self.start_pos and self.end_pos:
            dc.SetPen(wx.Pen(wx.RED, 2))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)

            rect = self.get_rect_screen()
            if rect:
                dc.DrawRectangle(*rect)

    def draw_checkerboard(self, dc, width, height, size=12):
        color1 = wx.Colour(60, 60, 60)
        color2 = wx.Colour(40, 40, 40)

        for y in range(0, height, size):
            for x in range(0, width, size):
                if (x // size + y // size) % 2 == 0:
                    dc.SetBrush(wx.Brush(color1))
                else:
                    dc.SetBrush(wx.Brush(color2))

                dc.SetPen(wx.TRANSPARENT_PEN)
                dc.DrawRectangle(x, y, size, size)

    def draw_shadow(self, dc, x, y, w, h):
        shadow_color = wx.Colour(0, 0, 0, 80)  # semi-transparente

        dc.SetBrush(wx.Brush(shadow_color))
        dc.SetPen(wx.TRANSPARENT_PEN)

        # leve deslocamento (efeito sombra)
        dc.DrawRectangle(x + 5, y + 5, w, h)

    def draw_border(self, dc, x, y, w, h):
        dc.SetPen(wx.Pen(wx.Colour(200, 200, 200), 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(x, y, w, h)

class ThumbnailPanel(wx.ScrolledWindow):
    def __init__(self, parent, callback):
        super().__init__(parent, size=(200, -1), style=wx.BORDER_SIMPLE | wx.VSCROLL)
        
        self.callback = callback
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetMinSize((200, -1))
        self.SetMaxSize((300, -1))
        self.SetScrollRate(5, 5)
        self.SetSizer(self.sizer)
        self.cache = {}  # 🔥 cache de thumbnails

        self.thumbs = []
        self.selected = None

    # ==========================================
    # 🔥 CORREÇÃO PRINCIPAL
    # ==========================================
    def get_image_source(self, directory, item, is_entity_list):
        if is_entity_list:
            return item.bytes  # bytes (PDF)
        else:
            return os.path.join(directory, item)  # path (diretório)

    # ==========================================
    # 🔥 CORREÇÃO wx.Image
    # ==========================================
    def create_thumbnail(self, img_source, max_w=120, max_h=90):
        # 🔥 GERA A CHAVE PRIMEIRO
        key = self._get_cache_key(img_source)

        # 🔥 CACHE HIT
        if key in self.cache:
            return self.cache[key]

        # 🔥 Detecta tipo automaticamente
        if isinstance(img_source, str):
            img = wx.Image(img_source)
        else:
            stream = io.BytesIO(img_source)
            img = wx.Image(stream, wx.BITMAP_TYPE_ANY)

        if not img.IsOk():
            logger.error("[ERRO] Falha ao carregar imagem")
            return None

        w, h = img.GetWidth(), img.GetHeight()

        # 🔥 mantém proporção
        ratio = min(max_w / w, max_h / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)

        img_resized = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

        # 🔥 canvas fixo
        canvas = wx.Bitmap(max_w, max_h)
        dc = wx.MemoryDC(canvas)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255)))
        dc.Clear()

        x = (max_w - new_w) // 2
        y = (max_h - new_h) // 2

        dc.DrawBitmap(wx.Bitmap(img_resized), x, y)
        dc.SelectObject(wx.NullBitmap)

        # 🔥 SALVA NO CACHE
        self.cache[key] = canvas

        return canvas

    # ==========================================
    # 🔥 LOAD
    # ==========================================
    def load_images(self, directory, image_list):
        self.sizer.Clear(True)
        self.thumbs.clear()
        self.selected = None
        self.cache.clear()  # 🔥 MUITO IMPORTANTE

        is_entity_list = (
            isinstance(image_list, list)
            and len(image_list) > 0
            and hasattr(image_list[0], "bytes")
        )

        for i, item in enumerate(image_list):
            img_source = self.get_image_source(directory, item, is_entity_list)

            if not img_source:
                continue

            bmp = self.create_thumbnail(img_source, 120, 90)

            if bmp is None:
                continue

            panel = wx.Panel(self)
            box = wx.BoxSizer(wx.VERTICAL)

            thumb = wx.StaticBitmap(panel, bitmap=bmp)
            thumb.Bind(wx.EVT_LEFT_DOWN, lambda e, idx=i: self.on_click(idx))

            box.Add(thumb, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            label = wx.StaticText(panel, label=f"Página {i+1}")
            box.Add(label, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)

            panel.SetSizer(box)

            self.sizer.Add(panel, 0, wx.EXPAND | wx.ALL, 5)
            self.thumbs.append(panel)

        self.Layout()
        self.FitInside()

    def _get_cache_key(self, img_source):
        if isinstance(img_source, str):
            return img_source  # path
        else:
            return hash(img_source[:100])  # evita custo alto

    # ==========================================
    # 🔥 EVENTOS
    # ==========================================
    def on_click(self, index):
        self.select(index)
        self.callback(index)

    def select(self, index):
        if self.selected is not None and self.selected < len(self.thumbs):
            self.thumbs[self.selected].SetBackgroundColour(wx.NullColour)

        if index < len(self.thumbs):
            self.thumbs[index].SetBackgroundColour(wx.Colour(0, 120, 215))
            self.selected = index

        self.Refresh()