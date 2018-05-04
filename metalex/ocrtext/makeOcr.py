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
import shutil
from PIL import ImageFilter as flt
from tesserocr import PyTessBaseAPI
from multiprocessing import Pool
from termcolor import colored

# ----Internal Modules------------------------------------------------------

import metalex

# -----Exported Functions---------------------------------------------------

__all__ = ['run_img_to_text']

# -----Global Variables-----------------------------------------------------



# --------------------------------------------------------------------------

def get_available_images(typ='tesserocr'):
    """Get all available path of dictionary images previously treated 

    :return array: list of path of enhanced dictionary images
    """
    allimages = ''
    if typ == 'tesserocr':
        if len(metalex.fileImages) >= 1 and not len(metalex.treatImages) >= 1 :
            contentPrint = "OCR ->> You don't have any previous treated image(s)!"+\
            " Please treat them before OCR "
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            allimages = metalex.fileImages
        elif not len(metalex.fileImages) >= 1 :
            contentPrint = "OCR ->>  You don't have any image(s) for this treatment"
            messageExit  = 'FATAL ERROR! We cannot continue, resolve the previous error'
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))
        else: allimages = metalex.treatImages
        return allimages
    elif typ == 'ocropy':
        if not len(metalex.fileImages) >= 1 :
            contentPrint = "OCR ->>  You don't have any image(s) for this treatment"
            messageExit  = 'FATAL ERROR! We cannot continue, resolve the previous error'
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
        metalex.currentOcr = 'tesserocr'
    
    def enhance_img_quality(self, typ='filter', filter=flt.DETAIL, value=0, other=0):
        """Enhance quality of image input files
        
        :param typ: type of enhancement
        :param filter: filter to use with typ=filter
        :param value: first value
        :param other: second value
        
        :return image enhanced
        """
        tiff = False
        for img in metalex.fileImages:
            if img.endswith('.tiff') or img.endswith('.tif'):
                messag = u"Tiff image is generally unstable for enhancement *"+img+u"*"+\
                " Instead use [png, jpg] format"
                metalex.logs.manageLog.write_log(messag, typ='warm')
                user = ''
                while user != 'y' or user != 'n':
                    user = raw_input('\tDo you really want to continue ? (y/n): ')
                    if user == 'y': 
                        tiff = True
                        break
                    elif user == 'n': return None
                break
        
        if tiff != True:   
            if typ == 'filter': metalex.EnhanceImages().filter(filter)
            if typ == 'contrast': metalex.EnhanceImages().contrast(value)
            if typ == 'bright': metalex.EnhanceImages().bright(value)
            if typ == 'sharp': metalex.EnhanceImages().sharp(value)
            if typ == 'contrastbright': metalex.EnhanceImages().contrast_bright(value, other)
                          
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
            
            image, ext = metalex.utils.get_part_file(img)
            imagepart = image.split('_')[:3]
            imagefile = image+ext

            imageconcat = ''
            for i in imagepart: imageconcat +='_'+i 
            imageconcat = imageconcat.split(u'.')[0]
            tempname = 'tesserocr'+imageconcat+'-ocr.html'
            
            metalex.utils.go_to_dicresult()
            if metalex.utils.in_dir(tempname) :
                message = "Starting optical characters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(message)
                textocr = api.GetHOCRText(2)
                messag = "Ending optical characters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
                
                metalex.utils.go_to_dicresult()
                if self.save:
                    with codecs.open(tempname, 'w', "utf-8") as wr :
                        wr.write(textocr)
                    message = "*"+ imagefile +"* is ocrized to > *"+\
                    tempname+"* > Saved in dicTemp folder" 
                    metalex.logs.manageLog.write_log(message) 
                    metalex.resultOcrData[img] = [textocr]
                elif self.show :
                    print("\n\n %s \n\n" %'**'*20)
                    print(textocr)
                    print(" %s \n\n" %'**'*20)
                else :
                    message = "imageToText(show=False, save=False) :"+\
                    " precise the action 'show=False or save=False'"
                    metalex.logs.manageLog.write_log(message, typ='warm') 
            else :
                messag = "[Treated] Ending optical characters recognition of *"+imagefile+u"* "
                metalex.logs.manageLog.write_log(messag)
            
            metalex.utils.write_temp_file(tempname, 'ocr')
                
    def image_to_text(self):
        """Run simultanously all OCR processes of dictionary files
    
        :return array: list of path of HTML files
        """
        allimages = get_available_images()
        processOcr = Pool(metalex.utils.calculate_process())
        if allimages == None: 
            contentPrint = u"OCR ->> You don't have any previous treated image(s)!"+\
            " Please treat them before OCR or change image format to [png] or [jpg] "
            messageExit  = u'We are going to use no enhance images'
            metalex.logs.manageLog.write_log(contentPrint, typ='error')
            sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='warm'))
            processOcr.map(self, metalex.fileImages)
            metalex.utils.read_temp_file('ocr')
        else:
            processOcr.map(self, allimages)
            metalex.utils.read_temp_file('ocr')
       
    def __call__(self, img):   
        return self.ocr_exec(img)

  
