from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
import wx, os

from app.utils.path_manager import PathManager

class MenuFactory:
    def __init__(self, frame):
        self.frame = frame
        self.map = {}

    def create(self):
        # Menu Bar
        bar = wx.MenuBar()

        # Make a file menu with Open and Exit items
        fileMenu = wx.Menu()

        self.add(fileMenu, "open", wx.ID_OPEN, "Abrir PDF\tCtrl+O", "gtk-pdf.png", "Abrir um arquivo PDF")
        self.add(fileMenu, "folder", wx.ID_FILE, "Abrir Pasta de Imagens\tCtrl+F", "gtk-open.png", "Abrir pasta de imagens")
        self.add(fileMenu, "save", wx.ID_SAVE, "Salvar Texto Extraído\tCtrl+S", "gtk-save.png", "Salvar Texto Extraído pelo OCR")
        self.add(fileMenu, "export", wx.ID_SAVEAS, "Salvar Imagens\tCtrl+I", "gtk-bitmap.png", "Salvar Imagens Obtidas do PDF")
        fileMenu.AppendSeparator()
        self.add(fileMenu, "exit", wx.ID_EXIT, "Sair\tCtrl+Q", "gtk-quit.png", "Encerrar o aplicativo")

        bar.Append(fileMenu, "Arquivo")

        # Make a edit menu with GetText and CleanText items
        editMenu = wx.Menu()

        self.add(editMenu, "ocr", wx.Window.NewControlId(), "Obtêm Texto\tCtrl+G", "gtk-bold.png", "Reconhece o texto da imagem")
        self.add(editMenu, "clear", wx.ID_CLEAR, "Limpa Texto\tCtrl+L", "gtk-clear.png", "Limpa o texto obtido")

        bar.Append(editMenu, "Editar")

        # Make a view menu with ZoonIn, ZoonOut
        viewMenu = wx.Menu()

        self.add(viewMenu, "rotate_left", wx.Window.NewControlId(), "Girar ←\tCtrl+E", "gtk-rotate-left.png", "Girar imagem p/ esquerda")
        self.add(viewMenu, "rotate_right", wx.Window.NewControlId(), "Girar →\tCtrl+D", "gtk-rotate-right.png", "Girar imagem p/ direita")
        self.add(viewMenu, "zoom_in", wx.ID_ZOOM_IN, "Ampliar\tCtrl++", "gtk-zoom-in.png", "Amplia a imagem")
        self.add(viewMenu, "zoom_out", wx.ID_ZOOM_OUT, "Reduzir\tCtrl+-", "gtk-zoom-out.png", "Reduz a imagem")

        bar.Append(viewMenu, "Exibir")

        # Now a help menu for the about item
        helpMenu = wx.Menu()

        self.add(helpMenu, "about", wx.ID_ABOUT, 'Sobre\tCtrl+A', "gtk-about.png", "Informações sobre o aplicativo e o desenvolvedor")
        self.add(helpMenu, "commands", wx.ID_HELP_COMMANDS, 'Comandos do Aplicativo\tCtrl+K', "gtk-execute.png", "Descreve as funcionalidades do aplicativo")

        bar.Append(helpMenu, "Ajuda")

        self.frame.SetMenuBar(bar)

    def add(self, menu, key, id, label, icon, help=""):
        item = menu.Append(id, label, help)

        icon_path = PathManager.icon(icon)

        logger.debug("Icon Path: %s", icon_path)

        if os.path.exists(icon_path):
            item.SetBitmap(wx.Bitmap(icon_path))

        self.map[item.GetId()] = key

    def handler(self, cmd):
        def _handler(event):
            logger.debug(f"Executando: {cmd.__class__.__name__}")
            cmd.execute()
        return _handler

    def bind(self, commands):
        for id, key in self.map.items():
            cmd = commands.get(key)
            if cmd:
                self.frame.Bind(wx.EVT_MENU, self.handler(cmd), id=id)