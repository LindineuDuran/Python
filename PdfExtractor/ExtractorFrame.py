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
        # self._main_window.directory = r'C:\Users\lindineu.duran\Downloads\PDFs - MELI'
        # self._main_window.process_list = ['2310-9699194331-4500183752.pdf','2311-9699194331-4500183752.pdf','2312 -  9699194331 - 45001837520.pdf','2313 - 9699194331 -  45001837520.pdf','231-9600021336-4500191333.pdf','233-9600021336-4500195329.pdf','23556 - 9699195478 - 4500201296.pdf','245-9600021370-4500195203.pdf','265-9699194964-4500194366.pdf','2714 - 9699193852 - 4500200622.pdf','298-9699194964-4500198269.pdf','314-9699194964-4500199253.pdf','32.588.153-9600021872-4500199452.pdf','32.588.310-9600021872-4500199453.pdf','3828 - 9699194245 - 4500194073.pdf','3829 - 9699194245 - 4500193982.pdf','3843 - 9699194245 - 4500194059.pdf','3846 - 9699194245 - 4500194000.pdf','542-9699194099-4500187438.pdf','599 -  9699194520  - 4500200706.pdf','63609-9600021505-4500194058.pdf','63611-9600021505-4500194057.pdf','64195-9600021505-4500198344.pdf','661 - 9600021270 - 4500199607.pdf','662 - 9600021270 - 4500200063.pdf','664.157-9600019604-4500194071.pdf','664156-9600019604-4500194075.pdf','664-9600021270-4500195870.pdf','665-9600021270-4500195976.pdf','667535 - 9600019604 - 4500198337.pdf','786 - 9699195435 - 4500201960 -.pdf','88 - 9699193256 - 4500202070.pdf','89 - 9699193256 - 4500199756.pdf','931-9699191508-4500194805.pdf','9821-9699191902-4500193888.pdf','9826-9699194675-4500194140.pdf','9830-9699191902-4500196225.pdf','9831-9699191902-4500196091.pdf','9832-9699191902-4500196092.pdf','9835-9699191902-4500196229.pdf','9836-9699191902-4500196122.pdf','9837-9699191902-4500196095.pdf','9838-9699191902-4500196125.pdf','9843-9699191902-4500196240.pdf','9844-9699191902-4500196174.pdf','9845-9699191902-4500196085.pdf','9849-9699191902-4500196099.pdf','9853-9699191902-4500196078.pdf']
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

            if parsed != '' and re.search('DANFE',parsed) is not None:
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

    def pdf2png(self, pdf_input_path, png_output_path):
        args = ["pdf2png", # actual value doesn't matter
                "-dNOPAUSE",
                "-sDEVICE=png16m",
                "-r300",
                "-sOutputFile=" + png_output_path,
                pdf_input_path]

        encoding = locale.getpreferredencoding()
        args = [a.encode(encoding) for a in args]

        try:
            ghostscript.Ghostscript(*args)
            ghostscript.cleanup()
        except:
            print("Erro", ghostscript.GhostscriptError)

    def convert_pdf_to_img(self, fileName):
        img_file_path = "{}png".format(fileName[:-3])

        self.pdf2png(fileName, img_file_path,)
        if os.path.exists(img_file_path):
            return img_file_path
        else:
            return ''

    def carrega_imagem_cortada(self, fileName):
        image = Image.open(fileName)
        width, height = image.size

        croppedIm = image.crop((0, 0, width, 700))
        croppedIm.save(fileName)

        image = Image.open(fileName)
        return image

    def processa_imagem(self, fileName):
        pdf = {'chave': 'ERRO', 'fileName': fileName}

        img_file_path = self.convert_pdf_to_img(fileName)
        image = self.carrega_imagem_cortada(img_file_path)
        if image is not None:
            texto = pytesseract.image_to_string(image)
            pdf = self.processa_dados(texto)

        image.close()

        if os.path.exists(img_file_path):
            try:
                os.remove(img_file_path)
            except OSError as e:
                print(e)
            else:
                print("File is deleted successfully")

        return pdf

    def limpa_texto(self, page_content):
        parsed = ''.join(page_content)
        parsed = re.sub(' \n', '', parsed)

        return parsed

    def processa_dados(self, parsed):
        chave = self.extrai_texto(parsed, r'(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})(\s{1,2})(\d{4})')
        if chave is not None: print("Critério 1 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{44})')
            if chave is not None: print("Critério 2 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})')
            if chave is not None: print("Critério 3 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})')
            if chave is not None: print("Critério 4 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{10}) (\d{7}) (\d{7}) (\d{11}) (\d{9})')
            if chave is not None: print("Critério 5 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{10}) (\d{7}) (\d{18}) (\d{9})')
            if chave is not None: print("Critério 6 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{6}) (\d{11}) (\d{7}) (\d{11}) (\d{9})')
            if chave is not None: print("Critério 7 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{3}) (\d{7}) (\d{7}) (\d{7}) (\d{11}) (\d{9})')
            if chave is not None: print("Critério 8 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{3}) (\d{7}) (\d{7}) (\d{18}) (\d{9})')
            if chave is not None: print("Critério 9 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{3}) (\d{7}) (\d{24}) (\d{1}) (\d{9})')
            if chave is not None: print("Critério 10 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{24}) (\d{20})')
            if chave is not None: print("Critério 11 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{17}) (\d{27})')
            if chave is not None: print("Critério 12 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{34}) (\d{10})')
            if chave is not None: print("Critério 13 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{17}) (\d{18}) (\d{9})')
            if chave is not None: print("Critério 14 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{17}) (\d{17}) (\d{10})')
            if chave is not None: print("Critério 15 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})\.(\d{4})')
            if chave is not None: print("Critério 16 - Chave: ", chave)
        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{2})([,|\.])(\d{4})([,|\.])(\d{2})([,|\.])(\d{3})([,|\.])(\d{3})/(\d{4})-(\d{2})-(\d{2})-(\d{3})-(\d{3})([,|\.])(\d{3})([,|\.])(\d{3})-(\d{3})([,|\.])(\s?)(\d{3})([,|\.])(\d{3})-(\d{1})')
            if chave is not None: print("Critério 17 - Chave: ", chave)

        if chave is None:
            chave = self.extrai_texto(parsed, r'(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})')
            if chave is not None: print("Critério 18 - Chave: ", chave)

        if chave is not None:
            chave = chave.group().replace('.', '').replace(',', '').replace('/', '').replace('-', '').replace(' ', '').replace('\n', '')
        else:
            chave = ''

        pdf_info = {'chave': chave, 'fileName': parsed}

        return pdf_info

    def extrai_texto(self, texto, padrao):
        textoNovoRegex = re.compile(padrao)
        textoNovo = textoNovoRegex.search(texto)

        return textoNovo

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
            self.save_path = self.define_extensao_arquivo(fdlg.GetPath())

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

    def define_extensao_arquivo(self, nome_arquivo):
        extensao = nome_arquivo[-4::]

        if extensao != '.txt': nome_arquivo += ".txt"

        return nome_arquivo
