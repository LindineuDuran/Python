import wx, os, re
import time
import PyPDF2
# from pdf2image import convert_from_path, convert_from_bytes
import ghostscript
import locale
from PIL import Image  # Importando o módulo Pillow para abrir a imagem no script
import pytesseract  # Módulo para a utilização da tecnologia OCR
from threading import *
from CheckBoxPanel import CheckBoxPanel

app_path = os.path.dirname(os.path.abspath(r'.'))
tesseract_path = os.path.join(app_path, 'Tesseract-OCR', 'tesseract.exe')
tessdata = os.path.join(app_path, 'Tesseract-OCR', 'tessdata')

if os.path.exists(tesseract_path):
    #pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    #tessdata_dir_config = r'--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
    tessdata_dir_config = '--tessdata-dir ' + tessdata

"""Define notification event for thread completion"""
EVT_RESULT_ID = 100

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class ThreadExtract(Thread):
    def __init__(self, main_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._main_window = main_window
        self.want_abort = 0
        self.start()

    def run(self):
        """Inicializa a progress_bar"""
        number_of_process = self._main_window.progress_bar.GetRange()
        self._main_window.progress_bar.SetValue(0)
        progress_bar_step = 1

        """Processa os PDFs"""
        for item in self._main_window.process_list:
            if self.want_abort:
                """Use a result of None to acknowledge the abort"""
                wx.PostEvent(self._main_window, ResultEvent(None))
                return

            self._main_window.progress_bar.SetValue(progress_bar_step)
            progress_bar_step += 1
            self._main_window.SetStatusText('Processando o arquivo ' + item)

            fileName = os.path.join(self._main_window.directory, item)
            pdf_file = open(fileName, 'rb')

            value = self._main_window.tc.GetValue()
            parsed = ''
            try:
                pdfReader = PyPDF2.PdfFileReader(fileName, strict=False)
                number_of_pages = pdfReader.getNumPages()
                try:
                    page = pdfReader.getPage(0)
                    page_content = page.extractText()
                    parsed = parsed.join(page_content).replace('\n', '')
                except:
                    print("Erro ao ler PDF! - " + fileName + '\r\n')
            except:
                print("Erro ao ler PDF! - " + fileName + '\r\n')

            if parsed != '':
                for x in range(number_of_pages):
                    page = pdfReader.getPage(x)
                    pdf = self.processa_texto(page)

                    value = self._main_window.tc.GetValue()
                    if pdf['chave'] == '': pdf['chave'] = 'Erro'
                    value += pdf['chave'] + '\t' + fileName + '\r\n'
                    # value += '=========================================================\r\n'
                    self._main_window.tc.SetValue(value)
            else:
                pdf = self.processa_imagem(fileName)

                value = self._main_window.tc.GetValue()
                if pdf['chave'] == '': pdf['chave'] = 'Erro'
                value += pdf['chave'] + '\t' + fileName + '\r\n'
                self._main_window.tc.SetValue(value)

            wx.Yield()
            time.sleep(1)

        self._main_window.SetStatusText('Fim do processo de extração!')
        wx.PostEvent(self._main_window, ResultEvent(1))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self.want_abort = 1

    def processa_texto(self, page):
        page_content = page.extractText()
        parsed = self.limpa_texto(page_content)
        pdf = self.processa_dados(parsed)

        return pdf

    def processa_imagem(self, fileName):
        pdf = {'chave': 'ERRO', 'fileName': fileName}

        img_file_path = self.convert_pdf_to_img(fileName)
        image = Image.open(img_file_path)
        if image is not None:
            texto = pytesseract.image_to_string(image)
            pdf = self.processa_dados(texto)

        image.close()

        return pdf

    def limpa_texto(self, page_content):
        parsed = ''.join(page_content)
        parsed = re.sub(' \n', '', parsed)

        return parsed

    def processa_dados(self, parsed):
        # chave = extrai_texto(parsed, '(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})|(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4})|(\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})|(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})|(\d{44})|(\d{24}) (\d{20})')
        chave = self.extrai_texto(parsed, '(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})')

        if chave is None:
            chave = self.extrai_texto(parsed, '(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4})')

        if chave is None:
            chave = self.extrai_texto(parsed, '(\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})')

        if chave is None:
            chave = self.extrai_texto(parsed, '(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})')

        if chave is None:
            chave = self.extrai_texto(parsed, '(\d{44})')

        if chave is None:
            chave = self.extrai_texto(parsed, '(\d{24}) (\d{20})')

        if chave is not None:
            chave = chave.group().replace('.', '').replace(' ', '').replace('\n', '')
        else:
            chave = ''

        pdf_info = {'chave': chave, 'fileName': parsed}

        return pdf_info

    def extrai_texto(self, texto, padrao):
        textoNovoRegex = re.compile(padrao)
        textoNovo = textoNovoRegex.search(texto)

        return textoNovo

    def pdf2jpeg(self, pdf_input_path, jpeg_output_path):
        args = []
        args = ["pef2jpeg", # actual value doesn't matter
                "-dNOPAUSE",
                "-sDEVICE=jpeg",
                "-dJPEGQ=100",
                "-r144",
                "-sOutputFile=" + jpeg_output_path,
                pdf_input_path]

        encoding = locale.getpreferredencoding()
        args = [a.encode(encoding) for a in args]

        try:
            ghostscript.Ghostscript(*args)
            ghostscript.cleanup()
        except:
            print("Erro", ghostscript.GhostscriptError)

    def convert_pdf_to_img(self, fileName):
        img_file_path = "{}jpg".format(fileName[:-3])

        self.pdf2jpeg(fileName, img_file_path,)
        if os.path.exists(img_file_path):
            return img_file_path
        else:
            return ''

class ExtractorFrame(wx.Frame):
    directory = ''
    process_list = list()

    def __init__(self,parent,id,title):
        """lista de ítens para processar"""
        self.process_list = list()

        """Create a frame"""
        wx.Frame.__init__(self,parent,id,title,size=(1024,500), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        """Create a panel for text"""
        self.panel1 = wx.Panel(self,-1,size=(725,415), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.panel1.SetBackgroundColour('#FFFFFF')

        """Create a customized panel of checkboxes"""
        self.panel2 = CheckBoxPanel(self, sizePanel=(293,415), posPanel=(725,0))
        self.panel2.SetBackgroundColour('#A0A0A0')

        """create a menu bar"""
        self.makeMenuBar()

        """and a status bar"""
        self.CreateStatusBar()
        # self.SetStatusText('PDF Extractor')

        """create a text box"""
        self.tc = wx.TextCtrl(self.panel1, -1, size=(725,415), style=wx.TE_MULTILINE)

        self.textbox = wx.BoxSizer(wx.VERTICAL)
        self.textbox.Add(self.tc,proportion=1,flag = wx.EXPAND)

        self.panel1.SetSizer(self.textbox)

        """create a progress bar"""
        self.progress_bar = wx.Gauge(self, wx.ID_ANY, 100, (0, 415), (1024, 15))

        """Set up event handler for any worker thread results"""
        EVT_RESULT(self, self.on_result)

        """No threads at start"""
        self.thread = None

    def makeMenuBar(self):
        """Obtêm o caminho dos icones"""
        images_path = os.path.abspath(r'.\icones')

        """Make a file menu with Open and Exit items"""
        fileMenu = wx.Menu()

        openItem = fileMenu.Append(wx.ID_OPEN, 'Abrir\tCtrl+O', 'Selecionar pasta de imagens')
        if os.path.exists(os.path.join(images_path, 'gtk-open.png')):
            openItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-open.png')))

        saveItem = fileMenu.Append(wx.ID_SAVE, 'Salvar\tCtrl+S', 'Salvar o texto obtido')
        if os.path.exists(os.path.join(images_path, 'gtk-save.png')):
            saveItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-save.png')))

        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT, 'Sair\tCtrl+Q', 'Encerrar o aplicativo')
        if os.path.exists(os.path.join(images_path, 'gtk-quit.png')):
            exitItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-quit.png')))

        """Make a edit menu with GetText and CleanText items"""
        editMenu = wx.Menu()

        getItem = editMenu.Append(wx.ID_EXECUTE, "Obtêm Chave\tCtrl+G", "Extrai a chave do PDF")
        if os.path.exists(os.path.join(images_path, 'gtk-execute.png')):
            getItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-execute.png')))

        stopItem = editMenu.Append(wx.ID_STOP, "Para Extração\tCtrl+T", "Para a extração dos textos do PDF")
        if os.path.exists(os.path.join(images_path, 'cross.png')):
            stopItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'cross.png')))

        cleanItem = editMenu.Append(wx.ID_CLEAR, "Limpa Texto\tCtrl+L", "Limpa o texto obtido")
        if os.path.exists(os.path.join(images_path, 'gtk-clear.png')):
            cleanItem.SetBitmap(wx.Bitmap(os.path.join(images_path, 'gtk-clear.png')))

        """Make the menu bar and add the menus to it."""
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "Arquivo")
        menuBar.Append(editMenu, "Editar")

        """Give the menu bar to the frame"""
        self.SetMenuBar(menuBar)

        """Finally, associate a handler function with the EVT_MENU event for each of the menu items."""
        self.Bind(wx.EVT_MENU, self.onOpen, openItem)
        self.Bind(wx.EVT_MENU, self.onSave, saveItem)
        self.Bind(wx.EVT_MENU, self.onExit, exitItem)
        self.Bind(wx.EVT_MENU, self.onGetText, getItem)
        self.Bind(wx.EVT_MENU, self.onStopExtract, stopItem)
        self.Bind(wx.EVT_MENU, self.onCleanText, cleanItem)

    def onOpen(self, event):
        """Browse for directory"""
        dialog = wx.DirDialog (None, "Escolha a pasta com os PDFs", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
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

            extractedFile = open(self.save_path, 'w', encoding="utf-8")
            extractedFile.write(value+'\r\n')
            extractedFile.close()

        fdlg.Destroy()

    def onView(self):
        """Retorna uma lista de strings com
           nomes de arquivo do diretório atual"""
        included_extensions = ['pdf','PDF']
        fileList = [fn for fn in os.listdir(self.directory)
                      if any(fn.endswith(ext) for ext in included_extensions)]

        """Cria CheckBoxs com nomes doa arquivos"""
        self.panel2.setTextList(fileList)
        if self.panel2.getTextList() is not None: self.panel2.createCheckBoxesList()

        self.panel2.SetupScrolling()
        self.panel2.Refresh()

    def onGetText(self, event):
        self.process_list = self.panel2.getProcessList()
        number_of_process = len(self.process_list)
        self.progress_bar.SetRange(number_of_process)

        value = self.tc.GetValue()
        if value == '':
            value += 'chave\tnome do arquivo\r\n'
            self.tc.SetValue(value)

        if not self.thread:
            self.thread = ThreadExtract(self)

    def onStopExtract(self, event):
        """Stop any task.
           Flag the worker thread to stop if running"""
        if self.thread:
            self.thread.abort()

    def onCleanText(self, event):
        value = ""
        self.tc.SetValue(value)  # Clear the text

    def on_result(self, event):
        value = self.tc.GetValue()
        if event.data is None:
            # Thread aborted (using our convention of None return)
            value += 'Aborted\r\n'
            self.tc.SetValue(value)
        else:
            value += 'Finished\r\n'
            self.tc.SetValue(value)
        # In either event, the worker is done
        self.thread = None

    def onExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)
