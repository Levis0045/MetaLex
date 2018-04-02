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

-------------------------------------------------------------------------

word spelling mecanism.

Usage:
    >>> from metalex.wordsCorrection import *
    >>> correctWord(word)
"""

# ----External Modules------------------------------------------------------

import re
import sys 
import collections
from collections import Counter

# ----Internal Modules------------------------------------------------------

import metalex

# -----Exported Functions---------------------------------------------------

__all__ = ['correct_word', 'word_replace', 'caract_replace']

# -----Global Variables-----------------------------------------------------



# --------------------------------------------------------------------------

def correct_word (word):
    """Give a good spelling of the input word
    
   :param  word:str
      
   :return str:word 
    """
    correct = wordCorrection()
    if len(word) > 1:
        word = word.strip()
        if word[-1] in [u'.', u',']:
            fin = word[-1]
            if word[0].isupper():
                deb = word[0]
                wordc = word[:-1]
                goodword = correct.correction(wordc.lower())
                wordg = deb+goodword[1:]+fin
                return wordg
            else: 
                wordc = word[:-1]
                goodword = correct.correction(wordc)
                wordg = goodword+fin
                return wordg
        elif word[-1] in [u')']: return word
        elif word[1] in [u"'", u"’"]:
            wordtab = word.split(u"’")
            deb, wordc = wordtab[0], wordtab[1]
            goodword = correct.correction(wordc)
            wordg = deb+u'’'+goodword[1:]
            return wordg
        elif word[0] in [u":"]:
            wordtab = word.split(u":")
            deb, wordc = wordtab[0], wordtab[1]
            goodword = correct.correction(wordc)
            wordg = deb+u'’'+goodword[1:]
            return wordg
        else:
            goodword = correct.correction(word)
            return goodword
    else: return word


class WordCorrection:
    """Give a good spelling of the input word
    
   :return inst:objetwordcorrection
    """
    
    def __init__(self):
        metalex.dicPlugins
        filepath = sys.path[-1]+'/metalex_words-corpus.txt'
        self.corpusData = open(filepath).read()
        self.WORDS = {}
        self.start()
        self.lettersFr = u"abcdefghijklmnopqrstuvwxyzéèêîiïàùûâ'"

    def start(self): self.WORDS = self.train(self.words(self.corpusData))
        
    def words(self, text): return re.findall(r'(\s+)', text.lower())
    
    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features: model[f] += 1
        return model

    def edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.lettersFr if b]
        inserts    = [a + c + b     for a, b in splits for c in self.lettersFr]
        return set(deletes + transposes + replaces + inserts)
    
    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.WORDS)
    
    def known(self, words): return set(w for w in words if w in self.WORDS)
    
    def correction(self, word):
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        return max(candidates, key=self.WORDS.get)
    
    
    
def word_replace(word, data, test=False):
    """
    
    """
    equiv_words = data
    if test:
        if equiv_words.has_key(word): return True
        else: return False
    elif word in equiv_words.keys():
        return equiv_words[word]
        
       
def caract_replace(word, data, test=False):
    """
    
    """
    equiv_caract = data
    equiv_keys = equiv_caract.keys()
    if test:
        for k in equiv_keys:
            #print word + ' ' + k
            if word.find(k): return True
            else: return False
    else:
        for k in equiv_keys:
            #print equiv_caract.keys()
            if word.find(k): return re.sub(k, equiv_caract[k], word)
            
    
    