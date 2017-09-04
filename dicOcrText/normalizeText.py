#! usr/bin/env python
# coding: utf8

"""
    Implémentation des outils de normalization du texte des articles.
    
    Packages:
        >>> apt-get install python-html5lib
        >>> apt-get install python-lxml
        >>> apt-get install python-bs4
    
    Usage:
        >>> from MetaLex.dicOcrText import *
        >>> makeTextWell('dico_rules_larousse.dic')
    
"""

# ----Internal Modules------------------------------------------------------

import MetaLex
from MetaLex import dicXmlised as Xml
from MetaLex import codifications

# ----External Modules------------------------------------------------------

from bs4 import BeautifulSoup
import re, sys, codecs, os, time
import warnings
#import ipdb

# -----Exported Functions-----------------------------------------------------

__all__ = ['makeTextWell', 'fileRule']

# -----Global Variables-----------------------------------------------------

dicArticles = []
AllWords    = []
namepickle  = ''
nametxt     = ''

# ----------------------------------------------------------


def makeTextWell(file_rules, okCorrect=False, log=False):
    """
      Composed and saved all treatments process to enhance quality of html articles 
      @param   file_rules:str
      @param   okCorrect:bool
      @return: file:pickle and text 
    """
    debut = time.time()
    filerule = fileRule(file_rules, typ=u'rule_wc')
    data_rules = filerule.fileRuleUnpack()
    dfilerule = time.time() - debut
    
    html_ocr_files = MetaLex.resultOcrFiles
    if len(html_ocr_files) >= 1 :
        for html in html_ocr_files :
            with open(html, 'r') as html_file :
                enhanceText(html_file, data_rules, okCorrect)
            
        namepickle = MetaLex.dicProject.nameFile(html_ocr_files, u'.pickle')
        nametxt    = MetaLex.dicProject.nameFile(html_ocr_files, u'.art')
        
        saveNormalize(namepickle, u'pickle')
        saveNormalize(nametxt, u'text')     
           
        if log : print "--> %30s : %10.5f seconds\n" %("Durée d'extraction du fichier des règles", dfilerule)
    else :
        message = u'We are not found any OCR files to enhance text quality'
        return MetaLex.dicLog.manageLog.writelog(message, typ='error')
              
def enhanceText(html_file, rules, okCorrect):
    """
       Enhance quality of text by remove all inconvenients characters and optionally 
       correct malformed words.
       @param   html_file:str file
       @param   rules:str
       @param   okCorrect:Bool
       @return: list:dicArticles
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
                            spanCorrect = MetaLex.correctWord(span)
                            contentCorrection += spanCorrect
                        else :
                            contentOrigin += span
                        #print '*****  '+span + ' : ' + spanCorrect
                    elif MetaLex.wordReplace(span, rules[1], test=True) :
                        spanR = MetaLex.wordReplace(span, rules[1])
                        if okCorrect :
                            spanCorrect = MetaLex.correctWord(spanR)
                            contentCorrection += spanCorrect+u' '
                        else :
                            contentOrigin += spanR+u' '
                        #print '*****  '+span + ' : ' + spanR
                    elif MetaLex.caractReplace(span, rules[2], test=True):
                        spanR = MetaLex.caractReplace(span, rules[2])
                        AllWords.append(spanR)
                        if okCorrect :
                            spanCorrect = MetaLex.correctWord(spanR)
                            contentCorrection += spanCorrect+u' '
                        else:
                            contentOrigin += spanR+u' '
                        #print '*****  '+span + ' : ' + spanR
                    else:
                        if okCorrect :
                            AllWords.append(span)
                            spanCorrect = MetaLex.correctWord(span)
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
                article = {artnum:contentOrigin}
                dicArticles.append(article)
                art += 1
            elif len(contentOrigin) >= 15 and len(contentCorrection) >= 5 :
                article = {crtnum:contentCorrection, artnum:contentOrigin}
                dicArticles.append(article)
                art += 1
    
    
    
def saveNormalize(name, typ):
    """
      Saved normalized text in text format (*.art) or in pickle format (*.pickle) 
      @param   name:str file
      @param   typ:str
      @return: file:texts extracted
    """
    MetaLex.dicProject.createtemp()
    if typ == u'text' :
        if MetaLex.dicProject.inDir(name) :
            with codecs.open(name, 'a', 'utf-8') as fil :
                num = 1
                for art in dicArticles :
                    for k, v in art.items() :
                        if k != u'article_1' :
                            fil.write('%10s : %s\n' %(k, v))
                        else :
                            fil.write('\n----- FILE: %s ---------------------------------------------------------------------------------\n\n' %num)
                            fil.write('%10s : %s\n' %(k, v))
                            num += 1
            message = name+u' is created and contain all text format data from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
        else :
            message = name+u' is created and contain all text format data from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
    
    if typ == u'pickle' :  
        if MetaLex.dicProject.inDir(name) and MetaLex.dicProject.filePickle(dicArticles, name) :
            message = name+u' is created and contain pickle data object from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message)         
        else :
            message = name+u' is created and contain pickle data object from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message)     
        
 
        
class fileRule():
    """
      Managing of input file rules for text normalization
      @param   file_rule:str file
      @param   typ:str
      @return: obj:fileRule instanciation
    """
    
    def __init__(self, file_rule, typ):
        self.file = file_rule
        self.typ = typ
         
    def fileRuleUnpack(self):
        """
          Unpack file rule and extract its contents
          @param   self:class object
          @return: dict:metadata, ruleWords, ruleCaracts, ruleRegex
        """
        word, caracter, regex = u'\W', u'\C', u'\R'
        metadata, ruleWords, ruleCaracts, ruleRegex = {}, {}, {}, {}
        startw, startc, startr = False, False, False
        
        if self.verify(self.typ) :
            if self.typ == u'rule_wc' :
                with codecs.open(self.file, 'r', 'utf-8') as rule :
                    for line in rule : 
                        line = line.strip()
                        if line.startswith(u'\MetaLex') : 
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
            log = u"fileRuleUnpack() >> Your file rule syntax is not correct. Please correct it as recommended"
            MetaLex.dicLog.manageLog.writelog(log, typ='warm')
            
        return metadata, ruleWords, ruleCaracts, ruleRegex 
        
    
    def verify(self, typ):
        """
          Verified if file rule content respect the norm description of MetaLex 
          @param   typ:str
          @return: Bool:True|Fase
        """
        module, synw, sync, synr, synrw, delimiter = (False for x in range(6))
        try :
            fileop = codecs.open(self.file, 'r', 'utf-8').readlines()
        except :
            log = u"verify() >> We can't open your file rule. Please set it !"
            return MetaLex.dicLog.manageLog.writelog(log, typ='error')
        
        if typ == u'rule_wc' :
            if u'\START' == fileop[0].strip() and u'\END' == fileop[-1].strip() : delimiter = True
            if len(fileop[1].strip().split(u'\\')) == 7 :
                for el in fileop[1].strip().split(u'\\') :
                    if el == u'MetaLex': module = True
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



