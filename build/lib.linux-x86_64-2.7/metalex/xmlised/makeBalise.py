#! usr/bin/env python
# coding: utf8

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

"""metalex is general tool for lexicographic and metalexicographic activities

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

makeBalise transform extracted articles into  well formed xml file.
It can also generate HTML file for article edition

Packages:
    >>> sudo apt-get install python-html5lib
    >>> sudo apt-get install python-lxml
    >>> sudo apt-get install python-bs4

Usage:
    >>> from metalex.dicXmilised import *
    >>> dicoHtml(save=True)
    
"""

# ----Internal Modules------------------------------------------------------

import metalex
from .composeArticle import *
from .dicXmlTool import *

# ----External Modules------------------------------------------------------

import re
import sys
import codecs
import os
from bs4 import BeautifulSoup
from random import sample
from shutil import copyfile
from lxml import etree
from termcolor import colored

# -----Exported Functions-----------------------------------------------------

__all__ = ['BaliseXML', 'dico_html']

# -----Global Variables-----------------------------------------------------

components = {
    'xml' :   {
                'metalexMetadata' : ['metalexMetadata', 'projectName', 'author', 
                                     'dateCreation', 'comment', 'contributors', 'candidate'],
                'metalexContent'  : ['article', 'definition', 'example', 'figured', 'contrary',
                                     'entry', 'flexion', 'category', 'gender', 'rection', 'phonetic',
                                     'identificationComponent', 'treatmentComponent', 'cte_cat', 
                                     'processingUnit', 'cgr_pt', 'cgr_vrg', 'cgr_fpar', 'cgr_opar',
                                     'cgr_ocrch', 'cgr_fcrch', 'metalexContent', 'cte_gender',
                                     'metalexResultDictionary']
              },
    'tei' :   {
                'teiHeader' : ['teiHeader', 'text', 'TEI', 'fileDesc', 'titleStmt', 
                               'title', 'publicationStmt', 'p', 'sourceDesc', 'author'],
                'text'      : ['body', 'head', 'entry', 'form', 'orth', 'gramGrp',
                                'sense', 'def', 'cite', 'quote', 'span', 'usg', 'bibl', 
                                'pos', 'genre', 'number', 'pron', 'etym']
              },
    'lmf' :   {
                'GlobalInformation' : ['LexicalResource', 'feat', 'p', 'GlobalInformation'],
                'Lexicon'           : ['Lexicon', 'feat', 'LexicalEntry', 'WordForm', 
                                       'Definition', 'Sense', 'Lexicon']
               },
    'dtd' :   ['ELEMENT', 'ATTRIBUTE', 'PCDATA', 'CDATA', 'REQUIRED', 'IMPLIED'],
    'xsd' :   []
}

codifArticles   = []

# ----------------------------------------------------------

def dico_html(save=False):
    """Build HTML editor file of the all articles 
    
    :return file: metalexViewerEditor.html
    """
    print('\n --- %s %s \n\n' %(colored('Part 4: Generate Output formats', attrs=['bold']), '--'*25))
    
    metalex.plugins
    instanceHtml = BaliseHTML()
    filepath     = metalex.html_template
    metalex.utils.create_temp()
    if metalex.utils.in_dir('CopymetalexTemplate.html'):
        copyfile(filepath, 'CopymetalexTemplate.html')
        souphtl = instanceHtml.html_inject('CopymetalexTemplate.html')
        if save:
            metalex.utils.go_to_dicresult()
            name = metalex.currentOcr+'_metalexViewerEditor.html'
            with codecs.open(name, 'w') as htmlresult:
                htmlresult.write(souphtl)
            metalex.utils.create_temp()
            os.remove('CopymetalexTemplate.html')
            message = "*"+name+"* has correctly been generated > Saved in dicTemp folder" 
            metalex.logs.manageLog.write_log(message)
    else:
        souphtl = instanceHtml.html_inject('CopymetalexTemplate.html')
        if save:
            metalex.utils.go_to_dicresult()
            with codecs.open(name, 'w') as htmlresult:
                htmlresult.write(souphtl)
            metalex.utils.create_temp()
            os.remove('CopymetalexTemplate.html')
            message = "*"+name+"* has correctly been generated > Saved in dicTemp folder" 
            metalex.logs.manageLog.write_log(message)
    
    print('\n\n --- %s --------------- \n\n' %colored('MetaLex Processes was ended: consult results data in "dicTemp" folder',
                                                      'green', attrs=['bold']))
      
 
