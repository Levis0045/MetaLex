#! usr/bin/env python
# coding: utf8

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

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
    
    Contact: levismboning@yahoo.fr
    
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

# ----Internal Modules------------------------------------------------------

import metalex
from metalex import xmlised as Xml
from metalex import codifications

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
        print('\n --- %s %s \n\n' %(colored('Part 3: Correct OCR data', 
                                            attrs=['bold']), '--'*20))
        debut = time.time()
        filerule = FileRule(self.file_rules, typ='rule_wc')
        self.data_rules = filerule.file_rule_unpack()
        dfilerule = time.time() - debut
        if self.log: print("--> %30s: %10.5f seconds\n" 
                           %("Durée d'extraction du fichier des règles", dfilerule))
         

    def extract_correct(self, html):
        """Composed and saved all treatment processes to enhance quality of HTML articles 
        
        :param html: str HTML file
        
        :return dicArticles: add corrected file in dicArticles
        """
        with open(html, 'r') as html_file:
            enhance_text(html_file, self.data_rules, self.okCorrect)  
    
    
    def make_text_well(self):
        """Run simultaniously all html files processes to extract data articles
    
        :return file: pickle object and text data
        """
        html_ocr_files = metalex.resultOcrFiles
        processOcr = Pool(metalex.utils.calculate_process())
        if len(html_ocr_files) >= 1: processOcr.map(self, html_ocr_files)
        else:
            message = 'OCR  >> We are not found any OCR files to enhance text quality'
            messageExit = 'FATAL ERROR! We cannot continue, resolve the previous error'
            metalex.logs.manageLog.write_log(message, typ='error')
            return sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))

        namepickle = metalex.utils.name_file(html_ocr_files, '.pickle')
        nametxt = metalex.utils.name_file(html_ocr_files, '.art')
        
        metalex.utils.save_normalized_data(name=namepickle, typ='pickle', form='norm')
        metalex.utils.save_normalized_data(name=nametxt, typ='text', form='norm')
        
        metalex.utils.create_temp()
        os.remove('temp_norm.txt')
    
    def __call__(self, html):
        return self.extract_correct(html)
    
    
