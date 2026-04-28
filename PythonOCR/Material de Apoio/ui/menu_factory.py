import wx

class MenuFactory:

    def __init__(self, frame):
        self.frame = frame
        self.map = {}

    def create(self):
        bar = wx.MenuBar()

        fileMenu = wx.Menu()
        self.add(fileMenu, "open", wx.ID_OPEN, "Abrir")
        bar.Append(fileMenu, "Arquivo")

        actionMenu = wx.Menu()
        self.add(actionMenu, "ocr", wx.ID_ANY, "OCR")
        self.add(actionMenu, "clear", wx.ID_CLEAR, "Limpar")
        bar.Append(actionMenu, "Ações")

        viewMenu = wx.Menu()
        self.add(viewMenu, "zoom_in", wx.ID_ZOOM_IN, "Zoom In")
        self.add(viewMenu, "zoom_out", wx.ID_ZOOM_OUT, "Zoom Out")
        bar.Append(viewMenu, "Exibir")

        helpMenu = wx.Menu()
        self.add(helpMenu, "about", wx.ID_ABOUT, "Sobre")
        bar.Append(helpMenu, "Ajuda")

        self.frame.SetMenuBar(bar)

    def add(self, menu, key, id, label):
        item = menu.Append(id, label)
        self.map[item.GetId()] = key

    def bind(self, commands):
        for id, key in self.map.items():
            cmd = commands.get(key)
            if cmd:
                self.frame.Bind(wx.EVT_MENU, lambda evt, c=cmd: c.execute(), id=id)