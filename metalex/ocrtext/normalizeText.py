#! usr/bin/env python
# coding: utf8

"""
    metalex is general tool for lexicographic and metalexicographic activities
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
    
    Contact : levismboning@yahoo.fr
    
    ---------------------------------------------------------------------------
    
    Implémentation des outils de normalization du texte des articles.
    
    Packages:
        >>> apt-get install python-html5lib
        >>> apt-get install python-lxml
        >>> apt-get install python-bs4
    
    Usage:
        >>> from metalex.dicOcrText import *
        >>> makeTextWell('dico_rules_larousse.dic')
    
"""

# ----Internal Modules------------------------------------------------------

import metalex
from metalex import xmlised as Xml
from metalex import codifications

# ----External Modules------------------------------------------------------

import re
import sys
import codecs
import os
import time
import warnings
from bs4 import BeautifulSoup
from termcolor import colored
from multiprocessing import Pool

# -----Exported Functions---------------------------------------------------

__all__ = ['BuildTextWell', 'FileRule']

# -----Global Variables-----------------------------------------------------

AllWords    = []
namepickle  = ''
nametxt     = ''

# ----------------------------------------------------------
    
class BuildTextWell():
    """Extract and normalize all text data from HTML files 
    
    :param file_rules: file containing dictionary rules
    :param okCorrect: bool
    :param log: bool
    
    :return array: list of path of 
    """
    
    def __init__(self, file_rules, okCorrect=False, log=False):
        self.okCorrect = okCorrect
        self.log = log
        self.file_rules = file_rules
        print  u'\n --- %s ---------------------------------------------------------- \n\n' %colored('Part 3 : Correct OCR data', attrs=['bold'])
        debut = time.time()
        filerule = FileRule(self.file_rules, typ=u'rule_wc')
        self.data_rules = filerule.file_rule_unpack()
        dfilerule = time.time() - debut
        if self.log : print "--> %30s : %10.5f seconds\n" %("Durée d'extraction du fichier des règles", dfilerule)
         

    def extract_correct(self, html):
        """Composed and saved all treatment processes to enhance quality of HTML articles 
        
        :param html: str HTML file
        
        :return dicArticles: add corrected file in dicArticles
        """
        with open(html, 'r') as html_file :
            enhance_text(html_file, self.data_rules, self.okCorrect)  

    
    def calculate_process(self):
        """Calculate a number of processes usefull for OCR processing
    
        :return int: number of processes
        """
        processExec = 0
        lenHtmlOcrFiles = len(metalex.resultOcrFiles)
        if lenHtmlOcrFiles == 1: 
            processExec = 1
        elif lenHtmlOcrFiles == 2:
            processExec = 2
        elif lenHtmlOcrFiles > 2 and lenHtmlOcrFiles < 10 :
            processExec = 3
        elif lenHtmlOcrFiles > 10 :
            processExec = 5
        return processExec
    
    
    def make_text_well(self):
        """Run simultanously all html files processes to extract data articles
    
        :return file: pickle object and texte data
        """
        html_ocr_files = metalex.resultOcrFiles
        processOcr = Pool(self.calculate_process())
        if len(html_ocr_files) >= 1 :
            processOcr.map(self, html_ocr_files)
        else :
            message = u'OCR  >> We are not found any OCR files to enhance text quality'
            messageExit = u'FATAL ERROR! We cannot continue, resolve the previous error'
            metalex.logs.manageLog.write_log(message, typ='error')
            return sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))

        namepickle = metalex.project.name_file(html_ocr_files, u'.pickle')
        nametxt = metalex.project.name_file(html_ocr_files, u'.art')
        
        metalex.project.save_normalized_data(name=namepickle, typ=u'pickle', form=u'norm')
        metalex.project.save_normalized_data(name=nametxt, typ=u'text', form=u'norm')
        
        metalex.project.create_temp()  
        os.remove('temp_norm.txt')
    
    def __call__(self, html):
        return self.extract_correct(html)
    
    