class BaliseHTML():
    
    def __init__(self):
        self.resultHtml = ''
        
    def html_inject(self, template):
        """Create prettify HTML file all previous data generated 
        
       :return str: html (prettify by BeautifulSoup)
        """
        instanceXml    = BaliseXML()
        contentxml     = instanceXml.put_xml(typ='xml', save=True)
        metalex.utils.create_temp()
        soupXml        = BeautifulSoup(contentxml, "html.parser")
        projectconf    = metalex.utils.read_conf()
        Hauthor, Hname = projectconf['Author'], projectconf['Projectname'],
        Hdate,Hcomment = projectconf['Creationdate'], projectconf['Comment']
        Hcontrib       = projectconf['Contributors']
        filetemplate   = codecs.open(template, 'r', 'utf-8')
        souphtml       = BeautifulSoup(filetemplate, "html5lib")
        content        = souphtml.find('div', attrs={'id': 'all-articles'}) 
        author         = content.find('h3', attrs={'id': 'author'})
        author.string  = 'main: '+Hauthor
        date           = content.find('h5', attrs={'id': 'date'})
        date.string    = Hdate
        descipt        = content.find('p', attrs={'id': 'description'})
        descipt.string = Hcomment
        contrib        = content.find('h4', attrs={'id': 'contributors'})
        contrib.string = 'contributors: '+Hcontrib
        project        = content.find('h4', attrs={'id': 'projetname'})
        project.string = Hname
        articlesxml    = soupXml.findAll('article')
        articleshtml   = souphtml.find('div', attrs={'id': 'mtl:articles'})
        for x in articlesxml: 
            elementart = BeautifulSoup('<article id=""></article>', 'html5lib')
            idart   = x.get('id')
            artlem  = x.get_text()
            elementart.article.append(artlem)
            elementart.article['id'] = idart
            articleshtml.append(elementart.find('article'))  
        listlemme   = souphtml.find('ul', attrs={'id': 'list-articles'})
        for x in articlesxml:
            art     = x.get_text()
            idart   = x.get('id')
            lem     = x.find('entry').get_text()
            lemme   = BeautifulSoup('<li class="w3-hover-light-grey"><span class="lemme" onclick="changeImage('+
                                    "'"+idart+"'"+')">'+lem+'</span><span class="fa fa-plus w3-closebtn" onclick="add('+
                                    "'"+idart+"'"+')"/></li>', 'html5lib')
            listlemme.append(lemme.find('li'))
            
        filetemplate.close()
        self.resultHtml = souphtml.prettify('utf-8')
        return self.resultHtml
    
     

