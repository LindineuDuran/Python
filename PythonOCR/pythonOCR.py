import wx, os, string
from PIL import Image  # Importando o módulo Pillow para abrir a imagem no script
import pytesseract  # Módulo para a utilização da tecnologia OCR

app_path = os.path.dirname(os.path.abspath(__file__))
tesseract_path = os.path.join(app_path, 'Tesseract-OCR', 'tesseract.exe')
tessdata = os.path.join(app_path, 'Tesseract-OCR', 'tessdata')

if os.path.exists(tesseract_path):
    #pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    #tessdata_dir_config = r'--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
    tessdata_dir_config = '--tessdata-dir ' + tessdata

# The following are the character codes for a Swedish keyboard
M_KEY     = 77
R_KEY     = 82
PLUS_KEY  = 43
MINUS_KEY = 45

class PythonOCR(wx.Frame):
    directory = ''

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(PythonOCR, self).__init__(*args, **kw)

        self.panel1 = wx.Panel(self, size=(785,300), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.panel1.SetBackgroundColour('#A0A0A0')

        self.panel2 = wx.Panel(self,-1,size=(785,220), pos=(0,300), style=wx.SIMPLE_BORDER)
        self.panel2.SetBackgroundColour('#FDDF99')

        self.imgbox = wx.BoxSizer(wx.VERTICAL)

        self.tc = wx.TextCtrl(self.panel2, -1, size=(785,220), style=wx.TE_MULTILINE)

        self.textbox = wx.BoxSizer(wx.VERTICAL)
        self.textbox.Add(self.tc,proportion=1,flag = wx.EXPAND)

        # create a menu bar
        self.makeMenuBar()

        self.CreateStatusBar(5)
        self.SetStatusWidths([-1, 70, 50, 50, 30])

        self.cursor     = wx.Cursor( wx.CURSOR_ARROW)  # single arrow pointer
        self.moveCursor = wx.Cursor(wx.CURSOR_SIZING)  # N,E,S,W arrows (when panning)

        self.panel1.SetSizer(self.imgbox)
        self.panel2.SetSizer(self.textbox)
        self.Show()

        self.sbm       = 0
        self.imageList = []
        self.imageIndx = 0
        self.numImages = 0
        self.factor    = 1
        self.rotation  = 0
        self.width     = 0
        self.height    = 0
        self.size      = 0
        self.count     = 0
        self.mc        = False        # change mouse cursor
        self.mode      = 0            # rendering quality
        self.SetStatusText(str(self.mode), 4)

    def makeMenuBar(self):
        """Obtêm o caminho das imagens"""
        images_path = os.path.abspath(r'.\images')

        """Make a file menu with Open and Exit items"""
        fileMenu = wx.Menu()

        openItem = fileMenu.Append(wx.ID_OPEN, '', 'Selecionar pasta de imagens')
        openItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-open.png')))

        saveItem = fileMenu.Append(wx.ID_SAVE, '', 'Salvar o texto obtido')
        saveItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-save.png')))

        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT, 'Sair\tCtrl+Q', 'Encerrar o aplicativo')
        exitItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-quit.png')))

        # Make a edit menu with GetText and CleanText items
        editMenu = wx.Menu()

        getItem = editMenu.Append(wx.ID_EXECUTE, "Obtêm Texto\tCtrl+G", "Reconhece o texto da imagem")
        getItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-bold.png')))

        cleanItem = editMenu.Append(wx.ID_CLEAR, "Limpa Texto\tCtrl+L", "Limpa o texto obtido")
        cleanItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-clear.png')))

        # Make a view menu with ZoonIn, ZoonOut
        viewMenu = wx.Menu()

        zoomInItem = viewMenu.Append(wx.ID_ZOOM_IN, "Ampliar\tCtrl++", "Amplia a imagem")
        zoomInItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-zoom-in.png')))

        zoomOutItem = viewMenu.Append(wx.ID_ZOOM_OUT, "Reduzir\tCtrl+-", "Reduz a imagem")
        zoomOutItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-zoom-out.png')))

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT,'Sobre\tCtrl+A','Descreve as funcionalidades do aplicativo')
        aboutItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-about.png')))

        # Make the menu bar and add the menus to it.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "Arquivo")
        menuBar.Append(editMenu, "Editar")
        menuBar.Append(viewMenu, "Exibir")
        menuBar.Append(helpMenu, "Ajuda")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for each of the menu items.
        self.Bind(wx.EVT_MENU, self.onOpen, openItem)
        self.Bind(wx.EVT_MENU, self.onSave, saveItem)
        self.Bind(wx.EVT_MENU, self.onExit, exitItem)
        self.Bind(wx.EVT_MENU, self.onGetText, getItem)
        self.Bind(wx.EVT_MENU, self.onCleanText, cleanItem)
        self.Bind(wx.EVT_MENU, self.onZoomIn, zoomInItem)
        self.Bind(wx.EVT_MENU, self.onZoomOut, zoomOutItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)

    def onOpen(self, event):
        """Browse for directory"""
        dialog = wx.DirDialog (None, "Escolha a pasta com as imagens", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            self.directory = dialog.GetPath()
            self.onView()

    def onSave(self, event):
        """Pega texto obtido"""
        value = self.tc.GetValue()

        """Browse for directory"""
        fdlg = wx.FileDialog(None, "Entre com o caminho para o arquivo de resultado", "", "", "text files(*.txt)|*.*", wx.FD_SAVE)

        if fdlg.ShowModal() == wx.ID_OK:
            self.save_path = fdlg.GetPath() + ".txt"

            ocrFile = open(self.save_path, 'w', encoding="utf-8")
            ocrFile.write(value+'\r\n')
            ocrFile.close()

        fdlg.Destroy()

    def onView(self):
        self.loadDirectory()

        # Ok, ready to process this image
        self.processPicture()
        self.panel1.SetBackgroundColour((0,0,0,0))

        # Define event handlers
        self.panel1.Bind(wx.EVT_SIZE, lambda evt: self.rescale(evt,1))
        self.panel1.Bind(wx.EVT_MOUSEWHEEL,       self.zoom)
        self.panel1.Bind(wx.EVT_KEY_DOWN,         self.keyEvent)
        self.panel1.Bind(wx.EVT_MIDDLE_UP,        self.endDrag)
        self.panel1.Bind(wx.EVT_LEFT_DOWN,        self.next)
        self.panel1.Bind(wx.EVT_RIGHT_DOWN,       self.prev)

    def onExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def onAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox(""" Objetivo: exibir imagens (*.jpg, *.jpeg, *.png, *.bmp),
		                  manipulá-las (aplicar zoom, panorâmica e girar imagens) e
		                  obter textos.

Uso:
	* Roda do mouse para frente (para trás) aumenta o zoom (diminui). [semelhante ao Google Earth];
	* A tecla "r" gira a imagem na direção CW em incrementos de 90 graus;
	* A tecla "m" muda o modo PIL de qualidade normal (rápido) para alta qualidade (lento);
	* Imagens menores que 1000 x 1000 (largura x altura em pixels) terão renderização de alta qualidade;
	* O botão do meio do mouse pressionado enquanto arrasta, desloca a imagem, assim como as teclas de seta, se a imagem
	  for maior que a janela). [Semelhante ao Google Earth];
	* Clique no botão esquerdo (direito) do mouse para a próxima imagem (anterior) na lista de imagens;
	* Ctrl+O - Seleciona a pasta de imagens;
	* Ctrl+S - Salva o texto obtido;
	* Ctrl+Q - Fecha a aplicação;
	* Ctrl+G - Obtêm o texto xistente na imagem;
	* Ctrl+L - Limpa o texto obtido;
	* Ctrl++ - Amplia a image;
	* Ctrl+- - Reduz a imagem;
	* Ctrl+A - Exibe esta ajuda;""",
                       "Sobre o aplicativo de OCR",
                      wx.OK|wx.ICON_INFORMATION)

    def onGetText(self, event):
        if 'imageOCR' in globals():
            value = self.tc.GetValue()
            value += pytesseract.image_to_string(imageOCR)
            self.tc.SetValue(value + "\r\n")

    def onZoomIn(self, event):
        self.rescale(event,1.25)

    def onZoomOut(self, event):
        self.rescale(event,0.8)

    def onCleanText(self, event):
        value = ""
        self.tc.SetValue(value)  # Clear the text

    def loadDirectory(self):
        """
         Purpose: create a list of all image files that can be displayed
                  in the dir directory.
        """
        self.imageList = []
        for image in os.listdir(self.directory):
            if image.lower().endswith(    'jpg') \
               or image.lower().endswith( 'png') \
               or image.lower().endswith('jpeg') \
               or image.lower().endswith( 'gif') \
               or image.lower().endswith( 'bmp'):
                self.imageList.append(image)

        self.numImages = len(self.imageList)

    def processPicture(self, factor = 0):
        global imageOCR

        """
         Purpose: get image, define geometric parameters, scale,
                  show information in status bar, and display it.
        """
        fileName = self.imageList[self.imageIndx]

        fileName = os.path.join(self.directory, fileName)
        img = wx.Image(fileName)
        imageOCR = Image.open(fileName)

        self.width = img.GetWidth()
        self.height = img.GetHeight()

        ogHeight    = self.height
        ogWidth     = self.width
        xWin        = self.panel1.Size[0]
        yWin        = self.panel1.Size[1]
        winRatio    = 1.0*xWin/yWin
        imgRatio    = 1.0*self.width/self.height

        self.factor = factor*self.factor
        if factor == 0:
            self.factor = 1

        # Mode toggle
        mode = 0
        if (ogWidth <=1000 and ogHeight <= 1000) or self.mode == 1:
            mode = 1
        if imgRatio >= winRatio:
            # Match widths
            self.width  = self.factor*xWin
            self.height = self.factor*xWin/imgRatio
        else:
            # Match heights
            self.height = self.factor*yWin
            self.width  = self.factor*yWin*imgRatio

        img = img.Scale(round(self.width),round(self.height))

        # Update information in status bar
        label = str(int(100*self.width/ogWidth))  # scale (percent)
        self.SetStatusText(self.imageList[self.imageIndx], 0)
        self.SetStatusText(str(ogWidth) + 'x' + str(ogHeight), 1)
        self.SetStatusText(label + '%', 2)
        self.SetStatusText(str(self.imageIndx+1) + '/' + str(self.numImages), 3)

        # Check for rotation of image
        if self.rotation % 360 != 0:
            img_centre = wx.Point(round(img.GetWidth()/2), round(img.GetHeight()/2))
            img = img.Rotate(self.rotation, img_centre)
            self.width = img.GetWidth()
            self.height = img.GetHeight()

        self.showPicture(img)

    def showPicture(self,img):
        """
         Purpose: get bitmap, setup event handlers, and show image (refresh window).
        """
        bmp = wx.Bitmap(img)
        x = (self.panel1.Size[0] -  self.width)/2.0
        y = (self.panel1.Size[1] - self.height)/2.0

        tmp = wx.StaticBitmap(self.panel1,wx.ID_ANY,bmp,(round(x),round(y)))

        tmp.Bind(wx.EVT_LEFT_DOWN,    self.next   )
        tmp.Bind(wx.EVT_RIGHT_DOWN,   self.prev   )
        tmp.Bind(wx.EVT_MOTION,       self.drag   )
        tmp.Bind(wx.EVT_MIDDLE_UP,    self.endDrag)
        tmp.SetBackgroundColour((180,180,180,180))

        if self.sbm:
            self.sbm.Destroy()
        self.sbm = tmp
        self.panel1.Refresh()

    def next(self,event):
        """
         Purpose: process next image in image list.
        """
        if self.imageIndx == self.numImages-1:
            self.imageIndx = -1
        self.imageIndx += 1
        self.rotation = 0
        self.processPicture()

    def prev(self,event):
        """
         Purpose: process previous image in image list.
        """
        if self.imageIndx == 0:
            self.imageIndx = self.numImages
        self.imageIndx += -1
        self.rotation = 0
        self.processPicture()

    def rescale(self,event,factor):
        """
         Purpose: rescale image.
        """
        if self.GetStatusBar():
            self.processPicture(factor)

    def zoom(self,event):
        """
         Purpose: mouse wheel forward zooms in and mouse
                  wheel backwards zooms out.
        """
        factor = 1.25
        if event.GetWheelRotation() < 0:
            factor = 0.8
        self.rescale(event,factor)

    def keyEvent(self,event):
        """
         Purpose: process keys for control of image.
        """
        code = event.GetKeyCode()
        if code   == PLUS_KEY  or code == wx.WXK_NUMPAD_ADD:
            self.rescale(event,1.25)
        elif code == MINUS_KEY or code == wx.WXK_NUMPAD_SUBTRACT:
            self.rescale(event,0.8)
        elif code == R_KEY:
            # Rotation in CW direction by 90 degrees
            self.rotation = self.rotation + 90
            self.processPicture(1)
        elif (code in [wx.WXK_LEFT, wx.WXK_UP, wx.WXK_RIGHT, wx.WXK_DOWN]) and self.sbm:
            # Process arrow keys
            self.scroll(code)
        elif code == M_KEY:
            if self.mode == 0:
                self.mode = 1
            else:
                self.mode = 0

            self.SetStatusText(str(self.mode), 4)
            self.processPicture(1)

    def scroll(self,code):
        """
         Purpose: pan image with "arrow" keys.
        """
        boxPos = self.panel1.GetScreenPositionTuple()
        imgPos = self.sbm.GetScreenPositionTuple()
        delta = 20  # initialize pan translation

        if code == wx.WXK_LEFT and self.width > self.panel1.Size[0]:
            compare = boxPos[0] - imgPos[0]
            if compare <= delta:
                delta = max(compare,0)
            self.panel1.ScrollWindow(delta,0)

        if code == wx.WXK_UP and self.height > self.panel1.Size[1]:
            compare = boxPos[1] - imgPos[1]
            if compare <= delta:
                delta = max(compare,0)
            self.panel1.ScrollWindow(0,delta)

        if code == wx.WXK_RIGHT and self.width > self.panel1.Size[0]:
            compare =  imgPos[0] + self.sbm.Size[0] - boxPos[0] - self.panel1.Size[0]
            if compare <= delta:
                delta = max(compare,0)
            self.panel1.ScrollWindow(-delta,0)

        if code == wx.WXK_DOWN and self.height > self.panel1.Size[1]:
            compare =  imgPos[1] + self.sbm.Size[1] - boxPos[1] - self.panel1.Size[1]
            if compare <= delta:
                delta = max(compare,0)
            self.panel1.ScrollWindow(0,-delta)

    def drag(self,event):
        """
         Purpose: pan image with middle mouse button down.
        """
        if event.MiddleIsDown():
            if not self.mc:
                self.SetCursor(self.moveCursor)
                self.mc = True
            boxPos = self.panel1.GetScreenPosition()
            imgPos = self.sbm.GetScreenPosition()
            if self.count == 0:
                self.x = event.GetX()
                self.y = event.GetY()
            self.count +=  1
            if self.count > 1:
                deltaX = event.GetX() - self.x
                deltaY = event.GetY() - self.y
                if imgPos[0] >= boxPos[0] and deltaX > 0:
                    deltaX = 0
                if imgPos[0] + self.width <= boxPos[0] + self.panel1.Size[0] and deltaX < 0:
                    deltaX = 0
                if imgPos[1] >= boxPos[1] and deltaY > 0:
                    deltaY = 0
                if imgPos[1] + self.height <= boxPos[1] + self.panel1.Size[1] and deltaY < 0:
                    deltaY = 0
                self.panel1.ScrollWindow(2*deltaX,2*deltaY)
                self.count = 0

    def endDrag(self,event):
        """
          Purpose: clean-up after panning.
        """
        self.count = 0
        self.SetCursor(self.cursor)
        self.mc = False

if __name__ == '__main__':
    app = wx.App()
    frm = PythonOCR(None, title='Reconhecimento Ótico de Caracteres',size=(800,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
    frm.Show()
    app.MainLoop()
