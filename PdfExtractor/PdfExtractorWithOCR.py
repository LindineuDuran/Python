import sys
import os
from PyQt5 import uic, QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt as qt
import PyPDF2
import re
import pandas as pd
import csv
from pdf2image import convert_from_path, convert_from_bytes
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

class DocPdf:
    def __init__(self):
        self.fileName        = ''
        self.number_of_pages = 0
        self.pdf_content     = ''
        self.filtros         = ''
        self.pdf_info        = ''

    def setFileName(self, fileName):
        self.fileName = fileName

    def getFileName(self):
        return self.fileName

    def setNumberOfPages(self, number_of_pages):
        self.number_of_pages = number_of_pages

    def getNumberOfPages(self):
        return self.number_of_pages

    def setPdfContent(self, pdf_content):
        self.pdf_content = pdf_content

    def getPdfContent(self):
        return self.pdf_content

    def setFiltros(self, filtros):
        self.filtros = filtros

    def getFiltros(self):
        return self.filtros

    def setPdfInfo(self, pdf_info):
        self.pdf_info = pdf_info

    def getPdfInfo(self):
        return self.pdf_info


docPdf = DocPdf()

def extrai_texto(texto, padrao):
        textoNovoRegex = re.compile(padrao)
        textoNovo = textoNovoRegex.search(texto)

        return textoNovo

def limpa_texto(page_content):
    parsed = ''.join(page_content)
    parsed = re.sub(' \n', '', parsed)

    return parsed

def convert_pdf_to_img(fileName):
    image = Image.new('RGBA', (20, 20))
    try:
        dpi = 300 # dots per inch
        pages = convert_from_path(fileName ,dpi )

        if pages is not None:
            # print('imagem convertida 300 dpi: ' , fileName)
            image = pages[0]
    except:
        try:
            dpi = 200 # dots per inch
            pages = convert_from_path(fileName ,dpi )

            if pages is not None:
                # print('imagem convertida 200 dpi: ' , fileName)
                image = pages[0]
        except:
            print('Error ao converter o PDF em imagem ', fileName)

    return image

def processa_imagem(fileName):
    image = Image.new('RGBA', (20, 20))
    pdf = {"numNF": "ERRO", "cnpj": "cnpj", "chave": fileName, "parsed": "parsed"}

    image = convert_pdf_to_img(fileName)
    if image is not None:
        # print('imagem convertida: ' , fileName)
        texto = pytesseract.image_to_string(image)
        # print('texto extraído: ' , texto)
        pdf = processa_dados(texto)

    imgFileName = "{}jpg".format(fileName[:-3])
    if os.path.exists(imgFileName):
        os.remove(imgFileName)

    return pdf

def processa_texto(page):
    page_content = page.extractText()
    parsed = limpa_texto(page_content)
    pdf = processa_dados(parsed)
    return pdf

def processa_dados(parsed):
        numNF = extrai_texto(parsed, "N° (\d{3}).(\d{3}).(\d{3})|N° (\d{1,10})|Nº.  (\d{1,10})    FL 1|No. (\d{1,10})Série|N°(\d{1,10})SÉRIE")
        if numNF is not None:
            numNF = extrai_texto(numNF.group(), "(\d{3}).(\d{3}).(\d{3})|(\d{1,10})")

            if numNF is not None:
                try:
                    numNF = int(numNF.group().replace('.', '').replace(',', ''))
                except:
                    print('numNF: ', numNF)
            else:
                numNF = ''
        else:
            numNF = ''

        cnpj = extrai_texto(parsed, "(\d{1,3}).(\d{3}).(\d{3})/(\d{4})\\n-\\n(\d{2})|(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})")
        if cnpj is not None:
            cnpj = extrai_texto(cnpj.group(), "(\d{1,3}).(\d{3}).(\d{3})/(\d{4})\\n-\\n(\d{2})|(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})")

            if cnpj is not None:
                cnpj = cnpj.group().replace('\n-\n', '').replace('.', '').replace('-', '').replace('/', '')
            else:
                cnpj = ''
        else:
            cnpj = ''

        chave = extrai_texto(parsed, '(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})|(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4})|(\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})|(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})|(\d{44})')

        if chave is not None:
            chave = chave.group().replace('.', '').replace(' ', '').replace('\n', '')
        else:
            chave = ''

        pdf_info = {"numNF": str(numNF), "cnpj": cnpj, "chave": chave, "parsed": parsed}

        return pdf_info