class BaliseXML ():
    """Build XML file type (xml|tei|lmf) with global metadata of the project
    
   :param typ: str 
  
   :return obj: instance of BaliseXML
    """
    
    def __init__(self, typ="xml"):
        self.typ = typ
        
    def build_structure(self, data, Sfile=None, typ='dtd'):
        return False
    
    def message(self, name):
        return  "*"+name+"*  dictionary articles formated in xml is"+\
            " created > Saved in dicTemp folder"
    
    def put_xml(self, typ='xml', save=False):
        """Create well formed (xml|tei|lmf) file with metadata and content xml 
        
       :return metalexXml
        """
        metadata = self.xml_metadata(typ)
        content  = self.xml_content(typ)
        metalex.utils.go_to_dicresult()
        if typ == 'xml':
            if save:
                name = 'metalex-'+metalex.projectName+'_'+metalex.currentOcr+'.xml'
                metalexXml = self.balise(metadata+content, 'metalexResultDictionary', 
                                         attr={'xmlns':'https://www.w3schools.com', 
                                               'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-in', 
                                               'xsi:schemaLocation':'metalexSchemaXML.xsd'})
                metalexXml = '<?xml version="1.0" encoding="UTF-8" ?>'+metalexXml
                metalexXmlTree = BeautifulSoup(metalexXml, 'xml')
                
                if metalex.utils.in_dir(name):
                    with codecs.open(name, 'w', 'utf-8') as fle:
                        fle.write(metalexXmlTree.prettify(formatter=None))
                    mge = self.message(name)
                    metalex.logs.manageLog.write_log(mge)
                else:
                    mge = self.message(name)
                    metalex.logs.manageLog.write_log(mge)
                return metalexXml
            else:
                metalexXml = self.balise(metadata+content, 'metalexResultDictionary', attr={})
                metalexXml = '<?xml version="1.0" encoding="UTF-8" ?>'+metalexXml
                metalexXmlTree = BeautifulSoup(metalexXml, 'xml')
                print(metalexXmlTree.prettify(formatter=None))
        if typ == 'tei':
            if save:
                name = 'metalex-'+metalex.projectName+'_'+metalex.currentOcr+'-TEI.xml'
                metalexXml = self.balise(metadata+content, 'TEI', typ= 'tei')
                metalexXml = '<?xml version="1.0" encoding="UTF-8" ?>'+metalexXml
                metalexXmlTree = BeautifulSoup(metalexXml, 'xml')
                if metalex.utils.in_dir(name):
                    with codecs.open(name, 'w', 'utf-8') as fle:
                        fle.write(metalexXmlTree.prettify(formatter=None))
                    mge = self.message(name)
                    metalex.logs.manageLog.write_log(mge)
                else:
                    mge = self.message(name)
                    metalex.logs.manageLog.write_log(mge)
                return metalexXml
            else:
                metalexXml = self.balise(metadata+content, 'TEI', typ= 'tei')
                metalexXml = '<?xml version="1.0" encoding="UTF-8" ?>'+metalexXml
                metalexXmlTree = BeautifulSoup(metalexXml, 'xml')
                print(metalexXmlTree.prettify(formatter=None))
        if typ == 'lmf':
            os.listdir('.')
            if save:
                name = 'metalex-'+metalex.projectName+'_'+metalex.currentOcr+'-LMF.xml'
                metalexXml = self.balise(metadata+content, 'LexicalResource', attr={'dtdVersion':'15'}, typ= 'lmf')
                metalexXml = '<?xml version="1.0" encoding="UTF-8" ?>'+metalexXml
                metalexXmlTree = BeautifulSoup(metalexXml, 'xml')
                if metalex.utils.in_dir(name):
                    with codecs.open(name, 'w', 'utf-8') as fle:
                        fle.write(metalexXmlTree.prettify(formatter=None))
                    mge = self.message(name)
                    metalex.logs.manageLog.write_log(mge)
                else:
                    mge = self.message(name)
                    metalex.logs.manageLog.write_log(mge)
                return metalexXml
            else:
                metalexXml = self.balise(metadata+content, 'LexicalResource', attr={'dtdVersion':'15'}, typ= 'lmf')
                metalexXml = '<?xml version="1.0" encoding="UTF-8" ?>'+metalexXml
                metalexXmlTree = BeautifulSoup(metalexXml, 'xml')
                print(metalexXmlTree.prettify(formatter=None))

    def xml_metadata(self, typ='xml'):
        """Create xml metadata file with configuration of the project 
        
       :return str: metadata
        """
        metalex.utils.create_temp()
        
        projectconf = metalex.utils.read_conf()
        contribtab  = projectconf['Contributors'].split(',') \
        if projectconf['Contributors'].find(',') else projectconf['Contributors']
        contrib = ''
        if typ == 'xml':
            author  = self.balise(projectconf['Author'], 'author', typ)
            name    = self.balise(projectconf['Projectname'].strip(), 'projectName', typ)
            date    = self.balise(projectconf['Creationdate'].strip(), 'dateCreation', typ)
            comment = self.balise(projectconf['Comment'], 'comment', typ)
            if len(contribtab) > 1:
                for data in contribtab: contrib += self.balise(data.strip(), 'candidate', typ) 
            else: contrib = self.balise(''.join(contribtab), 'candidate', typ)
            contrib     = self.balise(contrib, 'contributors', typ)
            cont        = name+author+date+comment+contrib
            
            metadataxml = self.balise(cont, 'metalexMetadata', typ) 
            return metadataxml
        if typ == 'tei':
            if len(contribtab) > 1:
                for data in contribtab: 
                    if len(data) > 2: contrib += self.balise(data.strip(), 'span', 
                                                             attr={'content':'contributor'}, typ='tei') 
            else: contrib = self.balise(''.join(contribtab), 'span', typ='tei')
            author      = self.balise(projectconf['Author'], 'author', typ='tei')
            title       = self.balise(projectconf['Projectname'], 'title', typ='tei')
            RtitleStmt  = self.balise(title, 'titleStmt', typ='tei')
            pdate       = self.balise(projectconf['Creationdate'], 'p', typ='tei')
            pcomment    = self.balise(projectconf['Comment'], 'p', typ='tei')
            pcontrib    = self.balise(contrib, 'p', attr={'content':'contributors'}, typ='tei')
            Rpubli      = self.balise(author+pdate+pcomment+pcontrib, 'publicationStmt', typ='tei')
            sourc       = self.balise('TEI metadata for metalex project output', 'p', typ='tei')
            Rsourc      = self.balise(sourc, 'sourceDesc', typ='tei')
            RfilD       = self.balise(RtitleStmt+Rpubli+Rsourc, 'fileDesc', typ='tei')
            metadatatei = self.balise(RfilD, 'teiHeader', typ='tei')
            return metadatatei
        if typ == 'lmf':
            if len(contribtab) > 1:
                for data in contribtab: 
                    if len(data) > 2: contrib += data.strip()+', '
            else: contrib = ', '.join(contribtab)
            enc      = self.balise('', 'feat', attr={'att':'languageCoding', 'val':'utf-8'}, 
                                      typ='lmf', sclose=True)
            pauthor  = self.balise('', 'feat', attr={'att':'author', 'val':projectconf['Author'].strip()}, 
                                      typ='lmf', sclose=True)
            pdate    = self.balise('', 'feat', attr={'att':'dateCreation', 'val':projectconf['Creationdate'].strip()},
                                       typ='lmf', sclose=True)
            pname    = self.balise('', 'feat', attr={'att':'projectName', 'val':projectconf['Projectname'].strip()},
                                       typ='lmf', sclose=True)
            pcomment = self.balise('', 'feat', attr={'att':'comment', 'val':projectconf['Comment'].strip()},
                                       typ='lmf', sclose=True)
            pcontrib = self.balise('', 'feat', attr={'att':'contributors', 'val':contrib.strip(', ')}, 
                                      typ='lmf', sclose=True)
            meta     = self.balise('', 'p', attr={'att':'meta', 'val':'TEI metadata for metalex project output'}, 
                                      typ='lmf', sclose=True)
            metadatalmf = self.balise(enc+pauthor+pname+meta+pdate+pcomment+pcontrib, 'GlobalInformation', typ='lmf')
            return metadatalmf
                    
    def balise_content_article (self):
        data = get_data_articles('text')
        cod  = StructuredWithCodif(data, 'xml')
        resultArticles = []
        for art in  cod.format_articles():
            article_type_form(art)
            if article_type_form(art) == '1':
                partArt = re.search(r'(([a-zéèàûô]+)\s(<cte_cat>.+</cte_cat>)\s(.+)<cgr_pt>\.</cgr_pt>)', art, re.I)
                if partArt != None:
                    ident, entry, cat, treat = partArt.group(1), partArt.group(2), partArt.group(3), partArt.group(4)
                    id    = generate_id()
                    entry = self.balise(entry, 'entry')
                    ident = self.balise(entry+cat, 'identificationComponent')
                    treat = self.balise(self.balise(treat, 'definition'), 'processingUnit')
                    article = self.balise(ident+self.balise(treat, 'treatmentComponent'), 'article', attr={'id':id})
                    resultArticles.append(article)     
            if article_type_form(art) == '2':
                research = r'(([a-zéèàûô]+)\s(<cte_cat>.+</cte_cat>\s<cte_gender>..</cte_gender>)\s(.+)<cgr_pt>\.</cgr_pt>)'
                partArt = re.search(research, art, re.I)
                if partArt != None:
                    ident, entry, cat, treat = partArt.group(1), partArt.group(2), partArt.group(3), partArt.group(4)
                    id    = generate_id()
                    entry = self.balise(entry, 'entry')
                    ident = self.balise(entry+cat, 'identificationComponent')
                    if not re.search(r'(<cgr_pt>\.</cgr_pt>|<cte_cat>.+</cte_cat>|<cgr_vrg>,</cgr_vrg>)', partArt.group(4), re.I):
                        treat = self.balise(self.balise(treat+'.', 'definition'), 'processingUnit')
                        article = self.balise(ident+self.balise(treat, 'treatmentComponent'), 'article', attr={'id':id})
                        resultArticles.append(article)
                    elif partArt.group(4).find(' et ') != -1:
                        suite = 'hahaha'
        
        return resultArticles
                      
    def xml_content(self, typ='xml', forme='text'): 
        """Create xml content file (representing articles) with data articles extracting
        
       :return str: contentXml
        """
        content     = ''
        contentXml  = ''
        data = self.balise_content_article()
        if typ == 'xml':
            if forme == 'pickle': 
                data = get_data_articles('pickle')
                for dicart in data:
                    for art in dicart.keys():
                        art = self.balise(dicart[art], 'article', art=True)
                        content += art
                contentXml = self.balise(content, 'metalexContent')
                return contentXml
            else: 
                for art in data: content += art
                contentXml = self.balise(content, 'metalexContent', attr={'totalArticle': str(len(data))})
                return contentXml
        
        if typ == 'tei':
            for art in data:
                soupart = BeautifulSoup(art, 'html.parser')
                orth    = soupart.find('entry').getText()
                atOrth  = soupart.find('article').get('id')
                orth    = self.balise(orth, 'orth', {'id': atOrth}, typ='tei')
                formB   = self.balise(orth, 'form', attr={'xml:lang':'fr', 'type':'lemma'}, typ='tei')
                pos     = soupart.find('cte_cat').getText()
                posB    = self.balise(pos, 'pos', typ='tei')
                genB    = ''
                if soupart.find('cte_gender'): genB = soupart.find('cte_gender').getText().strip()
                if genB == 'f.' or genB == 'm.': genB = self.balise(genB, 'genre', typ='tei')
                gramgrp = self.balise(posB+genB, 'gramGrp', typ='tei')
                sens    = soupart.find('processingunit').getText().replace(' .', '.')
                defi    = self.balise(sens, 'def', typ='tei')
                if sens != None: sens  = self.balise(defi, 'sense', typ='tei')
                entry   = self.balise(formB+gramgrp+sens, 'entry', typ='tei')
                content += entry
            body  = self.balise(content, 'body', typ='tei')
            contentXml   = self.balise(body, 'text', attr={'totalArticle': str(len(data))}, typ='tei')
            return contentXml
        
        if typ == 'lmf':
            for art in data:
                soupart = BeautifulSoup(art, 'html.parser')
                orth    = soupart.find('entry').getText()
                atOrth  = soupart.find('article').get('id')
                orth    = self.balise('', 'feat', attr={'att':'writtenForm','val':orth}, 
                                      typ='lmf', sclose=True)
                wordF   = self.balise(orth, 'WordForm', attr={'id': atOrth}, typ='lmf')
                pos     = soupart.find('cte_cat').getText()
                posB    = self.balise('', 'feat', attr={'att':'partOfSpeech','val':pos}, 
                                      typ='lmf', sclose=True)
                genB    = ''
                if soupart.find('cte_gender'): genB = soupart.find('cte_gender').getText().strip()
                if genB == 'f.' or genB == 'm.': 
                    genB = self.balise('', 'feat', attr={'att':'grammaticalNumber','val': genB}, 
                                       typ='lmf', sclose=True)
                sens    = soupart.find('processingunit').getText().replace(' .', '.')
                sensnb  = self.balise('', 'feat', attr={'att':'sensNumber','val':'1'}, 
                                      typ='lmf', sclose=True)
                definb  = self.balise('', 'feat', attr={'att':'text','val':sens.strip()}, 
                                      typ='lmf', sclose=True)
                defi    = self.balise(definb, 'Definition', typ='lmf')
                if sens != None: sens  = self.balise(sensnb+defi, 'Sense', typ='lmf')
                entry   = self.balise(wordF+posB+genB+sens, 'LexicalEntry', typ='lmf')
                content += entry
            body = self.balise('', 'feat', attr={'att':'language','val':'fra'}, 
                               typ='lmf', sclose=True)+content
            contentXml   = self.balise(body, 'Lexicon', attr={'totalArticle': str(len(data))}, typ='lmf')
            return contentXml
                  
    def balise(self, element, markup, sclose=False, attr=None, typ='xml', art=False):
        """Markup data with a specific format type (xml|tei|lmf)
        
       :return str: balised element
        """
        if typ == 'xml':
            if markup in components['xml']['metalexContent'] or markup \
            in components['xml']['metalexMetadata']:
                if art:
                    element = self.chevron(markup, attr, art=True)+element+self.chevron(markup, attr, False)
                    return element
                else:
                    element = self.chevron(markup, attr)+element+self.chevron(markup, attr, False)
                    return element
        if typ == 'tei':
            if markup in components['tei']['text']  or markup in components['tei']['teiHeader']:
                if art:
                    element = self.chevron(markup, attr, art=True)+element+self.chevron(markup, attr, False)
                    return element
                else:
                    element = self.chevron(markup, attr)+element+self.chevron(markup, attr, False)
                    return element
        if typ == 'lmf':
            if markup in components['lmf']['GlobalInformation'] \
            or components['lmf']['Lexicon']:
                if sclose:
                    element = self.chevron(markup, attr, True, sclose=True)
                    return element
                else: 
                    element = self.chevron(markup, attr)+element+self.chevron(markup, attr, False)
                    return element
                    
    def chevron(self, el, attr, openchev=True, art=False, sclose=False):
        """Put tag around the data of element
        
       :return str: tagging element 
        """
        idart = generate_id()
        if art and attr == None:
            if openchev    : return "<"+el+" id='"+idart+"' class='data-entry'"+">"
            if not openchev: return "</"+el+">"
            if sclose      : return "<"+el+" id='"+idart+"'/>"
        if art and attr != None:
            allattrib = ''
            for at in attr.keys():
                allattrib += ' '+at+'="'+attr[at]+'"'
            if openchev  and not sclose  : return "<"+el+" id='"+idart+"' class='data-entry'"+' '+allattrib+">"
            if openchev and sclose: return "<"+el+" id='"+idart+"' class='data-entry'"+' '+allattrib+"/>"
            if not openchev: return "</"+el+">"
        elif art == False and attr != None:
            #print openchev
            allattrib = ''
            for at in attr.keys(): allattrib += ' '+at+'="'+attr[at]+'"'
            if openchev  and not sclose: return "<"+el+' '+allattrib+">"
            if openchev and sclose: return "<"+el+' '+allattrib+"/>"
            if not openchev: return "</"+el+">"
        elif art == False and attr == None:
            if openchev    : return "<"+el+">"
            if sclose      : return "<"+el+"/>"
            if not openchev: return "</"+el+">"
        
        
        