class BuildOcrOcropy():    
    def __init__(self, debug=0):
        self.debug = debug
        metalex.utils.go_to_dicresult()
        metalex.utils.create_temp()
        self.allimages = get_available_images('ocropy')       
        self.allimagesProc = []
        metalex.currentOcr = 'ocropy'
        
    def make_ocropy_folder(self):
        metalex.utils.create_temp()
        if 'ocropy_temp' not in os.listdir('.'): os.mkdir('ocropy_temp')
        os.chdir('ocropy_temp')
        for img in self.allimages: 
            if img not in os.listdir('.'): shutil.copy(img, '.')
              
    def binarized(self, black=5, errcheck='', white=90, percen=0, escale=1.0, paral=8):
        messag = u"Starting Ocropy-Binarization ... "
        metalex.logs.manageLog.write_log(messag)
        self.make_ocropy_folder()
        for inImg in os.listdir('.'): 
            for ext in ['.png', '.jpg', '.tiff', '.jpeg']:
                if inImg.endswith(ext): self.allimagesProc.append(inImg)
        
        groupImgFiles = metalex.utils.chunck_list(self.allimagesProc, 1000)
        for i, imgFilesPart in enumerate(groupImgFiles):
            imgFilesPart = ' '.join(imgFilesPart)
            if len(glob.glob('*.nrm.png')) == len(self.allimages): 
                metalex.logs.manageLog.write_log('Binarization already treated ...', typ='warm')
                return None
            metalex.ocropy_command('nlbin', param=' '+errcheck+' --lo '+str(black)+\
                ' -p '+str(percen)+' -e '+str(escale)+' '+imgFilesPart+' --debug '+\
                str(self.debug)+' --hi '+str(white)+' -Q '+str(paral))
                         
    def segment(self, scale=0.0, errcheck='', gray='', expand=3, padding=3, 
                     clnsep='', vscale=1.0, hscale=1.0, paral=8, maxlines=300):
        messag = u"Starting Ocropy-Segmentation ... "
        print('\n')
        metalex.logs.manageLog.write_log(messag)
        self.make_ocropy_folder()
        
        binFiles = glob.glob('*.bin.png')
        groupBinFiles = metalex.utils.chunck_list(binFiles, 1000)
        for i, binFilesPart in enumerate(groupBinFiles):
            binFilesPart = ' '.join(binFilesPart)
            if len(glob.glob('*.pseg.png')) == len(self.allimages): 
                metalex.logs.manageLog.write_log('Segmentation already treated ...', typ='warm')
                return None
            metalex.ocropy_command('pageseg', param=' '+errcheck+' --maxlines 1000 '+\
                clnsep+' --scale '+str(scale)+' --hscale '+str(hscale)+' --vscale '+\
                str(vscale)+' --gray '+str(gray)+' -e '+str(expand)+'  --maxlines '+\
                str(maxlines)+' -p '+str(padding)+'  '+binFilesPart+' -Q '+str(paral))
             
    def recognize(self, model='', llocs='', proba='', errorcheck='', 
                    quiet='', show=-1, context=0, conf_matrix='', paral=1):
        messag = u"Starting Ocropy-Recognition ... "
        print('\n')
        metalex.logs.manageLog.write_log(messag)
        self.make_ocropy_folder()
        
        binFiles = glob.glob('*/*.bin.png')
        if len(model) <= 1: model = metalex.modeldef
        groupBinFiles = metalex.utils.chunck_list(binFiles, 1000)
        for binFilesPart in groupBinFiles:
            binFilesPart = ' '.join(binFilesPart)
            if len(glob.glob('*/*.txt')) > 20: 
                metalex.logs.manageLog.write_log('Recognition already treated ...', typ='warm')
                return None
            metalex.ocropy_command('rpred', param=' '+str(binFilesPart)+' -m '+model+\
                    ' -s '+str(show)+' --context '+str(context)+' '+quiet+' '+llocs+\
                    ' '+proba+' '+' '+conf_matrix+' '+errorcheck+'  -Q '+str(paral))

    def builds_out(self):
        self.make_ocropy_folder()
        nameFolder = [x.replace('/', '') for x in glob.glob('*/')]
        messag = u"Starting Ocropy-BuildVisualisation ... "
        print('\n')
        metalex.logs.manageLog.write_log(messag)
        self.make_ocropy_folder()
        
        dicresults = metalex.utils.get_root_project()+'/dicResults/'
        for fld in nameFolder:
            rexHtmlName = dicresults+'ocropy_'+fld+'-ocr.html'
            rexHtmlEditName = dicresults+'ocropy_'+fld+'-edit.html'
            if fld+'-ocr.html' and fld+'-edit.html' in os.listdir(dicresults): 
                metalex.logs.manageLog.write_log('BuildVisualisation already treated ...',
                                                  typ='warm')
            else:
                metalex.ocropy_command('hocr', param=' '+fld+'.bin.png  -o '+rexHtmlName)
                metalex.ocropy_command('edit', param=' html  -o '+rexHtmlEditName+' '+fld+'/*.bin.png')
        
        for img in glob.glob(dicresults+'*-ocr.html'):
            metalex.resultOcrFiles.append(img)
            
        """  
        rexname = 'results'
        rexFolderN = metalex.utils.get_root_project()+'/dicTemp#'+rexname
        rexOrgName = rexname+'_ocr.txt'
        metalex.ocropy_command('edit', param=' write -x _write.txt '+rexOrgName+'  '+rexFolderN)
        """
    
    def image_to_text(self, model=''):
        self.binarized()
        self.segment()
        self.recognize(model=model)
        self.builds_out()
    