class Worker(qtc.QObject):
    processed = qtc.pyqtSignal(str, str, str, str)

    @qtc.pyqtSlot(str, list)
    def obter_info(self, data_path, process_list):
        """Processa os PDFs"""
        for item in process_list:
            fileName = os.path.join(data_path, item)

            pdf_file = open(fileName, 'rb')

            try:
                pdfReader = PyPDF2.PdfFileReader(fileName, strict=False)
                number_of_pages = pdfReader.getNumPages()

                page = pdfReader.getPage(0)
                page_content = page.extractText()
                parsed = ''.join(page_content).replace('\n', '')

                # print('page_content: ' , page_content)

                if parsed != '' and 'CNPJ' in parsed:
                    for x in range(number_of_pages):
                        page = pdfReader.getPage(x)
                        pdf = processa_texto(page)

                        if pdf is not None:
                            docPdf.setPdfInfo(pdf)
                            if pdf['chave'] == '': pdf['chave'] = fileName
                            self.processed.emit(pdf['numNF'], pdf['cnpj'], pdf['chave'], fileName)
                        else:
                            self.processed.emit(pdf['numNF'], pdf['cnpj'], fileName, fileName)
                else:
                    # print('processa imagem: ' , fileName)
                    pdf = processa_imagem(fileName)

                    if pdf is not None:
                        docPdf.setPdfInfo(pdf)
                        if pdf['chave'] == '': pdf['chave'] = fileName
                        self.processed.emit(pdf['numNF'], pdf['cnpj'], pdf['chave'], fileName)
                    else:
                        self.processed.emit(pdf['numNF'], pdf['cnpj'], fileName, fileName)
            except:
                # print("Erro ao ler PDF! - " + fileName)
                self.processed.emit('Erro', page_content, fileName, '')


