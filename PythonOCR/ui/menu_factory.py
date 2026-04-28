import wx, os

class MenuFactory:
    def __init__(self, frame):
        self.frame = frame
        self.map = {}

    def create(self):
        bar = wx.MenuBar()

        """Make a file menu with Open and Exit items"""
        fileMenu = wx.Menu()

        self.add(fileMenu, "open", wx.ID_OPEN, "Abrir", "gtk-open.png")
        self.add(fileMenu, "save", wx.ID_SAVE, "Salvar", "gtk-save.png")
        fileMenu.AppendSeparator()
        self.add(fileMenu, "exit", wx.ID_EXIT, "Sair", "gtk-quit.png")

        bar.Append(fileMenu, "Arquivo")

        # Make a edit menu with GetText and CleanText items
        editMenu = wx.Menu()

        self.add(editMenu, "ocr", wx.ID_ANY, "OCR", "gtk-bold.png")
        self.add(editMenu, "clear", wx.ID_CLEAR, "Limpar", "gtk-clear.png")

        bar.Append(editMenu, "Editar")

        # Make a view menu with ZoonIn, ZoonOut
        viewMenu = wx.Menu()

        self.add(viewMenu, "rotate_left", wx.ID_ANY, "Girar ←", "gtk-rotate-left.png")
        self.add(viewMenu, "rotate_right", wx.ID_ANY, "Girar →", "gtk-rotate-right.png")
        self.add(viewMenu, "zoom_in", wx.ID_ZOOM_IN, "Zoom In", "gtk-zoom-in.png")
        self.add(viewMenu, "zoom_out", wx.ID_ZOOM_OUT, "Zoom Out", "gtk-zoom-out.png")

        bar.Append(viewMenu, "Exibir")

        # Now a help menu for the about item
        helpMenu = wx.Menu()

        self.add(helpMenu, "about", wx.ID_ABOUT, "Sobre", "gtk-about.png")

        bar.Append(helpMenu, "Ajuda")

        self.frame.SetMenuBar(bar)

    def add(self, menu, key, id, label, icon):
        """Obtêm o caminho das imagens"""
        images_path = os.path.abspath(r'.\icones')

        item = menu.Append(id, label)

        if os.path.exists(os.path.join(images_path, icon)):
            item.SetBitmap(wx.Bitmap(os.path.join(images_path, icon)))

        self.map[item.GetId()] = key

    def bind(self, commands):
        for id, key in self.map.items():
            cmd = commands.get(key)
            if cmd:
                self.frame.Bind(wx.EVT_MENU, lambda evt, c=cmd: c.execute(), id=id)