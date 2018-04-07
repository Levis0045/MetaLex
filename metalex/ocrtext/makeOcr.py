#! usr/bin/env python
# coding: utf8

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

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


# ----External Modules------------------------------------------------------

import codecs
import os
import sys
import glob
from tesserocr import PyTessBaseAPI
from multiprocessing import Pool
from termcolor import colored

# ----Internal Modules------------------------------------------------------

import metalex

# -----Exported Functions---------------------------------------------------

__all__ = ['BuildOcrTesserocr', 'BuildOcrOcropy']

# -----Global Variables-----------------------------------------------------



# --------------------------------------------------------------------------

def get_available_images(typ='tesserocr'):
    """Get all available path of dictionary images previously treated 

    :return array: list of path of enhanced dictionary images
    """
    if typ == 'tesserocr':
        if len(metalex.fileImages) >= 1 and not len(metalex.treatImages) >= 1 :
            contentPrint = u"OCR ->> You don't have any previous treated image(s)!"+\
            " Please treat them before OCR "
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            return None
        elif not len(metalex.fileImages) >= 1 :
            contentPrint = u"OCR ->>  You don't have any image(s) for this treatment"
            messageExit  = u'FATAL ERROR! We cannot continue, resolve the previous error'
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))
        else: allimages = metalex.treatImages
        return allimages
    elif typ == 'ocropy':
        if not len(metalex.fileImages) >= 1 :
            contentPrint = u"OCR ->>  You don't have any image(s) for this treatment"
            messageExit  = u'FATAL ERROR! We cannot continue, resolve the previous error'
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))
        else: allimages = metalex.fileImages
        return allimages 
      
      