class Ui_MainWindow(qtw.QMainWindow):
    process_list = list()
    data_path = ''

    pdf_requested = qtc.pyqtSignal(str, list)

    columns = ['numNF', 'cnpj', 'chave']
    dfPDF = pd.DataFrame(columns=columns)

    # Configura interface
    def __init__(self, parent=None):
        super(qtw.QMainWindow, self).__init__()
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname,'frmPdfExtratorWithOCR.ui'), self)

        """Define o Título da Janela"""
        self.setWindowTitle("Pdf Extractor")

        """Guarda o Diretório da Aplicação"""
        self.application_path = os.getcwd()

        """checkboxes list"""
        self.scrollAreaWidgetContents = qtw.QWidget()
        self.scrollAreaWidgetContents.setGeometry(qtc.QRect(0, 0, 299, 319))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = qtw.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.saCheckBoxList.setWidget(self.scrollAreaWidgetContents)

        self.createActions()
        self.createMenus()

        """configura thread"""
        qtc.QMetaObject.connectSlotsByName(self)

        """Create a worker object and a thread"""
        self.worker = Worker()
        self.worker_thread = qtc.QThread()
        self.worker.processed.connect(self.atualiza_interface)
        self.pdf_requested.connect(self.worker.obter_info)

        """Assign the worker to the thread and start the thread"""
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    def createActions(self):
        self.actionSelect_Folder = qtw.QAction("&Select Folder", self, shortcut="Ctrl+S", triggered=self.selectDir)
        self.actionExit = qtw.QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.btnProcessar.clicked.connect(self.inicia_extracao)
        self.btnLimpar.clicked.connect(self.limpar)
        self.btnSalvar.clicked.connect(self.save_data_grid)

    def createMenus(self):
        self.menuAction.addAction(self.actionSelect_Folder)
        self.menuAction.addAction(self.actionExit)

    # Seleciona Diretório de Trabalho
    def selectDir(self):
        """Abre Dialogo de Abrir Arquivo"""
        selected_dir = qtw.QFileDialog.getExistingDirectory(self, caption='Choose Directory', directory=os.getcwd())

        if selected_dir != '':
            """Alterar o diretório de trabalho atual"""
            os.chdir(selected_dir)

            """Guarda o Diretório dos Dados"""
            self.data_path = os.getcwd()

            """Retorna uma lista de strings com
               nomes de arquivo do diretório atual"""
            fileList = os.listdir(os.getcwd())

            """Cria CheckBoxs com nomes doa arquivos"""
            cb_widget_list = list()
            for item in fileList:
                if item.endswith('.pdf') or item.endswith('.PDF'):
                    widget = qtw.QCheckBox(item)
                    widget.stateChanged.connect(lambda state, checkbox=item: self.update(state, checkbox))
                    cb_widget_list.append(widget)

            """Insere os checkboxes na lista"""
            for widget in cb_widget_list:
                self.verticalLayout.addWidget(widget)

    # Atualiza lista de checkboxes
    def update(self, state, origin: str):
        if state:
            self.process_list.append(origin)
        else:
            self.process_list.remove(origin)

    # Rotina principal de tratamento de dados
    def inicia_extracao(self):
        """Inicializa Tabela de resultados"""
        if self.process_list:
            self.tbvExtratacao.setColumnCount(4)
            self.tbvExtratacao.setHorizontalHeaderLabels(['#', 'numNF', 'cnpj', 'chave'])
            self.tbvExtratacao.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
            self.tbvExtratacao.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        """Dispara o processo de extração"""
        self.pdf_requested.emit(self.data_path, self.process_list)

    # Atualiza a interface, exibindo os dados lidos
    def atualiza_interface(self, numNF, cnpj, chave, fileName):
        """Insere no Grid a linha obtida"""
        row = self.tbvExtratacao.rowCount()
        self.tbvExtratacao.insertRow(row)

        aqr_icon = os.path.join(self.application_path, 'images', 'cross.png')
        self.btn_del = qtw.QPushButton(qtg.QIcon(aqr_icon),'')
        self.btn_del.clicked.connect(self.handleButtonClicked)
        self.tbvExtratacao.setCellWidget(row,0,self.btn_del)

        self.tbvExtratacao.setItem(row, 1, qtw.QTableWidgetItem(numNF))
        self.tbvExtratacao.setItem(row, 2, qtw.QTableWidgetItem(cnpj))
        self.tbvExtratacao.setItem(row, 3, qtw.QTableWidgetItem(chave))

        """Salva no arquivo a linha obtida"""
        self.salvar_arquivo(numNF, cnpj, chave, fileName)

        """Escreve o nome do arquivo na StatusBar"""
        self.statusBar().showMessage(fileName)

    # Obtêm caminho dos arquivos
    def extrai_caminho(self):
        fileName = docPdf.getFileName()
        arrFileName = fileName.split('\\')
        caminho = ''

        for x in range(len(arrFileName)-1):
            caminho = caminho + arrFileName[x] + '\\'

        return caminho

    # Salva dados em arquivo texto
    def salvar_arquivo(self, numNF, cnpj, chave, fileName):
        """Limpa o conteúdo do arquivo de saída ou mantêm"""
        caminho = self.extrai_caminho()
        fileNameOut = os.path.join(caminho,'TextoExtraido.txt')

        if os.path.exists(fileNameOut) and not self.chBoxNewOutputFile.isChecked():
            self.dfPDF = pd.read_csv(fileNameOut, encoding='ISO-8859-1', sep=';')
            self.dfPDF.loc[len(self.dfPDF)]= [str(numNF), str(cnpj), str(chave)]
        else:
            self.dfPDF.loc[len(self.dfPDF)]= [str(numNF), str(cnpj), str(chave)]

        """output csv"""
        self.dfPDF = self.dfPDF.drop_duplicates(subset='chave', keep='first')
        self.dfPDF.to_csv(fileNameOut, encoding='latin-1', sep = ';', index = False)

    # Salva o grid todo
    def save_data_grid(self):
        """Obtêm o DataFrame dos Dados Processados"""
        if self.tbvExtratacao.model() is not None:
            """Inicializa DataFrame"""
            # columns = ['numNF', 'cnpj', 'chave']
            # data = {}
            # df = pd.DataFrame(data, columns=columns)
            df = pd.DataFrame()

            # """Define o nome do arquivo pelo tipo de processamento"""
            # caminho = self.extrai_caminho()
            # fileNameOut = os.path.join(caminho,'DadosPDF.txt')

            """Abre Dialogo de Salvar Arquivo"""
            fileNameOut = qtw.QFileDialog.getSaveFileName(self, 'Save File', 'DadosPDF.txt', 'TXT files (*.txt)')

            rows = self.tbvExtratacao.rowCount()
            columns = self.tbvExtratacao.columnCount()

            for i in range(rows):
                for j in range(columns):
                    if self.tbvExtratacao.item(i, j) is not None:
                        df.loc[i, j] = str(self.tbvExtratacao.item(i, j).text())
                    else:
                        df.loc[i, j] = ''

            """Rename multiple columns in one go with a larger dictionary"""
            df = df.rename (columns={1 :  'numNF', 2 :  'cnpj', 3 :  'chave'})

            """Resetando o index para juntar no concatenar"""
            df = df.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna

            """elimina coluna 0"""
            df = df.drop(columns=[0])

            """output csv"""
            df.to_csv(fileNameOut[0], encoding='latin-1', sep = '\t', index = False)

    # Gera um DataFrame vazio
    def inicializa_data_frame(self):
        """Inicializa DataFrame"""
        columns = ['numNF', 'cnpj', 'chave']
        data = {}
        self.dfPDF = pd.DataFrame(data, columns=columns)

    # Limpar status atual
    def limpar(self):
        """Prepare the GUI and emit the hash_requested signal"""

        """Limpa tabela de resultado da extração e campo de texto lido"""
        while self.tbvExtratacao.rowCount() > 0:
            self.tbvExtratacao.removeRow(0)
        self.tbvExtratacao.setColumnCount(0)

        """Limpa a StatusBar"""
        self.statusBar().showMessage('')

        """Limpa lista de checkboxes"""
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        """Limpa lista de ítens à processar"""
        self.process_list.clear()

        """Limpa o caminho para os dados"""
        self.data_path = ''

        """Inicializa DataFrame"""
        self.inicializa_data_frame()

        """output csv"""
        caminho = self.extrai_caminho()
        if self.chBoxNewOutputFile.isChecked():
            with open(caminho + "TextoExtraido.txt", "w") as f:
                wr = csv.writer(f, delimiter=';')
                wr.writerow(['numNF', 'cnpj', 'chave'])


    # Deletar linha do grid
    def handleButtonClicked(self):
        # button = QtGui.qApp.focusWidget()
        button = self.sender()
        if button:
            row = self.tbvExtratacao.indexAt(button.pos()).row()
            self.tbvExtratacao.removeRow(row)

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
