#! usr/bin/env python
# coding: utf8

"""
    Implémentation de détection de composants  des articles.
 
    Packages:
        >>> apt-get install python-html5lib
        >>> apt-get install python-lxml
        >>> apt-get install python-bs4
        
    Usage:
        >>> from MetaLex.dicOcrText import *
        >>> parseArticle()
        >>> structuredWithCodif()
        
"""

# ----Internal Modules------------------------------------------------------

from MetaLex    import codifications
from dicXmlTool import * 

# ----External Modules------------------------------------------------------

import re, sys, codecs, time
from bs4  import BeautifulSoup
from lxml import etree

# -----Exported Functions---------------------------------------------------

__all__ = ['parseArticle', 'structuredWithCodif']

# -----Global Variables-----------------------------------------------------

codi       = codifications.codificationsStore()
contentDic = codi.getAllCodifications()
textCodif  = codi.getCodifTextType()
symbCodif  = codi.getCodifSymbType()
graphCodif = codi.getCodifGraphType()

# --------------------------------------------------------------------------

def parseArticle(textart) :
    """
      Generate results from Parser codifications types
      @param  textart:str
      @return: dict:resultext
    """
    codif=[u'text', u'symb', u'typo', u'graph']
    i, c = 0, 0
    p = parserCodification()
    resultext = p.procCodi(textart, i, c, codif, contentDic)
    return resultext


def buildReplaceCodif(codif, typ):
    """
      Make balise to codifications types 
      @param  codif:str
      @param   type:str
      @return: str:balise codification type
    """
    for k, v in contentDic.items():
        if typ == u'text' and codif in v and k == typ :
            for i, t in textCodif.items() :
                if codif in t and i == u'cats'    : return u' <cte_cat>'+codif+u'</cte_cat> '
                if codif in t and i == u'genres'  : return u' <cte_gender>'+codif+u'</cte_gender> '
                if codif in t and i == u'marques' : return u' <cte_mark>'+codif+u'</cte_mark> '
                if codif in t and i == u'varLings': return u' <cte_vLings>'+codif+u'</cte_vLings> '
                if codif in t and i == u'nombres' : return u' <cte_nbre>'+codif+u'</cte_nbre> '
                if codif in t and i == u'rection' : return u' <cte_rection>'+codif+u'</cte_rection> '
                if codif in t and i == u'affixe'  : return u' <cte_affix>'+codif+u'</cte_affix> '
        
        elif typ == u'symb' and codif in v and k == typ  :
            for i, t in symbCodif.items() :
                if codif in t and i == u'numbers' : return u' <csy_chif>'+codif+u'</cte_chif> '
                if codif in t and i == u'alpha'   : return u' <cte_alpha>'+codif+u'</cte_alpha> '
                if codif in t and i == u'symbs'   : return u' <cte_syb>'+codif+u'</cte_syb> '
        
        elif typ == u'graph' and codif in v and k == typ  :
            for i, t in graphCodif.items() :
                if codif == t and i == u'point'    : return u' <cgr_pt>'+codif+u'</cgr_pt> '
                if codif == t and i == u'virgule'  : return u' <cgr_vrg>'+codif+u'</cgr_vrg> '
                if codif == t and i == u'pointv'   : return u' <cgr_ptvrg>'+codif+u'</cgr_ptvrg> '
                if codif == t and i == u'dpoint'   : return u' <cgr_dpt>'+codif+u'</cgr_dpt> '
                if codif == t and i == u'ocrochet' : return u' <cgr_ocrh>'+codif+u'</cgr_ocrh> '
                if codif == t and i == u'fcrochet' : return u' <cgr_fcrh>'+codif+u'</cgr_fcrh> '
                if codif == t and i == u'opara'    : return u' <cgr_opar>'+codif+u'</cgr_opar> '
                if codif == t and i == u'fpara'    : return u' <cgr_fpar>'+codif+u'</cgr_fpar> '
                
                
class parserCodification() :
    """
      Parse data article with all type of dictionaries codification
      @return: dict:resultext
    """
    
    def __init__(self):
        self.result = u''
        self.codif = [u'text', u'symb', u'typo', u'graph']
          
    def procCodi(self, art, i, c, codif, codifs, log=False):
        num    = i
        codift = self.codif[c] 
        codi   = ' '+codifs[codift][num]+' '
        
        if  art.find(codi)  != -1 :
            if log : print '3'
            if codift == u'text' : replac = buildReplaceCodif(codifs[codift][num], u'text')
            if codift == u'graph': replac = buildReplaceCodif(codifs[codift][num], u'graph')
            if codift == u'typo' : replac = u' <cty>'+codifs[codift][num]+u'</cty> '
            if codift == u'symb' : replac = buildReplaceCodif(codifs[codift][num], u'symb')
            artcodi = art.replace(codi, replac)
            self.result = artcodi
            num += 1
            if num < len(codifs[codift]) :
                if log : print '4', codifs[codift][num]
                self.procCodi(artcodi, num, c, self.codif, codifs, log)
            elif c < 3 :
                c = c + 1
                num = 0
                self.procCodi(artcodi, num, c, self.codif, codifs, log)
                if log : print artcodi, codif[c]
            if c == 3 and art == None :
                self.result = art
        else : 
            num += 1
            if num < len(codifs[codift]) :
                if log : print '6', codifs[codift][num]
                self.procCodi(art, num, c, self.codif, codifs, log)
            elif c < 3 :
                c = c + 1
                num = 0
                self.procCodi(art, num, c, self.codif, codifs, log)
            elif c == 3 and art == None :
                self.result =  art
        
        return self.result



