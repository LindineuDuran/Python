#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import pandas as pd
from datetime import datetime

from ConsultaBanco import ConsultaBanco
from XML_Tools import XML_Tools
from TableModel import TableModel

from PyQt5 import QtWidgets as qtw, uic
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt as qt, QPersistentModelIndex, QModelIndex

class GUI(qtw.QDialog):
    process_list = list()
    aplication_path = ''
    data_path = ''
    dfPadrao = ''

    # Configura interface
    def __init__(self):
        super(GUI, self).__init__()

        """Guarda o Diretório da Aplicação"""
        self.aplication_path = os.getcwd()

        uic.loadUi(os.path.join(self.aplication_path,'main.ui'), self)

        """buttons"""
        self.btnSelectPath.clicked.connect(self.selectDir)
        self.btnProcessar.clicked.connect(self.processar)
        self.btSave.clicked.connect(self.save_data)
        self.btnDeleteRow.clicked.connect(self.delete_rows)
        self.btnSair.clicked.connect(qtw.QApplication.quit)

        """checkboxes list"""
        self.scrollAreaWidgetContents = qtw.QWidget()
        self.scrollAreaWidgetContents.setGeometry(qtc.QRect(0, 0, 299, 319))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = qtw.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.saCheckBoxList.setWidget(self.scrollAreaWidgetContents)

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
                if item.endswith('.xml'):
                    widget = qtw.QCheckBox(item)
                    widget.stateChanged.connect(lambda state, checkbox=item: self.update(state, checkbox))
                    cb_widget_list.append(widget)

            for widget in cb_widget_list:
                self.verticalLayout.addWidget(widget)

    # Atualiza lista de checkboxes
    def update(self, state, origin: str):
        if state:
            self.process_list.append(origin)
        else:
            self.process_list.remove(origin)

    # Insere dados no Grid
    def carrega_tableview(self, dataframe):
        self.model = TableModel(dataframe)
        self.tbvExtratacao.setModel(self.model)

    # Obtêm Tags do layout Padrão
    def obtem_tags_padrao(self):
        """Carrega JSON em DataFrame, fazendo tranposição de Dados"""
        aqr_json = os.path.join(self.aplication_path, 'Tags.JSON')
        self.dfPadrao = pd.read_json(aqr_json).T

        """Obtêm os índices do DataFrame de Json"""
        tags_list = list(self.dfPadrao.index.values)

        self.dfPadrao = pd.DataFrame(tags_list, columns=['nome'])

        self.carrega_tableview(self.dfPadrao)

    # Concatena o Nome do Arquivo com a Data de Hoje
    def cria_nome_arq(self, Nome):
        """Obtêm data e hora atuais"""
        now     = datetime.now()
        ano     = now.year
        mes     = now.month
        dia     = now.day
        hora    = now.hour
        minuto  = now.minute
        segundo = now.second

        """Forma nome do arquivo"""
        file_name = Nome + ' - ' + str(ano) + '.' + str(mes) + '.' + str(dia) + ' ' + str(hora) + '_' + str(minuto) + '_' + str(segundo) + '.txt'

        return file_name

    # Elimina as linhas selecionadas do Grid
    def delete_rows(self):
        index_list = []
        if self.tbvExtratacao.model() is not None:
            for model_index in self.tbvExtratacao.selectionModel().selectedRows():
                index = QPersistentModelIndex(model_index)
                index_list.append(index)

            # print(f'Before delete_rows():\tself.df.shape(): {self.tbvExtratacao.model()._data.shape}')
            for index in index_list:
                self.tbvExtratacao.model().layoutAboutToBeChanged.emit()
                self.tbvExtratacao.model().removeRow(index.row())
                self.tbvExtratacao.model().layoutChanged.emit()
                self.tbvExtratacao.model()._data = self.tbvExtratacao.model()._data.drop([int(index.row())], axis=0)
            # print(f'After delete_rows():\tself.df.shape(): {self.tbvExtratacao.model()._data.shape}')

            if self.tbvExtratacao.model() is not None:
                dfProcess = self.tbvExtratacao.model()._data.reset_index(level=0, drop=True)

                """Preenche a TableView"""
                self.carrega_tableview(dfProcess)

        return

    # Obtêm Tags do(s) Arquivo(s) selecionado(s)
    def processar_layout(self):
        """Lê json de Tags Padrão
           e exibe na tabela"""
        self.obtem_tags_padrao()

        """Processa os XMLs"""
        for item in self.process_list:
            """Interpreta XML"""
            metadata = os.path.join(self.data_path, item)
            xt = XML_Tools()
            root = xt.intrepreta_xml(metadata)

            """Obtêm Tags"""
            columns = ['tag']
            dfTags = pd.DataFrame(columns=columns)
            dfTags = xt.obtem_tags(root, dfTags)

            CodigoMunicipio = ''
            Municipio = ''
            PrestadoCNPJ = ''
            NuNFSe = ''

            """Obtêm o Código do Município"""
            cb = ConsultaBanco(os.path.join(self.aplication_path, 'BaseRFE.db'))
            sql = """select t.id, t.nome, t.tag, t.tag_pai, t.id_tipo, x.descricao
                                         from rfe_tags t, rfe_tipos_xml x
                                         where (t.nome = 'MunGer' or
                                                t.nome = 'MunicipioGerador')
                                           and t.tag <> ''
                                           and t.id_tipo = x.id
                                         order by t.id_tipo;"""

            valor = cb.PesquisarValorTag(root, sql)
            if valor.isnumeric():
                CodigoMunicipio = cb.PesquisarValorTag(root, sql)
            else:
                Municipio = cb.PesquisarValorTag(root, sql)

            if CodigoMunicipio != '':
                """Obtêm o Município"""
                sql = "select municipio from rfe_municipios where cod_ibge = " + CodigoMunicipio
                Municipio = cb.PesquisaItem(sql)

            """Obtêm o Layout mais parecido"""
            dfTagsLayout = cb.ObtemLayout(Municipio,CodigoMunicipio,root)

            dfOuter = pd.merge(dfTagsLayout, dfTags, on='tag', how='right')
            dfOuter = pd.merge(self.dfPadrao,dfOuter, on='nome', how='outer')

            """Preenche a TableView"""
            self.carrega_tableview(dfOuter.drop_duplicates().reset_index(level=0, drop=True))

    # Obtêm Município, CNPJ do Prestador e Número da Nota
    def processar_dados(self):
        """Define DataFrame para receber resultado do processamento"""
        columns = ['File', 'Código Município', 'Município', 'PrestadoCNPJ', 'NuNFSe']
        dfNFSe = pd.DataFrame(columns=columns)

        CodigoMunicipio = ''
        PrestadoCNPJ = ''
        NuNFSe = ''

        """Processa os XMLs"""
        for item in self.process_list:
            # Interpreta XML
            metadata = os.path.join(self.data_path, item)
            xt = XML_Tools()
            root = xt.intrepreta_xml(metadata)

            """Obtêm o Código do Município"""
            cb = ConsultaBanco(os.path.join(self.aplication_path, 'BaseRFE.db'))
            sql = """select t.id, t.nome, t.tag, t.tag_pai, t.id_tipo, x.descricao
                                         from rfe_tags t, rfe_tipos_xml x
                                         where nome = 'MunGer'
                                           and descricao <> 'PADRAO'
                                           and t.id_tipo = x.id
                                         order by t.id_tipo;"""

            CodigoMunicipio = cb.PesquisarValorTag(root, sql)

            """Obtêm o Município"""
            Municipio = ""
            if CodigoMunicipio != '':
                sql = "select municipio, cod_uf, cod_ibge from rfe_municipios where cod_ibge = " + str(CodigoMunicipio)
                Municipio = cb.PesquisaItem(sql)

            """Obtêm o CNPJ do Prestador do Serviço"""
            sql = "select t.id, t.nome, t.tag, t.tag_pai, t.id_tipo from rfe_tags t where t.nome = 'PrestadorCNPJ'"
            PrestadorCNPJ = cb.PesquisarValorTag(root, sql)

            """Obtêm Número da Nota Fiscal de Serviço"""
            sql = """select t.id, t.nome, t.tag, t.tag_pai, t.id_tipo
                                          from rfe_tags t
                                          where t.nome = 'NuNFSe'"""
            NuNFSe = cb.PesquisarValorTag(root, sql)

            """Insere Dados no DataFrame"""
            dfNFSe.loc[len(dfNFSe)]=[item,CodigoMunicipio,Municipio,PrestadorCNPJ,NuNFSe]

        """Preenche a TableView"""
        self.carrega_tableview(dfNFSe)

    # Rotina principal de tratamento de dados
    def processar(self):
        """Executa Processamento Escolhido"""
        if self.rb_layout.isChecked():
            self.processar_layout()
        else:
            self.processar_dados()

    # Salva o resultado do processamento
    def save_data(self):
        """Obtêm o DataFrame dos Dados Processados"""
        if self.tbvExtratacao.model() is not None:
            dfProcess = self.tbvExtratacao.model()._data

            """Define o nome do arquivo pelo tipo de processamento"""
            file_name = ''
            if self.rb_layout.isChecked():
                """Forma nome do arquivo para Layout Processado"""
                municipio = ''
                if 'municipio' in dfProcess.columns: # Testa se a coluna 'municipio' existe no dataframe
                    municipio = dfProcess.loc[:,'municipio'].drop_duplicates().dropna().iloc[0]
                else:
                    municipio = 'Padrão'

                """Sempre formar nome de arquivo"""
                file_name = self.cria_nome_arq(municipio)
            else:
                """Forma nome do arquivo para Dados do(s) XML(s) Processado(s)"""
                file_name = self.cria_nome_arq('DadosNFSe')

            path_file = qtw.QFileDialog.getSaveFileName(self, 'Save File', file_name, ".txt(*.txt)")

            """Salva o resultado do processamento"""
            if path_file[0] != '':
                dfProcess.drop_duplicates().to_csv(path_file[0], encoding='latin-1', sep = ';', index = False)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
