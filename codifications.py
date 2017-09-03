#!/usr/bin/env python
# coding: utf8


"""
    codifications build all means of codifications and other process related
    to metalexicographic processing

    Usage:
        >>> from MetaLex import codifications
        >>> allcodi = codifications.getAllCodifications()
        >>> codi    = codifications.getCodification(typ='text)
"""

# ----Internal Modules------------------------------------------------------

from MetaLex import dicLog
from MetaLex import dicProject

# ----External Modules------------------------------------------------------

import codecs

# -----Exported Functions---------------------------------------------------

__all__ = ['codificationsStore']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

class codificationsStore() :

    def getCodification(self, typ=None):
        """
          Generate specific means of codification type
          @param   typ:text|graph|symb|typo
          @return: list:allcoditext
        """
        if typ == u'text' :
            cats        = [u'n', u'adj', u'v', u'prép', u'adv', u'loc',
                           u'Fig', u'tr', u'intr', u'interj', u'art', u'conj', u'pron',
                           u'loc.conj', u'loc.adv', u'loc.adj', u'pron.relat', u'pronom'
                           u'article']
            genres      = [u'm', u'f']
            marques     = [u'fam', u'anc', u'UK', u'US' , u'PHY', u'LITT', u'ADMIN',
                           u'AERON', u'AGRIC', u'ANAT', u'ANTIQ',  u'ANTIQ.ROM',
                           u'BIOCHIM', u'BIOL',  u'CHIM.TECHN', u'CONSTR', u'ÉLECTR',
                           u'GRAMM', u'GÉOL', u'HIST', u'LING', u'LITURG', u'MATH',
                           u'MÉD', u'MÉTALL', u'MUS', u'POLIT', u'RELIG', u'ZOOL'
                           u'Phys']
            rections    = [u'tr', u't', u'intr', u't.dir', u't.indir', u'inv']
            nombres     = [u'plur', u'pl', u'sing', u'sg', u'neutre']
            affixes     = [u'suff', u'préf']
            varLings    = [u'ant', u'contr', u'syn', u'hom', u'fig', u'par_métonymie',
                           u'par_anal', u'encycl', u'etym', u'abrév', u'V', u'var']
            allcoditext = []
            for cat in cats :
                if len(cat) > 1 :
                    allcoditext.append(cat+u'.')
                    allcoditext.append(cat.capitalize()+u'.')
                    allcoditext.append(cat.upper()+u'.')
                else :
                    allcoditext.append(cat.capitalize()+u'.')
                    allcoditext.append(cat+u'.')
            for genre  in genres   : allcoditext.append(genre+u'.')
            for marque in marques  :
                allcoditext.append(marque+u'.')
                if not marque.isupper() : allcoditext.append(marque.upper()+u'.')
            for varL in varLings :
                allcoditext.append(varL+u'.')
                if not varL.isupper() : allcoditext.append(varL.capitalize()+u'.')
                allcoditext.append(varL.upper()+u'.')
            for nombre in nombres :
                allcoditext.append(nombre+u'.')
                allcoditext.append(nombre.capitalize()+u'.')
                allcoditext.append(nombre.upper()+u'.')
            for rection in rections  : allcoditext.append(rection+u'.')
            for affixe  in affixes   : allcoditext.append(affixe+u'.')
            return allcoditext

        if typ == u'graph' :
            graphs = [u'.', u',', u':', u'-', u';', u'[', u']', u'(', u')']
            return graphs

        if typ == u'symb' :
            symbs        = [u'||', u'&#9830;', u'--']
            allnumbers   = [u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0']
            alphabs      = [u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h', u'i',u'j',
                            u'k',u'l',u'm',u'n',u'o',u'q',u'r',u's',u't',u'v',
                            u'w',u'x', u'y', u'z']
            allcodisymbs = []
            for numb in allnumbers :
                allcodisymbs.append(numb+u'.')
                allcodisymbs.append(numb+u'-')
                allcodisymbs.append(numb+u')')
                allcodisymbs.append(u'('+numb+u')')
            for alpha in alphabs :
                allcodisymbs.append(alpha+u')')
                allcodisymbs.append(alpha.upper()+u'-')
                allcodisymbs.append(alpha.upper()+u'.')
            for symb in symbs : allcodisymbs.append(symb)
            return allcodisymbs

        if typ == u'typo' :
            typograhs = [u'(I)', u'(G)', u'(B)', u'(P)']
            return typograhs


    def getCodifTextType(self):
        cats        = [u'n', u'adj', u'v', u'prép', u'adv', u'loc',
                       u'Fig', u'tr', u'intr', u'interj', u'art', u'conj', u'pron',
                       u'loc.conj', u'loc.adv', u'loc.adj', u'pron.relat', u'pronom',
                       u'article', u'pr. rel']
        genres      = [u'm', u'f']
        marques     = [u'fam', u'anc', u'UK', u'US' , u'PHY', u'Phys', u'LITT', u'ADMIN',
                       u'AERON', u'AGRIC', u'ANAT', u'ANTIQ',  u'ANTIQ.ROM',
                       u'BIOCHIM', u'BIOL',  u'CHIM.TECHN', u'CONSTR', u'ÉLECTR',
                       u'GRAMM', u'GÉOL', u'HIST', u'LING', u'LITURG', u'MATH',
                       u'MÉD', u'MÉTALL', u'MUS', u'POLIT', u'RELIG', u'ZOOL'
                       u'Phys']
        rections    = [u'tr', u't', u'intr', u't.dir', u't.indir', u'inv']
        nombres     = [u'plur', u'pl', u'sing', u'sg', u'neutre']
        affixes     = [u'suff', u'préf']
        varLings    = [u'ant', u'contr', u'syn', u'hom', u'fig', u'par_métonymie',
                       u'par_anal', u'encycl', u'etym', u'abrév', u'V', u'var']

        allcoditype, allcodicats, allcodigenres, allcodirection, allcodinombres = {}, [], [], [], []
        allcodiaff, allcodivarlings, allcodimarques  = [], [], []
        for cat in cats :
            if len(cat) > 1 :
                allcodicats.append(cat+u'.')
                allcodicats.append(cat.capitalize()+u'.')
                allcodicats.append(cat.upper()+u'.')
            else :
                allcodicats.append(cat.capitalize()+u'.')
                allcodicats.append(cat+u'.')
        allcoditype[u'cats']  = allcodicats
        for genre in genres   :
            allcodigenres.append(genre+u'.')
        allcoditype[u'genres'] = allcodigenres
        for marque in marques :
            allcodimarques.append(marque+u'.')
            if not marque.isupper() : allcodimarques.append(marque.upper()+u'.')
            if not marque.isupper() : allcodimarques.append(marque.capitalize()+u'.')
            if marque.isupper()     : allcodimarques.append(marque.capitalize()+u'.')
            #if marque.isupper()     : allcodimarques.append(marque.lower()+u'.')
        allcoditype[u'marques'] = allcodimarques
        for varL in varLings :
            allcodivarlings.append(varL+u'.')
            if not varL.isupper() : allcodivarlings.append(varL.capitalize()+u'.')
            allcodivarlings.append(varL.upper()+u'.')
        allcoditype[u'varLings'] = allcodivarlings
        for nombre in nombres :
            allcodinombres.append(nombre+u'.')
            allcodinombres.append(nombre.capitalize()+u'.')
            allcodinombres.append(nombre.upper()+u'.')
        allcoditype[u'nombres'] = allcodinombres
        for rection in rections : allcodirection.append(rection+u'.')
        allcoditype[u'rection'] = allcodirection
        for affixe in affixes   : allcodiaff.append(affixe+u'.')
        allcoditype[u'affixe']  = allcodiaff
        return allcoditype


    def getCodifSymbType(self):
        symbs        = [u'||', u'&#9830;', u'--']
        allnumbers   = [u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0']
        alphabs      = [u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h', u'i',u'j',
                        u'k',u'l',u'm',u'n',u'o',u'q',u'r',u's',u't',u'v',
                        u'w',u'x', u'y', u'z']
        allcoditype, allcodisymbs, allcodinumbers, allcodialpha = {}, [], [], []
        for numb in allnumbers :
            allcodinumbers.append(numb+u'.')
            allcodinumbers.append(numb+u'-')
            allcodinumbers.append(numb+u')')
            allcodinumbers.append(u'('+numb+u')')
        allcoditype[u'numbers'] = allcodinumbers
        for alpha in alphabs :
            allcodialpha.append(alpha+u')')
            allcodialpha.append(alpha.upper()+u'-')
            allcodialpha.append(alpha.upper()+u'.')
        allcoditype[u'alpha'] = allcodialpha
        for symb in symbs : allcodisymbs.append(symb)
        allcoditype[u'symbs'] = allcodisymbs
        return allcoditype

    def getCodifGraphType(self):
        graphs = [u'.', u',', u':', u'-', u';', u'[', u']', u'(', u')']
        allcoditype = {}
        for graph in graphs :
            if graph == u'.' : allcoditype['point'] = u'.'
            if graph == u',' : allcoditype['virgule'] = u','
            if graph == u':' : allcoditype['dpoint'] = u':'
            if graph == u';' : allcoditype['pointv'] = u';'
            if graph == u'[' : allcoditype['ocrochet'] = u'['
            if graph == u']' : allcoditype['fcrochet'] = u']'
            if graph == u'(' : allcoditype['opara'] = u'('
            if graph == u')' : allcoditype['fpara'] = u')'
        return allcoditype

    def getAllCodifications(self) :
        """
            Get all existing dictionary codification
            @param   self:class object
            @return: dict:allcodifications
        """
        coditext  = self.getCodification(u'text')
        codigraph = self.getCodification(u'graph')
        coditypo  = self.getCodification(u'typo')
        codisymb  = self.getCodification(u'symb')
        allcodifications           = {}
        allcodifications[u'text']  = coditext
        allcodifications[u'graph'] = codigraph
        allcodifications[u'typo']  = coditypo
        allcodifications[u'symb']  = codisymb
        return allcodifications


    def exportCodifications(self, namefile, typ='text'):
        """
            Export dictionary codification to text file or to serialized pickle object
            @param   namefile:str
            @param   typ:str
            @return: file:allcodifications
        """
        coditext  = self.getCodification(u'text')
        codigraph = self.getCodification(u'graph')
        coditypo  = self.getCodification(u'typo')
        codisymb  = self.getCodification(u'symb')

        date = dicLog.getDate()
        if typ == u'text' :
            with codecs.open(namefile, 'a', 'utf-8') as f :
                f.write('******************** MetaLex codifications file : %s *********************************' %date)
                f.write('\%10s : %s' %('Textuels', str(coditext)))
                f.write('\%10s : %s' %('Graphematiques', str(codigraph)))
                f.write('\%10s : %s' %('Symboliques', str(codisymb)))
                f.write('\%10s : %s' %('Typographiques', str(coditypo)))
        if typ == 'pickle' :
            allcodi = self.getAllCodifications()
            dicProject.filePickle(allcodi, namefile)


    def importCodifications(self, namefile):
        return False


