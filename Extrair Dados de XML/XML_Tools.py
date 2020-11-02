# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 16:41:23 2020

@author: lindineu.duran
"""
from lxml import etree, objectify

class XML_Tools:
    def intrepreta_xml(self, metadata):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(metadata, parser)
        root = tree.getroot()

        #### Elimina namespace ####
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'): continue  # (1)
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i+1:]
        objectify.deannotate(root, cleanup_namespaces=True)
        ####

        return root

    def obtem_tags(self, root, dfTags):
        filtro = "*"
        for child in root.iter(filtro):
            myTag = child.tag
            dfTags.loc[len(dfTags)]=[myTag]

        return dfTags
