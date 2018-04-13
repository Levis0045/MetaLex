#! usr/bin/env python
# coding: utf8

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

"""metalex is general tool for lexicographic and metalexicographic activities

Copyright (C) 2017  by Elvis MBONING

This program is free software: yo can redistribte it and/or modify
it nder the terms of the GN Affero General Pblic License as
pblished by the Free Software Fondation, either version 3 of the
License, or (at yor option) any later version.

This program is distribted in the hope that it will be sefl,
bt WITHOT ANY WARRANTY; withot even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICLAR PRPOSE.  See the
GN Affero General Pblic License for more details.

Yo shold have received a copy of the GN Affero General Pblic License
along with this program.  If not, see <https://www.gn.org/licenses/>.

Contact: levismboning@yahoo.fr

---------------------------------------------------------------------------

Implémentation de détection de composants  des articles.

Packages:
    >>> apt-get install python-html5lib
    >>> apt-get install python-lxml
    >>> apt-get install python-bs4
    
sage:
    >>> from metalex.dicOcrText import *
    >>> parseArticle()
    >>> structredWithCodif()
        
"""

# ----External Modles------------------------------------------------------

import re
import sys
import codecs
import time
from bs4  import BeautifulSoup
from lxml import etree

# ----Internal Modles------------------------------------------------------

import metalex 
from metalex import codifications
from metalex import utils
from .dicXmlTool import * 

# -----Exported Fnctions---------------------------------------------------

__all__ = ['parse_article', 'StructuredWithCodif']

# -----Global Variables-----------------------------------------------------

codi = codifications.CodificationsStore()
contentDic = codi.get_all_codifications()
textCodif = codi.get_codif_text_type()
symbCodif = codi.get_codif_symb_type()
graphCodif = codi.get_codif_graph_type()

# --------------------------------------------------------------------------

def parse_article(textart, log=False):
    """Generate reslts from Parser codifications types
    
   :param  textart: str
      
   :return dict: resltext
    """
    codif=['text', 'symb', 'typo', 'graph']
    i, c = 0, 0
    parser = ParserCodification(log)
    resultext = parser.proc_codi(textart, i, c, codif, contentDic, log)
    #print resltext
    return resultext


def bild_replace_codif(codif, typ):
    """Make balise to codifications types 
    
   :param codif: str
   :param type: str
    
   :return str: balise codification type
    """
    for k, v in contentDic.items():
        if typ == 'text' and codif in v and k == typ:
            for i, t in textCodif.items():
                if codif in t and i == 'cats'   : return ' <cte_cat>'+codif+'</cte_cat> '
                if codif in t and i == 'genres' : return ' <cte_gender>'+codif+'</cte_gender> '
                if codif in t and i == 'marqes': return ' <cte_mark>'+codif+'</cte_mark> '
                if codif in t and i == 'varLings': return ' <cte_vLings>'+codif+'</cte_vLings> '
                if codif in t and i == 'nombres': return ' <cte_nbre>'+codif+'</cte_nbre> '
                if codif in t and i == 'rection': return ' <cte_rection>'+codif+'</cte_rection> '
                if codif in t and i == 'affixe' : return ' <cte_affix>'+codif+'</cte_affix> '
        
        elif typ == 'symb' and codif in v and k == typ:
            for i, t in symbCodif.items():
                if codif in t and i == 'numbers': return ' <csy_chif>'+codif+'</cte_chif> '
                if codif in t and i == 'alpha'  : return ' <cte_alpha>'+codif+'</cte_alpha> '
                if codif in t and i == 'symbs'  : return ' <cte_syb>'+codif+'</cte_syb> '
        
        elif typ == 'graph' and codif in v and k == typ:
            for i, t in graphCodif.items():
                if codif == t and i == 'point'   : return ' <cgr_pt>'+codif+'</cgr_pt> '
                if codif == t and i == 'virgule'  : return ' <cgr_vrg>'+codif+'</cgr_vrg> '
                if codif == t and i == 'pointv'  : return ' <cgr_ptvrg>'+codif+'</cgr_ptvrg> '
                if codif == t and i == 'dpoint'  : return ' <cgr_dpt>'+codif+'</cgr_dpt> '
                if codif == t and i == 'ocrochet': return ' <cgr_ocrh>'+codif+'</cgr_ocrh> '
                if codif == t and i == 'fcrochet': return ' <cgr_fcrh>'+codif+'</cgr_fcrh> '
                if codif == t and i == 'opara'   : return ' <cgr_opar>'+codif+'</cgr_opar> '
                if codif == t and i == 'fpara'   : return ' <cgr_fpar>'+codif+'</cgr_fpar> '
                
                
