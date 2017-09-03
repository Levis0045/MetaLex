#! usr/bin/env python
# coding: utf8


"""
    Implémentation des outils d'ocrisation de l'image.
 
    Packages:
        >>> sudo apt-get install tesseract-ocr-all
        >>> sudo apt-get install libtesseract-dev libleptonica-dev 
        >>> sudo pip install Cython
        >>> sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
        >>> sudo pip termcolor
        
    Usage:
        >>> import MetaLex as dico
        >>> import ImageFilter as     
        >>> project = dico.newProject(project_name)
        >>> images = project.MetaLex.getImages(imagelist)
        >>> images.enhanceImages().filter(f.DETAIL)
        >>> images.imageToText(show=True, langIn='fra')
    
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

from tesserocr import PyTessBaseAPI
import codecs, os
from termcolor import colored

# -----Exported Functions-----------------------------------------------------

__all__ = ['imageToText']

# -----Global Variables-----------------------------------------------------


# ----------------------------------------------------------

    
def imageToText(show=False, save=False, langIn='fra'):
    """
        Take image files, ocrised and save them to 'dicTemp' folder
        @param   show:Bool
        @param   save:Bool
        @param   langIn:str
        @return: str|file (MetaLex.resultOcrData)
    """
    datefile = os.popen('date').read()
    try :
        datetab = datefile.split(',')[1].split(' ')
        hour = datetab[1]
    except :
        datetab = datefile.split(' ')[3]
        hour = datetab
        
    log = u'[MetaLexLog - '+hour+u']'
    allimages = []
    if len(MetaLex.fileImages) >= 1 and not len(MetaLex.treatImages) >= 1 :
        contentPrint = u"Vous avez aucun(s) fichier(s) image traité(s), veuillez les traiter avant la lecture optique"
        print u'\n%-10s  %-30s\n' %(colored(log, u'red', attrs=['reverse', 'blink', 'bold']), contentPrint)
        os.chdir('..')
        return None
    elif not len(MetaLex.fileImages) >= 1 :
        contentPrint = u"Vous n'avez aucun(s) fichier(s) image à traiter"
        print u'\n%-10s %-30s\n' %(colored(log, u'red', attrs=['reverse', 'blink', 'bold']), contentPrint)
    else:
        allimages = MetaLex.treatImages
         
    num = 1
    for img in allimages :
        with PyTessBaseAPI() as api:
            api.Init(lang=langIn)
            api.SetImageFile(img)
            
            image, ext = MetaLex.dicProject.get_part_file(img)
            imagepart = image.split('_')[:3]
            imagefile = image+ext
            
            imageconcat = u''
            for i in imagepart :
                imageconcat +=u'_'+i 
            imageconcat = imageconcat.split(u'.')[0]
            tempname = u'text_ocr'+imageconcat+u'.html'
            
            MetaLex.dicProject.createtemp()
            if MetaLex.dicProject.inDir(tempname) :
                message = u"Début de la lecture optique de"
                print u'\n%-10s  %-24s %s \n' %(colored(log, u'green', attrs=['reverse', 'blink', 'bold']), message, imagefile.strip())
                textocr = api.GetHOCRText(2)
                messag = u"Fin de la lecture optique de"
                print u'\n%-10s  %-24s %s \n' %(colored(log, u'green', attrs=['reverse', 'blink', 'bold']), messag, imagefile.strip())
                
                if save:
                    with codecs.open(tempname, 'w', "utf-8") as wr :
                        wr.write(textocr)
                    message = u"'"+ imagefile +u"' is Ocrised to > '"+tempname+u"' > Saved in dicTemp folder" 
                    MetaLex.dicLog.manageLog.writelog(message) 
                    MetaLex.resultOcrData[img] = [textocr]
                    #os.chdir('..')
                elif show :
                    print u"\n\n*********************************************************\n\n"
                    print textocr
                    print u"\n\n*********************************************************\n\n"
                else :
                    message = u" Warning : imageToText(show=False, save=False) >> precise the action 'show=False or save=False'"
                    MetaLex.dicLog.manageLog.writelog(message) 
            else :
                messag =  u"Fin de la lecture optique de \n"
                print u'\n%-10s  %-24s %s \n' %(colored(log, u'green', attrs=['reverse', 'blink', 'bold']), messag, imagefile)
                 
            MetaLex.dicProject.treat_ocr_append(tempname)
            os.chdir('..')
              
            
        num += 1
                
    return MetaLex.resultOcrData
                
                
                
                
