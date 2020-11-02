# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 14:53:37 2020

@author: lindineu.duran
"""

import pandas as pd
import sqlite3

class ConsultaBanco:
    def __init__(self, connect_string):
        self.connect_string = connect_string

    def setConnectString(connect_string):
        self.connect_string = connect_string

    def getConnectString(self):
        return self.connect_string

    def finaliza_loop(self, valor):
        sair = False
        if valor != '':
            sair = True

            return sair

    def PesquisarValorTag(self, root, sql):
        # Conecta ao Banco de Dados
        conn = sqlite3.connect(self.connect_string)
        cursor = conn.cursor()

        valor = ""
        sair = False
        for row in cursor.execute(sql):
            if row[3] != "":
                for child in root.iter(row[3]):
                    for child1 in child.iter(row[2]):
                        # valor = child1.tag
                        valor = child1.text

                        sair = self.finaliza_loop(valor)
                        if sair:
                            break
                    if sair:
                            break
            else:
                for child in root.iter(row[2]):
                        # valor = child.tag
                        valor = child.text

                        sair = self.finaliza_loop(valor)
                        if sair:
                            break
            if sair:
                    break

        cursor.close()
        conn.close()

        return valor


    def PesquisaItem(self, sql):
        # Conecta ao Banco de Dados
        conn = sqlite3.connect(self.connect_string)
        cursor = conn.cursor()
        
        valor = ""
        for row in cursor.execute(sql):
            if row[0] != "":
                valor = row[0]

        cursor.close()
        conn.close()

        return valor

    def ObtemLayout(self,Municipio,CodigoMunicipio, root):
        # Conecta ao Banco de Dados
        conn = sqlite3.connect(self.connect_string)
        cursor = conn.cursor()

        # Configura DataFrame
        columns = ['nome', 'tag', 'tag_pai', 'municipio', 'cod_ibge']
        dfTagsLayout = pd.DataFrame(columns=columns)

        sql = """select t.nome, t.tag, t.tag_pai, t.id_tipo, x.descricao
                 from rfe_tags t, rfe_tipos_xml x
                 where t.tag <> ''
                   and t.id_tipo = x.id
                 order by t.id_tipo;"""

        sair = False
        for row in cursor.execute(sql):
            if row[2] != "":
                for child in root.iter(row[2]):
                    for child1 in child.iter(row[1]):
                        valor = child1.tag

                        dfTest = dfTagsLayout.query('tag=="'+row[1]+'"')

                        if dfTest.count().any() == 0:
                            dfTagsLayout.loc[len(dfTagsLayout)]=[row[0], row[1], row[2], Municipio, CodigoMunicipio]

                        sair = self.finaliza_loop(valor)
                        if sair:
                            break
                    if sair:
                            break
            else:
                for child in root.iter(row[1]):
                        valor = child.tag

                        dfTest = dfTagsLayout.query('tag=="'+row[1]+'"')

                        if dfTest.count().any() == 0:
                            dfTagsLayout.loc[len(dfTagsLayout)]=[row[0], row[1], row[2], Municipio, CodigoMunicipio]

                        sair = self.finaliza_loop(valor)
                        if sair:
                            break

        cursor.close()
        conn.close()

        return dfTagsLayout
