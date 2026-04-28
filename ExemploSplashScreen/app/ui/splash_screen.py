import os
import wx


class SplashScreen(wx.Frame):

    def __init__(self):
        super().__init__(None, style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        self.SetSize((420, 280))
        self.Center()
        self.SetBackgroundColour("#1e1e1e")  # tema escuro

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#1e1e1e")

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 📁 Caminho robusto (independente de onde executa)
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.abspath(os.path.join(base_path, "..", "icones", "visionparse_ocr.png"))
        logo = None

        # 🖼️ Logo (com tratamento)
        if os.path.exists(image_path):
            try:
                image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)

                if not image.IsOk():
                    print("Imagem inválida!")
                else:
                    # 🔧 Mantém proporção corretamente
                    max_size = 300
                    w, h = image.GetWidth(), image.GetHeight()

                    if w > h:
                        new_w = max_size
                        new_h = int(h * (max_size / w))
                    else:
                        new_h = max_size
                        new_w = int(w * (max_size / h))

                    image = image.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

                    logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap(image))

            except Exception as e:
                print(f"Erro ao carregar logo: {e}")

        # # 🧠 Título
        # title = wx.StaticText(panel, label="VisionParse OCR")
        # title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        # title.SetForegroundColour("white")

        # 📄 Subtítulo
        self.subtitle = wx.StaticText(panel, label="Inicializando aplicação...")
        self.subtitle.SetForegroundColour("#cccccc")

        # 📊 Barra de progresso
        self.progress = wx.Gauge(panel, range=100, size=(300, 20))

        # 📐 Layout
        vbox.AddStretchSpacer()

        if logo:  # 🔴 só adiciona se existir
            vbox.Add(logo, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        #vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        vbox.Add(self.subtitle, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        vbox.Add(self.progress, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.AddStretchSpacer()

        panel.SetSizer(vbox)
        panel.Layout()
        self.Layout()
        self.Fit()

    # 🔄 Atualiza progresso
    def update_progress(self, value, message=None):
        wx.CallAfter(self.progress.SetValue, value)

        if message:
            wx.CallAfter(self.subtitle.SetLabel, message)