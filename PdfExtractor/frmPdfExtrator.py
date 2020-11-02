import sys
import os
from PyQt5 import uic, QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt as qt
# from PyQt5.QtGui import QIcon
import PyPDF2
import re
import pandas as pd
import csv

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

def processa_dados(page, filtros):
        page_content = page.extractText()
        parsed = limpa_texto(page_content)

        numNF = extrai_texto(parsed, filtros['PrimeiroPadraoPesq'])
        if numNF is not None:
            numNF = extrai_texto(numNF.group(), filtros['PrimeiroPadraoDesejado'])

            if numNF is not None:
                numNF = numNF.group()
            else:
                numNF = ''
        else:
            numNF = ''

        cnpj = extrai_texto(parsed, filtros['SegundoPadraoPesq'])
        if cnpj is not None:
            cnpj = extrai_texto(cnpj.group(), filtros['SegundoPadraoDesejado'])

            if cnpj is not None:
                cnpj = cnpj.group().replace('\n-\n', '').replace('.', '').replace('-', '').replace('/', '')
            else:
                cnpj = ''
        else:
            cnpj = ''

        chave = extrai_texto(parsed, filtros['TerceiroPadraoPesq'])
        if chave is not None:
            chave = extrai_texto(chave.group(), filtros['TerceiroPadraoDesejado'])

            if chave is not None:
                chave = chave.group().replace(' ', '')
            else:
                chave = ''
        else:
            chave = ''

        pdf_info = {"numNF": numNF, "cnpj": cnpj, "chave": chave, "parsed": parsed}

        return pdf_info

class Worker(qtc.QObject):
    processed = qtc.pyqtSignal(int, str, str, str, str)

    @qtc.pyqtSlot(str)
    def obter_info(self, fileName):
        pdf_file = open(fileName, 'rb')
        pdfReader = PyPDF2.PdfFileReader(fileName)
        number_of_pages = pdfReader.getNumPages()

        filtros = docPdf.getFiltros()

        for x in range(number_of_pages):
            page = pdfReader.getPage(x)
            pdf = processa_dados(page, filtros)

            if pdf is not None:
                docPdf.setPdfInfo(pdf)
                self.processed.emit(x, pdf['numNF'], pdf['cnpj'], pdf['chave'], pdf['parsed'])