class run_img_to_text():
    def __init__(self, typ='ocropy', save=True, langIn='fra'):
        self.typ = typ
        self.save = save
        self.lang = langIn
    
    def enhance_img(self, typ='filter', filter=flt.DETAIL, value=0, other=0):
        if self.typ == 'tesserocr':
            tesserocr = BuildOcrTesserocr()
            tesserocr.enhance_img_quality(typ=typ, filter=filter, value=value, other=other)
        
    def run_ocr(self, model=''):
        if self.typ == 'ocropy': 
            print('\n --- %s %s \n\n' %(colored('Part 2 : OCR (Ocropy)',
                                                 attrs=['bold']), '---'*12))
            ocropy = BuildOcrOcropy()
            ocropy.make_ocropy_folder()
            ocropy.image_to_text(model=model)
        
        elif self.typ == 'tesserocr':
            print('\n --- %s %s \n\n' %(colored('Part 2 : OCR (Tesserocr)', 
                                                 attrs=['bold']), '---'*12))
            tesserocr = BuildOcrTesserocr(save=self.save, langIn=self.lang)
            tesserocr.image_to_text()
            htmls = [os.path.abspath(x) for x in glob.glob('tesserocr*.html')]
            metalex.utils.go_to_dicresult()
            if len(htmls) >= 1:
                for html in htmls:
                    name = html.split('/')[-1]
                    if name not in os.listdir('.'): shutil.move(html, '.')
                    else: os.remove(html)
        else:
            messag = "You must choice between [ocropy] or [tesserocr] "
            metalex.logs.manageLog.write_log(messag, typ='warm')
            return None
        
        
        