def enhance_text(html_file, rules, okCorrect):
    """Enhance quality of text by remove all inconvenients characters  
       and optionally correct malformed words.
    
    :param html_file: str file
    :param rules: str
    :param okCorrect: Bool
    
    :return list: dicArticles
    """
    soup = BeautifulSoup(html_file, "html5lib")
    div = soup.find('div', attrs={'class': 'ocr_page'}) 
    art, dataContent = 1, []
    
    if metalex.currentOcr == 'ocropy':
        for span in div.findAll('span', attrs={'class': 'ocr_line'}):
            dataContent.append(span)
    if metalex.currentOcr == 'tesserocr':
        for div in div.findAll('div', attrs={'class': 'ocr_carea'}):
            for para in div.findAll('p', attrs={'class': 'ocr_par'}):
                dataContent.append(para)       
                     
    spanCorrect = ''
    for para in dataContent:
        contentOrigin = ''
        contentCorrection = ''
        if not re.search(r'(@|>|ÊË|{/)', para.get_text().strip()) \
        and not re.search(r'(^\d)', para.get_text().strip()):
            for span in para.stripped_strings:
                if span[-1] == '—' or span[-1] == '-' or span[-1] == '— '\
                                    or span[-1] == '- ':
                    span = span[:-1]
                    AllWords.append(span)
                    if okCorrect:
                        spanCorrect = metalex.correct_word(span)
                        contentCorrection += spanCorrect
                    else: contentOrigin += span
                    #print('*****  '+span + ': ' + spanCorrect)
                elif metalex.word_replace(span, rules[1], test=True):
                    spanR = metalex.word_replace(span, rules[1])
                    if okCorrect:
                        spanCorrect = metalex.correct_word(spanR)
                        contentCorrection += spanCorrect+' '
                    else: contentOrigin += spanR+' '
                    #print ('*****  '+span + ': ' + spanR)
                elif metalex.caract_replace(span, rules[2], test=True):
                    spanR = metalex.caract_replace(span, rules[2])
                    AllWords.append(spanR)
                    if okCorrect:
                        spanCorrect = metalex.correct_word(spanR)
                        contentCorrection += spanCorrect+' '
                    else: contentOrigin += spanR+' '
                    #print ('*****  '+span + ': ' + spanR)
                else:
                    if okCorrect:
                        AllWords.append(span)
                        spanCorrect = metalex.correct_word(span)
                        contentCorrection += spanCorrect+' '
                    else:
                        AllWords.append(span)
                        contentOrigin += span+' '
                #print ('*****  '+span + ': ' + spanCorrect)
        else: pass
        
        #print contentOrigin+'\n'
        artnum = 'article_'+str(art)
        crtnum = 'correction_'+str(art)
        if len(contentOrigin) >= 15 and len(contentCorrection) == 0:
            article = '%s==%s' %(artnum, contentOrigin)
            metalex.utils.write_temp_file(article, 'norm')
            art += 1
        elif len(contentOrigin) >= 15 and len(contentCorrection) >= 5:
            article = '%s==%s | %s==%s' %(crtnum, contentCorrection, artnum, contentOrigin)
            metalex.utils.write_temp_file(article, 'norm')
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
        word, caracter, regex = '\W', '\C', '\R'
        metadata, ruleWords, ruleCaracts, ruleRegex = {}, {}, {}, {}
        startw, startc, startr = False, False, False
        
        if self.file_rule_verified(self.typ):
            if self.typ == 'rule_wc':
                with codecs.open(self.file, 'r', 'utf-8') as rule:
                    for line in rule: 
                        line = line.strip()
                        if line.startswith('\metalex'): 
                            names = ('tool', 'project', 'theme', 'lang', 'admin', 'date')
                            for name, cnt in zip(names, line.split('\\')[1:]):
                                metadata[name] = cnt
                        if line == word: startw, startc, startr = True, False, False
                        if line == caracter: startw, startc, startr = False, True, False
                        if line == regex: startw, startc, startr = False, False, True
                        if startw:
                            linepart = line.split('/')
                            if len(linepart) == 3: ruleWords[linepart[1]] = linepart[2]
                        if startc:
                            linepart = line.split('/')
                            if len(linepart) == 3: ruleCaracts[linepart[1]] = linepart[2]
                        if startr:
                            linepart = line.split('/')
                            if len(linepart) == 3: ruleRegex[linepart[1]] = linepart[2]
            if self.typ == 'rule_art': return False
        else:
            log = u"file_rule_unpack() >> Your file rule syntax is not correct. Please correct it as recommended"
            metalex.logs.manageLog.write_log(log, typ='warm')
            
        return metadata, ruleWords, ruleCaracts, ruleRegex 
        
    
    def file_rule_verified(self, typ):
        """Verified if file rule content respect the norm description of metalex 
        
        :param typ: str
        
        :return Bool: True|Fase
        """
        module, synw, sync, synr, synrw, delimiter = (False for x in range(6))
        try: fileop = codecs.open(self.file, 'r', 'utf-8').readlines()
        except:
            log = u"file_rule_verified() >> We can't open your file rule. Please set it !"
            return metalex.logs.manageLog.write_log(log, typ='error')
        
        if typ == 'rule_wc':
            if '\START' == fileop[0].strip() and '\END' == fileop[-1].strip(): delimiter = True
            if len(fileop[1].strip().split('\\')) == 7:
                for el in fileop[1].strip().split('\\'):
                    if el == 'metalex': module = True
            for lg in fileop:
                lg = lg.strip()
                if lg == '\W': synw = True
                if lg == '\C': sync = True
                if lg == '\R': synr = True
                if lg[0] == '/': 
                    if len(lg.split('/')) == 3: synrw = True
            if sync and synw and synr and module and delimiter and synrw:
                return True
            else: return False
            
        if typ == 'rule_art': return False



