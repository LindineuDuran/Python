import wx, os
import wx.lib.scrolledpanel
########################################################################
class MyPanel(wx.lib.scrolledpanel.ScrolledPanel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent, sizePanel, posPanel, text_list = list()):
        """Constructor"""
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, size=sizePanel, pos=posPanel, style=wx.SIMPLE_BORDER)
        self.number_of_buttons = 0
        self.process_list = list()
        self.frame = parent

        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.widgetSizer)

    #----------------------------------------------------------------------
    def setTextList(self, text_list):
        self.text_list = text_list

    #----------------------------------------------------------------------
    def getTextList(self):
        return self.text_list

    #----------------------------------------------------------------------
    def setProcessList(self, process_list):
        self.process_list = process_list

    #----------------------------------------------------------------------
    def getProcessList(self):
        return self.process_list

    #----------------------------------------------------------------------
    def createCheckBoxesList(self):
        """"""
        if self.number_of_buttons > 0: self.destroyCheckBoxesList()

        pos_y = 10
        self.bSizer = wx.BoxSizer( wx.VERTICAL )
        for item in self.text_list:
          self.addWidget(item, pos_y)
          pos_y += 20

    #----------------------------------------------------------------------
    def addWidget(self, texto, pos_y):
        """"""
        self.number_of_buttons += 1
        name = "chk%s" % self.number_of_buttons
        cb = wx.CheckBox(self, label=texto, name=name, pos=(10, pos_y))
        cb.Bind(wx.EVT_CHECKBOX, self.update)
        self.widgetSizer.Add(cb, 0, wx.ALL, 5)

    #----------------------------------------------------------------------
    def update(self, e):
        """"""
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        nome = sender.GetLabel()

        if isChecked:
            print('Insere item: ', nome)
            self.process_list.append(nome)
        else:
            print('Remolve item: ', nome)
            if nome in self.process_list: self.process_list.remove(nome)

    #----------------------------------------------------------------------
    def destroyCheckBoxesList(self):
        """"""
        while(self.number_of_buttons > 0):
            self.removeWidget()

    #----------------------------------------------------------------------
    def removeWidget(self):
        """"""
        if self.widgetSizer.GetChildren():
            self.widgetSizer.Hide(self.number_of_buttons-1)
            self.widgetSizer.Remove(self.number_of_buttons-1)
            self.number_of_buttons -= 1

########################################################################
class GUI(wx.Frame):
    directory = ''
    process_list = list()

    def __init__(self,parent,id,title):
        """First retrieve the screen size of the device"""
        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        """contador de widgets"""
        self.number_of_widgets = 0

        """Create a frame"""
        # wx.Frame.__init__(self,parent,id,title,size=screenSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        wx.Frame.__init__(self,parent,id,title,size=(800,400), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        """Create a panel for text"""
        self.panel1 = wx.Panel(self,-1,size=(500,400), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.panel1.SetBackgroundColour('#FFFFFF')

        """Create a customized panel of checkboxes"""
        self.panel2 = MyPanel(self, sizePanel=(283,340), posPanel=(500,0))
        self.panel2.SetBackgroundColour('#A0A0A0')

        """create a menu bar"""
        self.makeMenuBar()

        """create a text box"""
        self.tc = wx.TextCtrl(self.panel1, -1, size=(500,400), style=wx.TE_MULTILINE)

        self.textbox = wx.BoxSizer(wx.VERTICAL)
        self.textbox.Add(self.tc,proportion=1,flag = wx.EXPAND)

        self.panel1.SetSizer(self.textbox)

    def makeMenuBar(self):
        """Obtêm o caminho das imagens"""
        images_path = os.path.abspath(r'.\images')

        """Make a file menu with Open and Exit items"""
        fileMenu = wx.Menu()

        openItem = fileMenu.Append(wx.ID_OPEN, 'Abrir\tCtrl+O', 'Selecionar pasta de imagens')
        if os.path.exists(os.path.join(images_path, 'gtk-open.png')):
            openItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-open.png')))

        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT, 'Sair\tCtrl+Q', 'Encerrar o aplicativo')
        if os.path.exists(os.path.join(images_path, 'gtk-quit.png')):
            exitItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-quit.png')))

        """Make the menu bar and add the menus to it."""
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "Arquivo")

        """Give the menu bar to the frame"""
        self.SetMenuBar(menuBar)

        """Finally, associate a handler function with the EVT_MENU event for each of the menu items."""
        self.Bind(wx.EVT_MENU, self.onOpen, openItem)
        self.Bind(wx.EVT_MENU, self.onExit, exitItem)

    def onOpen(self, event):
        """Browse for directory"""
        dialog = wx.DirDialog (None, "Escolha a pasta com as imagens", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            self.directory = dialog.GetPath()

            self.onView()

    def onView(self):
        """Retorna uma lista de strings com
           nomes de arquivo do diretório atual"""
        fileList = os.listdir(self.directory)

        """Cria CheckBoxs com nomes doa arquivos"""
        self.panel2.setTextList(fileList)
        if self.panel2.getTextList() is not None: self.panel2.createCheckBoxesList()
        self.panel2.SetupScrolling()
        self.panel2.Refresh()

    """Atualiza lista de checkboxes"""
    def update(self, e):
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        nome = sender.GetLabel()

        if isChecked:
            print('Insere item: ', nome)
            self.process_list.append(nome)
        else:
            print('Remolve item: ', nome)
            if nome in self.process_list: self.process_list.remove(nome)

    def onExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

if __name__=='__main__':
    app = wx.App()
    frame = GUI(parent=None, id=-1, title="Test")
    frame.Show()
    app.MainLoop()