class BuildOcrTesserocr():
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
        print(u'\n --- %s %s \n\n' %(colored('Part 2 : OCR (Tesserocr)', attrs=['bold']), '---'*15))
      
    def calculate_process(self):
        """Calculate a number of processes useful for OCR processing
    
        :return int: number of processes
        """
        processExec = 0
        lenImages = len(get_available_images())
        if lenImages == 1: processExec = 1
        elif lenImages == 2: processExec = 2
        elif lenImages > 2 and lenImages < 10 : processExec = 5
        elif lenImages > 10: processExec = 8
        return processExec          
    
    def ocr_exec(self, img):
        """Take image files, ocrized and save them to 'dicTemp' folder
        
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
            for i in imagepart: imageconcat +=u'_'+i 
            imageconcat = imageconcat.split(u'.')[0]
            tempname = u'text_ocr'+imageconcat+u'.html'
            
            metalex.project.create_temp()
            if metalex.project.in_dir(tempname) :
                message = u"Starting optical characters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(message)
                textocr = api.GetHOCRText(2)
                messag = u"Ending optical characters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
                
                metalex.project.create_temp()
                if self.save:
                    with codecs.open(tempname, 'w', "utf-8") as wr :
                        wr.write(textocr)
                    message = u"*"+ imagefile +u"* is ocrized to > *"+\
                    tempname+u"* > Saved in dicTemp folder" 
                    metalex.logs.manageLog.write_log(message) 
                    metalex.resultOcrData[img] = [textocr]
                elif self.show :
                    print(u"\n\n %s \n\n" %'**'*20)
                    print(textocr)
                    print(u" %s \n\n" %'**'*20)
                else :
                    message = u"imageToText(show=False, save=False) :"+\
                    " precise the action 'show=False or save=False'"
                    metalex.logs.manageLog.write_log(message, typ='warm') 
            else :
                messag = u"Ending optical characters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
            
            metalex.project.write_temp_file(tempname, 'ocr')
                
    def image_to_text(self):
        """Run simultanously all OCR processes of dictionary files
    
        :return array: list of path of HTML files
        """ 
        allimages = get_available_images()
        processOcr = Pool(self.calculate_process())
        processOcr.map(self, allimages)
        metalex.project.read_temp_file('ocr')
       
    def __call__(self, img):   
        return self.ocr_exec(img)

  
class BuildOcrOcropy():    
    def __init__(self, debug=0):
        self.debug = debug
        metalex.project.go_to_dicresult()
        metalex.project.create_temp()
        self.allimages = get_available_images('ocropy')
        print(u'\n --- %s %s \n\n' %(colored('Part 2: OCR (Ocropy)',
                                             attrs=['bold']), '---'*15))
        
    def binarized(self, black=5, errcheck='', white=90, percen=0, escale=1.0, paral=8):
        messag = u"Starting Ocropy-Binarization -------- "
        metalex.logs.manageLog.write_log(messag)
        metalex.project.create_temp()
        groupImgFiles = metalex.project.chunck_list(self.allimages, 1000)
        for i, imgFilesPart in enumerate(groupImgFiles):
            imgFilesPart = ' '.join(imgFilesPart)
            metalex.ocropy_command('nlbin', param=' '+errcheck+' --lo '+str(black)+\
                ' -p '+str(percen)+' -e '+str(escale)+' '+imgFilesPart+' --debug '+\
                str(self.debug)+' --hi '+str(white)+' -Q '+str(paral)+' -o ocropy')
            
             
    def segment(self, scale=0.0, errcheck='', gray='', expand=3, padding=3, 
                     clnsep='', vscale=1.0, hscale=1.0, paral=8, maxlines=300):
        messag = u"Starting Ocropy-Segmentation -------- "
        metalex.logs.manageLog.write_log(messag)
        metalex.project.create_temp()
        
        binFiles = glob.glob('ocropy/*.bin.png')
        
        groupBinFiles = metalex.project.chunck_list(binFiles, 1000)
        for i, binFilesPart in enumerate(groupBinFiles):
            binFilesPart = ' '.join(binFilesPart)
            metalex.ocropy_command('pageseg', param=' '+errcheck+' --maxlines 1000 '+\
                clnsep+' --scale '+str(scale)+' --hscale '+str(hscale)+' --vscale '+\
                str(vscale)+' --gray '+str(gray)+' -e '+str(expand)+'  --maxlines '+\
                str(maxlines)+' -p '+str(padding)+'  '+binFilesPart+' -Q '+str(paral))
            
    
    def recognize(self, model='', llocs='', proba='', errorcheck='', 
                    quiet='', show=-1, context=0, conf_matrix='', paral=1):
        messag = u"Starting Ocropy-Recognition -------- "
        metalex.logs.manageLog.write_log(messag)
        metalex.project.create_temp()
        
        binFiles = glob.glob('ocropy/*/*.bin.png')
        if len(model) <= 1: model = metalex.model4
        groupBinFiles = metalex.project.chunck_list(binFiles, 1000)
        for binFilesPart in groupBinFiles:
            binFilesPart = ' '.join(binFilesPart)
            metalex.ocropy_command('rpred', param=' '+str(binFilesPart)+' -m '+model+\
                    ' -s '+str(show)+' --context '+str(context)+' '+quiet+' '+llocs+\
                    ' '+proba+' '+' '+conf_matrix+' '+errorcheck+'  -Q '+str(paral))

    
    def builds_out(self):
        rexHtmlName = metalex.project.get_root_project()+'/dicResults/results_ocr.html'
        rexHtmlEditName = metalex.project.get_root_project()+'/dicResults/results_ocr-edit.html'
        metalex.ocropy_command('hocr', param='  *.bin.png  -o '+rexHtmlName)
        metalex.ocropy_command('edit', param=' html  -o '+rexHtmlEditName+' */*.bin.png')
        
        rexname = 'results'
        rexFolderN = metalex.project.get_root_project()+'/dicTemp#'+rexname
        rexOrgName = rexname+'_ocr.txt'
        metalex.ocropy_command('edit', param=' write -x _write.txt '+rexOrgName+'  '+rexFolderN)

    
    def image_to_text(self):
        #self.binarized()
        os.chdir('ocropy')
        #self.segment()
        #self.recognize()
        self.builds_out()
    

        
        
        