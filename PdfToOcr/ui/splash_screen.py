import os, wx

class SplashScreen(wx.Frame):

    def __init__(self):
        super().__init__(None, style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        self.SetSize((400, 250))
        self.Center()

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        images_path = os.path.abspath(r'.\icones')
        icon = "VisionParse OCR.png"

        # 📁 Caminho robusto (independente de onde executa)
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "..", "icones", "VisionParse OCR.png")

        image_path = os.path.abspath(image_path)

        print("Image path:", image_path)
        print("Existe?", os.path.exists(image_path))

        # # 🖼️ Logo (com tratamento)
        # if os.path.exists(image_path):
        #     try:
        #         image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)

        #         # 🔧 Redimensiona mantendo proporção
        #         image = image.Scale(120, 120, wx.IMAGE_QUALITY_HIGH)

        #         logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap(image))
        #         vbox.Add(logo, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        #     except Exception as e:
        #         print(f"Erro ao carregar logo: {e}")

        # 🧠 Título
        title = wx.StaticText(panel, label="PDF OCR PRO")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        subtitle = wx.StaticText(panel, label="Inicializando aplicação...")
        self.progress = wx.Gauge(panel, range=100, size=(300, 20))

        vbox.AddStretchSpacer()

        # 🖼️ Logo (com tratamento)
        if os.path.exists(image_path):
            try:
                image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)

                # 🔧 Redimensiona mantendo proporção
                image = image.Scale(120, 120, wx.IMAGE_QUALITY_HIGH)

                logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap(image))
                vbox.Add(logo, 0, wx.ALIGN_CENTER | wx.TOP, 20)

            except Exception as e:
                print(f"Erro ao carregar logo: {e}")
                
        vbox.Add(title, 0, wx.CENTER | wx.ALL, 10)
        vbox.Add(subtitle, 0, wx.CENTER | wx.ALL, 5)
        vbox.Add(self.progress, 0, wx.CENTER | wx.ALL, 15)
        vbox.AddStretchSpacer()

        panel.SetSizer(vbox)

    def update_progress(self, value):
        wx.CallAfter(self.progress.SetValue, value)