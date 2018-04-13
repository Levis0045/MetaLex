#! usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

"""MetaLex is general tool for lexicographic and metalexicographic activities

Copyright (C) 2017  by Elvis MBONING

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: levismboning@yahoo.fr

---------------------------------------------------------------------------

Give extra functions for parser of dictionary and XML/HTML generator

Usage:
    >>> from metalex.dicXmilised import *
    >>> generateID()
"""

# ----Internal Modules------------------------------------------------------

import metalex
from .composeArticle import *

# ----External Modules------------------------------------------------------

import re
import sys
import codecs
import os
from random import sample
from lxml import etree
from bs4 import BeautifulSoup

# -----Exported Functions---------------------------------------------------

__all__ = ['generate_id', 'get_data_articles', 'MetalexGenerateXml', 'de_specialised',
           'article_type_form']

# -----Global Variables-----------------------------------------------------

codi = metalex.codifications.CodificationsStore()
contentDic = codi.get_all_codifications()

# --------------------------------------------------------------------------

    
def generate_id():
    """Generate ID of 5 characters with alpha numeric characters 
    
    :return str: id generated
    """
    idart = sample(['1','2','3','4','5','6','7','8','9','0','a'
                    ,'b','c','d','e','f','g','h','i','j','k','l','m'
                    ,'n','o','p','q','r','s','t','v','w','y','z'], k=5)
    return ''.join(idart)


def article_type_form(art):
    """Find type form of article depending on their codification  
    
    :param art: str 
    
    :return str: int of type found
    """
    soup = BeautifulSoup(art, 'html.parser')
    try: 
        if re.search(r'<cte_cat>', unicode(soup.contents[1])):
            if re.search(r'<cte_gender>', unicode(soup.contents[3])):
                if re.search(r'<cte_rection>', unicode(soup.contents[5])):
                    #print ('***gender*** '+art+'*****')
                    return '7' #cat, gender and rection
                else: return '2' #cat and gender
            elif re.search(r'<cte_rection>', unicode(soup.contents[3])):
                #print ('***rection*** '+art+'*****')
                return '4' #cat and rection
            else: 
                #print ('***cat*** '+art+'*****')
                return '1' #cat
                
        elif re.search(r'<cgr_vrg>', unicode(soup.contents[1])): 
            if re.search(r'<cgr_vrg>', unicode(soup.contents[3])): 
                #print('***cat*** '+art+'*****')
                return '3' #vrg, vrg and cat
            else: 
                #print('***cat*** '+art+'*****')
                return '8' #vrg and cat
                
        elif re.search(r'<cgr_ocrh>', unicode(soup.contents[1])): 
            if re.search(r'<cte_gender>', unicode(soup.contents[7])):
                #print('***cat*** '+art+'*****')
                return '6' #crh, crh, cat and gender
            else: return '5' #crh, crh, cat and rection
        else: 
            #print ('***cat*** '+art+'*****\n')
            return '9' #Problematic case
            
    except IndexError: pass
    
        
def get_data_articles(typ):
    """Get data article from the store data file depending of the type wanted   
    
    :return dic: datapickle or datatext
    """
    metalex.utils.create_temp()
    filepickle, filetext = '', ''
    for fil in os.listdir('.'):
        if fil.endswith('.pickle'): filepickle = fil 
        elif fil.endswith('.art'): filetext = fil
    if typ == 'pickle': return metalex.utils.file_unpickle(filepickle)
    if typ == 'text': return metalex.utils.file_get_text(filetext)


def de_specialised(strng):
    if strng.find(')'): return strng.replace(')', '\)')
    if strng.find('.'): return strng.replace('.', '\.')


class MetalexGenerateXml():
    """Generate XML file   
    
    :return xml: xml file
    """
    
    def trans(self, ruleEl, nsmap=None):
        attribs, el = '', ''
        if re.search(r'{', ruleEl): 
            partel  = re.split(r'{', ruleEl.strip()) 
            el      = partel[0].strip()
            if re.search(r',', partel[1]):
                attribs = re.split(r',', partel[1][:-1])
            else: attribs = partel[1].strip()
            elEtree = etree.Element(el, nsmap=None)
            for attrib in attribs:
                attr, val = re.split(r':', attrib.strip())
                elEtree.set(attr, val)
            return elEtree
        else:
            elEtree = etree.Element(ruleEl.strip(), nsmap=None)
            return elEtree
    
    def next_sect(self, nextS, m2, m1):
        nexts = nextS
        if re.search(r'-', nexts):
            nodes = re.split(r'-', nexts())
            for node in nodes:
                if node == nodes[-1]:
                    m2.append(self.trans(node))
                    m1.append(m2)
                    m3 = self.trans(node)
                    try:
                        nextCh = nexts.next()
                        self.nextSect(nextCh, m3, m2)
                    except StopIteration:
                        print(etree.tostring(m1, pretty_print=True))
                        break
                else: m2.append(self.trans(node))
        else: 
            m2.append(self.trans(nexts))
            m1.append(m2)
                      
    def make_rule_html_xml(self, datarule, typ='xml'):
        elements = re.split(r'->', datarule)
        master   = self.trans(elements[0])
        lenchild = elements[1:]
        childs   = iter(elements[1:])
        if lenchild > 2:
            i = 1
            while i < lenchild:
                try:
                    childsnext = childs.next()
                    if re.search(r'-', childsnext):
                        nodes = re.split(r'-', childsnext)
                        for node in nodes:
                            if node == nodes[-1]:
                                master.append(self.trans(node))
                                master2 = self.trans(node)
                                try:
                                    nextCh = childs.next()
                                    self.nextSect(nextCh, master2, master)
                                except StopIteration:
                                    print(etree.tostring(master, pretty_print=True))
                                    break
                            else:master.append(self.trans(node))           
                    else: master.append(self.trans(childsnext))
                    i += 1
                except StopIteration:
                    print(etree.tostring(master, pretty_print=True))
                    break
            
    
    
    
    
        