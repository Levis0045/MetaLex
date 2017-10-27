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
    
    Optical recognition characters implementation.
 
    Packages:
        >>> sudo apt-get install tesseract-ocr-all
        >>> sudo apt-get install libtesseract-dev libleptonica-dev 
        >>> sudo pip install Cython
        >>> sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
        
    Usage:
        >>> import metalex as dico
        >>> import ImageFilter as     
        >>> project = dico.newProject(project_name)
        >>> images = project.metalex.getImages(imagelist)
        >>> images.enhanceImages().filter(f.DETAIL)
        >>> images.imageToText(show=True, langIn='fra')
    
"""

# ----Internal Modules------------------------------------------------------

import metalex

# ----External Modules------------------------------------------------------

import codecs
import os
import sys
from tesserocr import PyTessBaseAPI

# -----Exported Functions---------------------------------------------------

__all__ = ['image_to_text']

# -----Global Variables-----------------------------------------------------


# ----------------------------------------------------------

    
def image_to_text(show=False, save=False, langIn='fra'):
    """Take image files, ocrised and save them to 'dicTemp' folder
    
    :param   show: Bool
    :param   save: Bool
    :param   langIn: str
    
    :return str|file (metalex.resultOcrData)
    """
        
    allimages = []
    if len(metalex.fileImages) >= 1 and not len(metalex.treatImages) >= 1 :
        contentPrint = u"OCR >> You don't have any previous treated image(s)! Please treat them before OCR "
        metalex.logs.manageLog.write_log(contentPrint, typ='error')
        os.chdir('..')
        return None
    elif not len(metalex.fileImages) >= 1 :
        contentPrint = u"OCR >>  You don't have any image(s) for this treatment"
        messageExit  = u'FATAL ERROR! We cannot continue, resolve the previous error'
        metalex.logs.manageLog.write_log(contentPrint, typ='error')
        sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))
    else:
        allimages = metalex.treatImages
         
    num = 1
    for img in allimages :
        with PyTessBaseAPI() as api:
            api.Init(lang=langIn)
            api.SetImageFile(img)
            
            image, ext = metalex.project.get_part_file(img)
            imagepart = image.split('_')[:3]
            imagefile = image+ext
            
            imageconcat = u''
            for i in imagepart :
                imageconcat +=u'_'+i 
            imageconcat = imageconcat.split(u'.')[0]
            tempname = u'text_ocr'+imageconcat+u'.html'

            metalex.project.create_temp()
            if metalex.project.in_dir(tempname) :
                message = u"OCR >> Starting optical charaters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(message)
                textocr = api.GetHOCRText(2)
                messag = u"OCR >> Ending optical charaters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
                
                metalex.project.create_temp()
                if save:
                    with codecs.open(tempname, 'w', "utf-8") as wr :
                        wr.write(textocr)
                    message = u"*"+ imagefile +u"* is Ocrised to > *"+tempname+u"* > Saved in dicTemp folder" 
                    metalex.logs.manageLog.write_log(message) 
                    metalex.resultOcrData[img] = [textocr]
                elif show :
                    print u"\n\n*********************************************************\n\n"
                    print textocr
                    print u"\n\n*********************************************************\n\n"
                else :
                    message = u"OCR >> imageToText(show=False, save=False) : precise the action 'show=False or save=False'"
                    metalex.logs.manageLog.write_log(message, typ='warm') 
            else :
                messag = u"OCR >> Ending optical charaters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
                
            metalex.project.treat_ocr_append(tempname)
            os.chdir('..')
              
            
        num += 1
                
    return metalex.resultOcrData
                
                
                
                