class ParserCodification():
    """Parse data article with all type of dictionaries codification
    
   :return dict: resltext
    """
    
    def __init__(self, log):
        self.result = ''
        self.codif = ['text', 'symb', 'typo', 'graph']
        self.log = log
        
    def proc_codi(self, art, i, c, codif, codifs, log):
        num = i
        codift = self.codif[c] 
        codi = ' '+codifs[codift][num]+' '
        
        if  art.find(codi) != -1:
            if self.log: print('3')
            if codift == 'text': replac = bild_replace_codif(codifs[codift][num], 'text')
            if codift == 'graph': replac = bild_replace_codif(codifs[codift][num], 'graph')
            if codift == 'typo': replac = ' <cty>'+codifs[codift][num]+'</cty> '
            if codift == 'symb': replac = bild_replace_codif(codifs[codift][num], 'symb')
            if self.log: print('%-10s -- %s ' %(codi, replac))
            artcodi = art.replace(codi, replac)
            self.result = artcodi
            num += 1
            if num < len(codifs[codift]):
                if self.log: print('4', codifs[codift][num])
                self.proc_codi(artcodi, num, c, self.codif, codifs, self.log)
            elif c < 3:
                c = c + 1
                num = 0
                self.proc_codi(artcodi, num, c, self.codif, codifs, self.log)
                if self.log: print(artcodi, codif[c])
            if c == 3 and art == None:
                self.result = art
        else: 
            num += 1
            if num < len(codifs[codift]):
                if self.log: print('6', codifs[codift][num])
                self.proc_codi(art, num, c, self.codif, codifs, self.log)
            elif c < 3:
                c = c + 1
                num = 0
                self.proc_codi(art, num, c, self.codif, codifs, self.log)
            elif c == 3 and art == None:
                self.result = art

        return self.result



class StructuredWithCodif():
    """Extract all single article from date articles codified
    
   :return dict: contentall
    """
    
    def __init__(self, data, otpt, log=False):
        self.data = data
        self.dataCodified = ''
        self.dataBalised = ''
        self.otpt = otpt
        self.treat_articles = []
        self.log = log
    
    def normalize_data_to_codif(self):
        """Extract all single article from date articles codified
        
       :return dict: contentall
        """
        contentall = {}
        for art in self.data.keys():
            content = ''
            for word in re.split(r' ', self.data[art]):
                word = word.strip()
                if re.search(r"[a-z.éèùàê,]+", word, re.I):
                    if word.isalnum() and word[-1] == ';' or word[-1] == ':' or word[-1] == ',':
                        word, caract = word[:-1], word[-1]
                        content += word+' {0} '.format(caract)
                    elif len(word)> 2 and word[-1] == '.' and word[0] != '(' and word[-2] != ')' and word not in contentDic['text']:
                        word, caract = word[:-1], word[-1]
                        content += word+' {0} '.format(caract)
                    elif word[0]  == '('  and word not in contentDic['symb']:
                        if self.log: print(word, '----------------')
                        word, caract = word[1:], word[0]
                        content += caract+' {0} '.format(word)
                    elif len(word)> 2 and word[-1] == '.' and word[-2] == ')' and word not in contentDic['symb']:
                        if self.log: print(word, word[-2],'----------------')
                        word, caract, point = word[:-2], word[-2], word[-1]
                        content += word+' {0} {1} '.format(caract, point)
                    elif len(word)> 2 and word[0] == '[' and word[-1] == ']' and word not in contentDic['symb']:
                        if self.log: print(word, word[-2],'----------------')
                        word, caract1, caract2 = word[1:-1], word[0], word[-1]
                        content += ' {0} {1} {2} '.format(caract1, word, caract2)
                    else: content += word +' '
                else: content += word+''
            
            contentall[art] = content
        return contentall
          
          
    def codified_articles(self):
        """Get all normalize articles and parse its content codifications types
        
       :return dict: datacodified
        """
        debut = time.time()

        dataArticles = self.normalize_data_to_codif()
        dnormal = time.time() - debut
        debut   = time.time()
        datacodified = {}
        for art in dataArticles.keys():
            artcodif = parse_article(dataArticles[art], self.log)
            datacodified[art] = artcodif
        dcodif  = time.time() - debut
        if self.log:
            print("Durée normalisation texte por codif: %10.3f seconds\n" %dnormal)
            print("Durée parsage codif texte: %10.3f seconds\n" %dcodif)
            
        utils.save_normalized_data(name='articles_'+metalex.currentOcr+'-codified.art', 
                                   typ='text', data=datacodified)
        return datacodified
         
         
    def read_tag(self, tag):
        """Read content of tag element
        
       :param tag: str 
        
       :return str: element (content of tag)
        """
        elsearch = re.search(r'<.+>(.+)</.+>', tag)
        element = elsearch.grop(1)
        return element
    
    
    def segment_articles (self, article, log):
        if re.search(r'.+\s<cgr_pt>\.</cgr_pt>\s.+\s<cte_cat>.+', article): 
            arts = re.search(r'(.+\s<cgr_pt>\.</cgr_pt>)(\s.+\s<cte_cat>.+)', article)
            art1, art2 = arts.group(1), arts.group(2)
            self.segment_articles(art1, self.log)
            self.segment_articles(art2, self.log)
        else:
            if self.log: print('3-----------------------------\n'+article+'---------------------------\n\n')
            self.treat_articles.append(article)
    
    
    def format_articles(self):
        """Get all articles from one compact string article
        
       :return list: treat_articles
        """
        dataCodified = self.codified_articles()
        for i, article in dataCodified.items():
            if i == 'article1': self.treat_articles.append('sep')
            if article.count('<cgr_pt>.</cgr_pt>') >= 2:
                if re.search(r'<cgr_pt>\.</cgr_pt>\s<cte_cat>', article):
                    self.treat_articles.append(article)
                    if self.log: print('1-----------------------------\n'+article+'---------------------------\n\n')
                elif self.segment_articles(article, self.log): print(Tre)
            else:
                self.treat_articles.append(article)
                if self.log: print('2-----------------------------\n'+article+'---------------------------\n\n')
        return self.treat_articles
                    
                    