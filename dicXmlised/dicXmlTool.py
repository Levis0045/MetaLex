#! usr/bin/env python
# -*- coding: utf8 -*-

"""
    Give extra functions for parser of dictionary and XML/HTML generator
    
    Usage:
        >>> from MetaLex.dicXmilised import *
        >>> generateID()
"""

# ----Internal Modules------------------------------------------------------

import MetaLex
from   composeArticle import *
from   MetaLex        import codifications


# ----External Modules------------------------------------------------------

import re, sys, codecs, os
from random import sample
from lxml   import etree
from bs4    import BeautifulSoup

# -----Exported Functions---------------------------------------------------

__all__ = ['generateID', 'getDataArticles', 'metalexGenerateXml', 'deSpecialised',
           'articleTypeForm']

# -----Global Variables-----------------------------------------------------

codi       = codifications.codificationsStore()
contentDic = codi.getAllCodifications()

# --------------------------------------------------------------------------

    
def generateID():
    """
      Generate ID of 5 characters with alpha numeric characters 
      @return: str:id generated
    """
    idart = sample([u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0',u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'v',u'w',u'y',u'z'], k=5)
    return u''.join(idart)


def articleTypeForm(art):
    """
      Find type form of article depending on their codification  
      @param art:str 
      @return: str:int of type found
    """
    soup = BeautifulSoup(art, 'html.parser')
    try : 
        if re.search(ur'<cte_cat>', unicode(soup.contents[1])) :
            if re.search(ur'<cte_gender>', unicode(soup.contents[3])) :
                if re.search(ur'<cte_rection>', unicode(soup.contents[5])) :
                    return u'7' #cat, gender and rection
                    #print '****gender**** '+art+'*****\n'
                else: return u'2' #cat and gender
            elif re.search(ur'<cte_rection>', unicode(soup.contents[3])) :
                return u'4' #cat and rection
                #print '*****rection*** '+art+'*****\n'
            else:
                return u'1' #cat
                #print '*****cat*** '+art+'*****\n'
        elif re.search(ur'<cgr_vrg>', unicode(soup.contents[1])) : 
            if re.search(ur'<cgr_vrg>', unicode(soup.contents[3])) : 
                return u'3' #vrg, vrg and cat
                #print '*****cat*** '+art+'*****\n'  
            else :
                return u'8' #vrg and cat
                #print '*****cat*** '+art+'*****\n'
        elif re.search(ur'<cgr_ocrh>', unicode(soup.contents[1])) : 
            if re.search(ur'<cte_gender>', unicode(soup.contents[7])) : 
                return u'6' #crh, crh, cat and gender
                #print '*****cat*** '+art+'*****\n'
            else :
                return u'5' #crh, crh, cat and rection
        else :
            return u'9' #Problematic case
            #print '*****cat*** '+art+'*****\n'
    except IndexError : pass
    
    
def getDataArticles(typ):
    """
      Get data article from the store data file depending of the type wanted   
      @return: dic:datapickle or datatext
    """
    MetaLex.dicProject.createtemp()
    contentdir = os.listdir('.')
    filepickle = u''
    filetext   = u''
    for fil in contentdir :
        if fil.split('.')[1]   == u'pickle' :
            filepickle = fil 
        elif fil.split('.')[1] == u'art'    :
            filetext = fil
    if typ == u'pickle' :
        datapickle = MetaLex.dicProject.fileUnpickle(filepickle)
        return datapickle
    if typ == u'text' :
        datatext = MetaLex.dicProject.fileGettext(filetext)
        return datatext


def deSpecialised(strng):
    if strng.find(u')') : 
        return strng.replace(u')', u'\)')
    if strng.find(u'.') : 
        return strng.replace(u'.', u'\.')

       
 
class metalexGenerateXml():
    
    def trans(self, ruleEl, nsmap=None) :
        attribs, el = '', ''
        if re.search(ur'{', ruleEl) : 
            partel  = re.split(ur'{', ruleEl.strip()) 
            el      = partel[0].strip()
            if re.search(ur',', partel[1]) :
                attribs = re.split(ur',', partel[1][:-1])
            else : attribs = partel[1].strip()
            elEtree = etree.Element(el, nsmap=None)
            for attrib in attribs :
                attr, val = re.split(ur':', attrib.strip())
                elEtree.set(attr, val)
            return elEtree
        else :
            elEtree = etree.Element(ruleEl.strip(), nsmap=None)
            return elEtree
    
    def nextSect(self, nextS, m2, m1):
        nexts = nextS
        if re.search(ur'-', nexts) :
            nodes = re.split(ur'-', nexts())
            for node in nodes :
                if node == nodes[-1] :
                    m2.append(self.trans(node))
                    m1.append(m2)
                    m3 = self.trans(node)
                    try :
                        nextCh = nexts.next()
                        self.nextSect(nextCh, m3, m2)
                    except StopIteration :
                        print etree.tostring(m1, pretty_print=True)
                        break
                else :
                    m2.append(self.trans(node))
        else : 
            m2.append(self.trans(nexts))
            m1.append(m2)
        
                
    def makeRuleHtmlXml(self, datarule, typ='xml'):
        elements = re.split(ur'->', datarule)
        master   = self.trans(elements[0])
        lenchild = elements[1:]
        childs   = iter(elements[1:])
        if lenchild > 2 :
            i = 1
            while i < lenchild :
                try :
                    childsnext = childs.next()
                    if re.search(ur'-', childsnext) :
                        nodes = re.split(ur'-', childsnext)
                        for node in nodes :
                            if node == nodes[-1] :
                                master.append(self.trans(node))
                                master2 = self.trans(node)
                                try :
                                    nextCh = childs.next()
                                    self.nextSect(nextCh, master2, master)
                                except StopIteration :
                                    print etree.tostring(master, pretty_print=True)
                                    break
                            else :master.append(self.trans(node))           
                    else : master.append(self.trans(childsnext))
                    i += 1
                except StopIteration :
                    print etree.tostring(master, pretty_print=True)
                    break
            
    
    
    
    
        