class Ui_MainWindow(qtw.QMainWindow):
    pdf_requested = qtc.pyqtSignal(str)

    columns = ['numNF', 'cnpj', 'chave']
    dfXML = pd.DataFrame(columns=columns)

    # Configura interface
    def __init__(self, parent=None):
        super(qtw.QMainWindow, self).__init__()
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname,'frmPdfExtrator.ui'), self)

        self.setWindowTitle("Pdf Extractor")

        """Guarda o Diretório da Aplicação"""
        self.application_path = os.getcwd()

        """buttons"""
        self.btnSelecionarArquivo.clicked.connect(self.selectPDF)
        self.btnProcessar.clicked.connect(self.inicia_extracao)
        self.btnLimpar.clicked.connect(self.limpar)
        self.btnSair.clicked.connect(qtw.QApplication.quit)

        """comboboxes"""
        self.cboPrimeiroPadraoPesq.addItem("Nº.  (\d{1,10})    FL 1 / 1")
        self.cboPrimeiroPadraoPesq.addItem("No. (\d{1,10})Série")
        self.cboPrimeiroPadraoPesq.addItem("N°(\d{1,10})SÉRIE(\d{1,2})")
        self.cboPrimeiroPadraoPesq.addItem("SaídaNº (\d{1,10})SÉRIE (\d{1,2})")
        self.cboPrimeiroPadraoPesq.setEditable(3)

        self.cboPrimeiroPadraoDesejado.addItem("(\d{1,10})")
        self.cboPrimeiroPadraoDesejado.setEditable(3)

        self.cboSegundoPadraoPesq.addItem("CNPJ\\n(\d{1,3}).(\d{3}).(\d{3})/(\d{4})\\n-\\n(\d{2})")
        self.cboSegundoPadraoPesq.addItem("(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})N°(\d{2,8})SÉRIE")
        self.cboSegundoPadraoPesq.addItem("CNPJ(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})CHAVE")
        self.cboSegundoPadraoPesq.addItem("CNPJ(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})")
        self.cboSegundoPadraoPesq.setEditable(3)

        self.cboSegundoPadraoDesejado.addItem("(\d{1,3}).(\d{3}).(\d{3})/(\d{4})\\n-\\n(\d{2})")
        self.cboSegundoPadraoDesejado.addItem("(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})")
        self.cboSegundoPadraoDesejado.setEditable(3)

        self.cboTerceiroPadraoPesq.addItem("CHAVE DE ACESSO\\n(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})")
        self.cboTerceiroPadraoPesq.addItem("CHAVE DE ACESSO(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})")
        self.cboTerceiroPadraoPesq.addItem("CHAVE DE ACESSO P/ CONSULTA DE AUTENTICIDADE(\d{44})")
        self.cboTerceiroPadraoPesq.addItem("AUTENTICIDADE(\d{44,59})DESTINATÁRIO|AUTENTICIDADE(\d{44,59})CÓD")
        self.cboTerceiroPadraoPesq.setEditable(3)

        self.cboTerceiroPadraoDesejado.addItem("(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})")
        self.cboTerceiroPadraoDesejado.addItem("(\d{44,59})")
        self.cboTerceiroPadraoDesejado.setEditable(3)

        """Tabela de resultados"""
        self.tbvExtratacao.setColumnCount(4)
        self.tbvExtratacao.setHorizontalHeaderLabels(['#', 'numNF', 'cnpj', 'chave'])
        self.tbvExtratacao.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        self.tbvExtratacao.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

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

    # Seleciona arquivo que será lido
    def selectPDF(self):
        """Limpa o campo de texto lido"""
        self.pteTextoLido.clear()  # Clear the text

        """Abre Dialogo de Abrir Arquivo"""
        fileName, _ = qtw.QFileDialog.getOpenFileName(None, "Select Image", "",
                                                            "PDF Files (*.pdf, *.PDF);;All Files (*)")  # Ask for file
        if fileName:  # If the user gives a file
            fileName = fileName.replace("/", "\\")
            self.pteTextoLido.insertPlainText(fileName + "\r\n")

            """Lê o PDF"""
            pdf_file = open(fileName, 'rb')
            read_pdf = PyPDF2.PdfFileReader(pdf_file)

            number_of_pages = read_pdf.getNumPages()
            self.pteTextoLido.insertPlainText(str(number_of_pages) + "\r\n")
            self.pteTextoLido.insertPlainText("==================================\r\n")

            """Guarda dados de fileName, number_of_pages e conteúdo do PDF no objeto docPdf"""
            docPdf.setFileName(fileName)
            docPdf.setNumberOfPages(number_of_pages)
            docPdf.setPdfContent(read_pdf)

            """Limpa o DataFrame"""
            columns = ['numNF', 'cnpj', 'chave']
            data = {}
            self.dfXML = pd.DataFrame(data, columns=columns)

            """Limpa o conteúdo do arquivo de saída"""
            caminho = self.extrai_caminho()
            fileNameOut = os.path.join(caminho,'TextoExtraido.txt')

            if os.path.exists(fileNameOut) and not self.chBoxNewOutputFile.isChecked():
                dfAnterior = pd.read_csv(fileNameOut, encoding='ISO-8859-1', sep=';')
                frames = [dfAnterior, self.dfXML]
                self.dfXML = pd.concat(frames)
            else:
                with open(fileNameOut, "w") as f:
                    wr = csv.writer(f, delimiter=';')
                    wr.writerow(['numNF', 'cnpj', 'chave'])

    # Define dicionário de filtros à partir das ComboBox
    def obter_filtros(self):
        filtros = {'PrimeiroPadraoPesq'     : self.cboPrimeiroPadraoPesq.currentText(),
                   'PrimeiroPadraoDesejado' : self.cboPrimeiroPadraoDesejado.currentText(),
                   'SegundoPadraoPesq'      : self.cboSegundoPadraoPesq.currentText(),
                   'SegundoPadraoDesejado'  : self.cboSegundoPadraoDesejado.currentText(),
                   'TerceiroPadraoPesq'     : self.cboTerceiroPadraoPesq.currentText(),
                   'TerceiroPadraoDesejado' : self.cboTerceiroPadraoDesejado.currentText()}

        return filtros

    # Inicia processo de leitura do PDF
    def inicia_extracao(self):
        """Obtêm os filtros"""
        filtros = self.obter_filtros()
        docPdf.setFiltros(filtros)

        """Emit the signal"""
        fileName = docPdf.getFileName()
        if fileName:
            self.pdf_requested.emit(fileName)

    # Atualiza a interface, exibindo os dados lidos
    def atualiza_interface(self, pagina, numNF, cnpj, chave, parsed):
        row = self.tbvExtratacao.rowCount()
        self.tbvExtratacao.insertRow(row)

        aqr_icon = os.path.join(self.application_path, 'images', 'cross.png')
        self.btn_del = qtw.QPushButton(qtg.QIcon(aqr_icon),'')
        self.btn_del.clicked.connect(self.handleButtonClicked)
        self.tbvExtratacao.setCellWidget(row,0,self.btn_del)

        self.tbvExtratacao.setItem(row, 1, qtw.QTableWidgetItem(numNF))
        self.tbvExtratacao.setItem(row, 2, qtw.QTableWidgetItem(cnpj))
        self.tbvExtratacao.setItem(row, 3, qtw.QTableWidgetItem(chave))

        self.pteTextoLido.insertPlainText("Página " + str(pagina) + " foi processada." + "\r\n")
        self.pteTextoLido.insertPlainText(parsed)
        self.pteTextoLido.insertPlainText("==================================\r\n")

        self.dfXML.loc[len(self.dfXML)]= [str(numNF), str(cnpj), str(chave)]
        self.salvar_arquivo(self.dfXML)

    # Obtêm caminho dos arquivos
    def extrai_caminho(self):
        fileName = docPdf.getFileName()
        arrFileName = fileName.split('\\')
        caminho = ''

        for x in range(len(arrFileName)-1):
            caminho = caminho + arrFileName[x] + '\\'

        return caminho

    # Salva dados em arquivo texto
    def salvar_arquivo(self, dfXML):
        caminho = self.extrai_caminho()
        fileNameOut = caminho + 'TextoExtraido.txt'

        """output csv"""
        dfXML.to_csv(fileNameOut, encoding='latin-1', sep = ';', index = False)

    # Limpar status atual
    def limpar(self):
        """Prepare the GUI and emit the hash_requested signal"""
        """Limpa tabela de resultado da extração e campo de texto lido"""
        self.pteTextoLido.clear()  # Clear the text
        while self.tbvExtratacao.rowCount() > 0:
            self.tbvExtratacao.removeRow(0)

        """Inicializa DataFrame"""
        columns = ['numNF', 'cnpj', 'chave']
        data = {}
        self.dfXML = pd.DataFrame(data, columns=columns)

        """output csv"""
        caminho = self.extrai_caminho()
        if self.chBoxNewOutputFile.isChecked():
            with open(caminho + "TextoExtraido.txt", "w") as f:
                wr = csv.writer(f, delimiter=';')
                wr.writerow(['numNF', 'cnpj', 'chave'])

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
