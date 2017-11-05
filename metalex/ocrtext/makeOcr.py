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
from multiprocessing import Pool
from termcolor import colored

# -----Exported Functions---------------------------------------------------

__all__ = ['BuildOcrImages']

# -----Global Variables-----------------------------------------------------



# --------------------------------------------------------------------------
    
class BuildOcrImages():
    """Extract all text data from dictionary images files 
    
    :param show: bool
    :param save: bool
    :param langIn: str (language used in OCR : format 'fra | eng | esp',  etc.)
    
    :return array: list of path of 
    """
    
    def __init__(self, show=False, save=True, langIn='fra'):
        self.show = show
        self.save = save
        self.langIn = langIn
        print  u'\n --- %s ---------------------------------------------------------------------- \n\n' %colored('Part 2 : OCR', attrs=['bold'])
        
    def get_available_images(self):
        """Get all available path of dictionary images previously treated 
    
        :return array: list of path of enhanced dictionary images
        """
        if len(metalex.fileImages) >= 1 and not len(metalex.treatImages) >= 1 :
            contentPrint = u"OCR >> You don't have any previous treated image(s)! Please treat them before OCR "
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            return None
        elif not len(metalex.fileImages) >= 1 :
            contentPrint = u"OCR >>  You don't have any image(s) for this treatment"
            messageExit  = u'FATAL ERROR! We cannot continue, resolve the previous error'
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))
        else:
            allimages = metalex.treatImages
        return allimages
    
    
    def calculate_process(self):
        """Calculate a number of processes usefull for OCR processing
    
        :return int: number of processes
        """
        processExec = 0
        lenImages = len(self.get_available_images())
        if lenImages == 1: 
            processExec = 1
        elif lenImages == 2:
            processExec = 2
        elif lenImages > 2 and lenImages < 10 :
            processExec = 3
        elif lenImages > 10 :
            processExec = 5
        return processExec
            
    
    def ocr_exec(self, img):
        """Take image files, ocrised and save them to 'dicTemp' folder
        
        :param show: Bool
        :param save: Bool
        :param langIn: str
        
        :return str|file (metalex.resultOcrData)
        """
    
        with PyTessBaseAPI() as api:
            api.Init(lang=self.langIn)
            api.SetImageFile(img)
            
            image, ext = metalex.project.get_part_file(img)
            imagepart = image.split('_')[:3]
            imagefile = image+ext
            
            imageconcat = u''
            for i in imagepart:
                imageconcat +=u'_'+i 
            imageconcat = imageconcat.split(u'.')[0]
            tempname = u'text_ocr'+imageconcat+u'.html'
            
            metalex.project.create_temp()
            if metalex.project.in_dir(tempname) :
                message = u"Starting optical charaters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(message)
                textocr = api.GetHOCRText(2)
                messag = u"Ending optical charaters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
                
                metalex.project.create_temp()
                if self.save:
                    with codecs.open(tempname, 'w', "utf-8") as wr :
                        wr.write(textocr)
                    message = u"*"+ imagefile +u"* is Ocrised to > *"+tempname+u"* > Saved in dicTemp folder" 
                    metalex.logs.manageLog.write_log(message) 
                    metalex.resultOcrData[img] = [textocr]
                elif self.show :
                    print u"\n\n*********************************************************\n\n"
                    print textocr
                    print u"\n\n*********************************************************\n\n"
                else :
                    message = u"imageToText(show=False, save=False) : precise the action 'show=False or save=False'"
                    metalex.logs.manageLog.write_log(message, typ='warm') 
            else :
                messag = u"Ending optical charaters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
            
            metalex.project.write_temp_file(tempname, 'ocr')
            
    
    def image_to_text(self):
        """Run simultanously all OCR processes of dictionary files
    
        :return array: list of path of HTML files
        """ 
        allimages = self.get_available_images()
        processOcr = Pool(self.calculate_process())
        processOcr.map(self, allimages)
        metalex.project.read_temp_file('ocr')

        
    def __call__(self, img):   
        return self.ocr_exec(img)
    
    
