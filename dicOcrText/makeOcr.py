#! usr/bin/env python
# coding: utf8


"""
    Implémentation des outils d'ocrisation de l'image.
 
    Packages:
        >>> sudo apt-get install tesseract-ocr-all
        >>> sudo apt-get install libtesseract-dev libleptonica-dev 
        >>> sudo pip install Cython
        >>> sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
        
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

# -----Exported Functions---------------------------------------------------

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
        
    allimages = []
    if len(MetaLex.fileImages) >= 1 and not len(MetaLex.treatImages) >= 1 :
        contentPrint = u"OCR >> You don't have any previous treated image(s)! Please treat them before OCR "
        MetaLex.dicLog.manageLog.writelog(contentPrint, typ='error')
        os.chdir('..')
        return None
    elif not len(MetaLex.fileImages) >= 1 :
        contentPrint = u"OCR >>  You don't have any image(s) for this treatment"
        MetaLex.dicLog.manageLog.writelog(contentPrint, typ='error')
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
                message = u"OCR >> Début de la lecture optique de "+imagefile+u' '
                MetaLex.dicLog.manageLog.writelog(message)
                textocr = api.GetHOCRText(2)
                messag = u"Fin de la lecture optique de "+imagefile+u' '
                MetaLex.dicLog.manageLog.writelog(messag)
                
                MetaLex.dicProject.createtemp()
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
                    message = u"OCR >> imageToText(show=False, save=False) : precise the action 'show=False or save=False'"
                    MetaLex.dicLog.manageLog.writelog(message, typ='warm') 
            else :
                messag =  u"OCR >> Fin de la lecture optique de '"+imagefile+u"' "
                MetaLex.dicLog.manageLog.writelog(messag)
                
            MetaLex.dicProject.treat_ocr_append(tempname)
            os.chdir('..')
              
            
        num += 1
                
    return MetaLex.resultOcrData
                
                
                
                