class structuredWithCodif():
    """
      Extract all single article from date articles codified
      @return: dict:contentall
    """
    
    def __init__(self, data, output):
        self.data          = data
        self.dataCodified  = u''
        self.dataBalised   = u''
        self.output        = output
        self.treatArticles = []
    
    def normalizeDataToCodif(self, log=False):
        """
          Extract all single article from date articles codified
          @return: dict:contentall
        """
        contentall = {}
        for art in self.data.keys() :
            content = u''
            for word in re.split(ur' ', self.data[art]) :
                word = word.strip()
                if re.search(ur"[a-z.éèùàê,]+", word, re.I):
                    if word.isalnum() and word[-1] == u';' or word[-1] == u':' or word[-1] == u',':
                        word, caract = word[:-1], word[-1]
                        content += word+u' {0} '.format(caract)
                    elif len(word)> 2 and word[-1] == u'.' and word[0] != u'(' and word[-2] != u')' and word not in contentDic['text'] :
                        word, caract = word[:-1], word[-1]
                        content += word+u' {0} '.format(caract)
                    elif word[0]  == u'('  and word not in contentDic['symb'] :
                        if log : print word, '----------------'
                        word, caract = word[1:], word[0]
                        content += caract+u' {0} '.format(word)
                    elif len(word)> 2 and word[-1] == u'.' and word[-2] == u')' and word not in contentDic['symb'] :
                        if log : print word, word[-2],'----------------'
                        word, caract, point = word[:-2], word[-2], word[-1]
                        content += word+u' {0} {1} '.format(caract, point)
                    elif len(word)> 2 and word[0] == u'[' and word[-1] == u']' and word not in contentDic['symb'] :
                        if log : print word, word[-2],'----------------'
                        word, caract1, caract2 = word[1:-1], word[0], word[-1]
                        content += u' {0} {1} {2} '.format(caract1, word, caract2)
                    else :
                        content += word +u' '
                else :
                    content += word+u''
            contentall[art]  = content
        return contentall
          
          
    def codifiedArticles(self, log=False):
        """
          Get all normalize articles and parse its content codifications types
          @return: dict:datacodified
        """
        debut = time.time()

        dataArticles = self.normalizeDataToCodif()
        dnormal = time.time() - debut
        debut   = time.time()
        datacodified = {}
        for art in dataArticles.keys() :
            artcodif          = parseArticle(dataArticles[art])
            datacodified[art] = artcodif
        dcodif  = time.time() - debut
        if log :
            print "Durée normalisation texte pour codif : %10.3f seconds\n" %dnormal
            print "Durée parsage codif texte : %10.3f seconds\n" %dcodif
        return datacodified
         
         
    def readTag(self, tag):
        """
          Read content of tag element
          @param tag:str 
          @return: str:element (content of tag)
        """
        elsearch = re.search(ur'<.+>(.+)</.+>', tag)
        elment   = elsearch.group(1)
        return elment
    
    
    def segmentArticles (self, article, log):
        if re.search(ur'.+\s<cgr_pt>\.</cgr_pt>\s.+\s<cte_cat>.+', article) : 
            arts = re.search(ur'(.+\s<cgr_pt>\.</cgr_pt>)(\s.+\s<cte_cat>.+)', article)
            art1, art2 = arts.group(1), arts.group(2)
            self.segmentArticles (art1, log)
            self.segmentArticles (art2, log)
        else :
            if log : print '3-----------------------------\n'+article+'---------------------------\n\n'
            self.treatArticles.append(article)
    
    
    def formatArticles(self, log=False):
        """
          Get all articles from one compact string article
          @return: list:treatArticles
        """
        dataCodified  = self.codifiedArticles()
        for i, article in dataCodified.items() :
            if i == 'article1' : self.treatArticles.append('sep')
            if article.count('<cgr_pt>.</cgr_pt>') >= 2 :
                if re.search(ur'<cgr_pt>\.</cgr_pt>\s<cte_cat>', article) :
                    self.treatArticles.append(article)
                    if log : print '1-----------------------------\n'+article+'---------------------------\n\n'
                elif self.segmentArticles(article, log):
                    print True
            else :
                self.treatArticles.append(article)
                if log : print '2-----------------------------\n'+article+'---------------------------\n\n'
        return self.treatArticles
                    
                    