def enhance_text(html_file, rules, okCorrect):
    """Enhance quality of text by remove all inconvenients characters and optionally 
       correct malformed words.
    
    :param html_file: str file
    :param rules: str
    :param okCorrect: Bool
    
    :return list: dicArticles
    """
    soup = BeautifulSoup(html_file, "html5lib")
    div = soup.find(u'div', attrs={u'class': u'ocr_page'}) 
    art = 1
        
    for div in div.findAll(u'div', attrs={u'class': u'ocr_carea'}) :
        for para in div.findAll(u'p', attrs={u'class': u'ocr_par'}) :
            contentOrigin = u''
            contentCorrection = u''
            if not re.search(ur'(@|>|ÊË|{/)', para.get_text().strip()) and not re.search(ur'(^\d)', para.get_text().strip()):
                for span in para.stripped_strings:
                    if span[-1] == u'—' or span[-1] == u'-' or span[-1] == u'— ' or span[-1] == u'- ':
                        span = span[:-1]
                        AllWords.append(span)
                        if okCorrect :
                            spanCorrect = metalex.correct_word(span)
                            contentCorrection += spanCorrect
                        else :
                            contentOrigin += span
                        #print '*****  '+span + ' : ' + spanCorrect
                    elif metalex.word_replace(span, rules[1], test=True) :
                        spanR = metalex.word_replace(span, rules[1])
                        if okCorrect :
                            spanCorrect = metalex.correct_word(spanR)
                            contentCorrection += spanCorrect+u' '
                        else :
                            contentOrigin += spanR+u' '
                        #print '*****  '+span + ' : ' + spanR
                    elif metalex.caract_replace(span, rules[2], test=True):
                        spanR = metalex.caract_replace(span, rules[2])
                        AllWords.append(spanR)
                        if okCorrect :
                            spanCorrect = metalex.correct_word(spanR)
                            contentCorrection += spanCorrect+u' '
                        else:
                            contentOrigin += spanR+u' '
                        #print '*****  '+span + ' : ' + spanR
                    else:
                        if okCorrect :
                            AllWords.append(span)
                            spanCorrect = metalex.correct_word(span)
                            contentCorrection += spanCorrect+u' '
                        else :
                            AllWords.append(span)
                            contentOrigin += span+u' '
                    #print '*****  '+span + ' : ' + spanCorrect
            else :
                pass
            
            #print contentOrigin+'\n'
            artnum = u'article_'+str(art)
            crtnum = u'correction_'+str(art)
            if len(contentOrigin) >= 15 and len(contentCorrection) == 0:
                article = u'%s==%s' %(artnum, contentOrigin)
                metalex.project.write_temp_file(article, 'norm')
                art += 1
            elif len(contentOrigin) >= 15 and len(contentCorrection) >= 5 :
                article = u'%s==%s | %s==%s' %(crtnum, contentCorrection, artnum, contentOrigin)
                metalex.project.write_temp_file(article, 'norm')
                art += 1
                
    formFile = str(html_file).split('/')[-1].split("'")[0]
    message = u"enhance_text() >> *"+formFile+u"* has been extracted and corrected"
    metalex.logs.manageLog.write_log(message) 
        
        
class FileRule():
    """Managing of input file rules for text normalization
    
    :param file_rule: str file
    :param typ: str
    
    :return obj: FileRule instanciation
    """
    
    def __init__(self, file_rule, typ):
        self.file = file_rule
        self.typ = typ
         
    def file_rule_unpack(self):
        """Unpack file rule and extract its contents
        
        :param self: class object
        
        :return dict: metadata, ruleWords, ruleCaracts, ruleRegex
        """
        word, caracter, regex = u'\W', u'\C', u'\R'
        metadata, ruleWords, ruleCaracts, ruleRegex = {}, {}, {}, {}
        startw, startc, startr = False, False, False
        
        if self.file_rule_verified(self.typ) :
            if self.typ == u'rule_wc' :
                with codecs.open(self.file, 'r', 'utf-8') as rule :
                    for line in rule : 
                        line = line.strip()
                        if line.startswith(u'\metalex') : 
                            names = (u'tool', u'project', u'theme', u'lang', u'admin', u'date')
                            for name, cnt in zip(names, line.split(u'\\')[1:]) :
                                metadata[name] = cnt
                        if line == word : startw, startc, startr = True, False, False
                        if line == caracter : startw, startc, startr = False, True, False
                        if line == regex : startw, startc, startr = False, False, True
                        if startw :
                            linepart = line.split(u'/')
                            if len(linepart) == 3 : ruleWords[linepart[1]] = linepart[2]
                        if startc :
                            linepart = line.split(u'/')
                            if len(linepart) == 3 : ruleCaracts[linepart[1]] = linepart[2]
                        if startr :
                            linepart = line.split(u'/')
                            if len(linepart) == 3 : ruleRegex[linepart[1]] = linepart[2]
            if self.typ == u'rule_art' :
                return False
        else :
            log = u"file_rule_unpack() >> Your file rule syntax is not correct. Please correct it as recommended"
            metalex.logs.manageLog.write_log(log, typ='warm')
            
        return metadata, ruleWords, ruleCaracts, ruleRegex 
        
    
    def file_rule_verified(self, typ):
        """Verified if file rule content respect the norm description of metalex 
        
        :param typ: str
        
        :return Bool: True|Fase
        """
        module, synw, sync, synr, synrw, delimiter = (False for x in range(6))
        try :
            fileop = codecs.open(self.file, 'r', 'utf-8').readlines()
        except :
            log = u"file_rule_verified() >> We can't open your file rule. Please set it !"
            return metalex.logs.manageLog.write_log(log, typ='error')
        
        if typ == u'rule_wc' :
            if u'\START' == fileop[0].strip() and u'\END' == fileop[-1].strip() : delimiter = True
            if len(fileop[1].strip().split(u'\\')) == 7 :
                for el in fileop[1].strip().split(u'\\') :
                    if el == u'metalex': module = True
            for lg in fileop:
                lg = lg.strip()
                if lg == u'\W' : synw = True
                if lg == u'\C' : sync = True
                if lg == u'\R' : synr = True
                if lg[0] == u'/' : 
                    if len(lg.split(u'/')) == 3 : synrw = True
            if sync and synw and synr and module and delimiter and synrw :
                return True
            else :
                return False
            
        if typ == u'rule_art' :
            return False



