#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    
    Normalization tool for images.
 
    Package:
        >>> pip install pillow
    
    Usage:
        >>> import metalex as dico
        >>> import ImageFilter
        >>> project = dico.newProject(project_name)
        >>> images = project.metalex.getImages(imagelist)
        >>> images.enhanceImages().filter(f.DETAIL)
        >>> images.enhanceImages().bright(1, save=True)
    
    ImageFilter.filters:
        'BLUR', 'BuiltinFilter', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 
        'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'Filter', 
        'GaussianBlur', 'Kernel', 'MaxFilter', 'MedianFilter', 
        'MinFilter', 'ModeFilter', 'RankFilter', 
        'SHARPEN', 'SMOOTH', 'SMOOTH_MORE', 'UnsharpMask'
          
"""

# ----External Modules------------------------------------------------------

import os
import sys
from PIL import Image
from PIL import ImageEnhance
from shutil import copyfile
from termcolor import colored

# ----Internal Modules------------------------------------------------------

import metalex

# ----Exported Functions-----------------------------------------------------

__all__ = ['get_images', 'EnhanceImages']

# ----------------------------------------------------------


def get_images(images):
    """Take input image list and save it in the scope
    
    :param images: file
    
    :return file: images 
    """
    
    if len(images) >= 1 :
        num = 1
        for image in images : 
            exts = ('.png', '.jpg', '.JPG', '.jpeg', '.PNG', '.JPEG', 
                    '.tiff', '.gif', 'tif')
            imageroot, ext = metalex.utils.get_part_file(image)

            if os.path.isfile(image) and ext in exts:
            
                mainFolder = 'metalex_'+metalex.projectName
                mainPath = metalex.projectFolder[mainFolder]
                
                imagedirNew = mainPath+'/'+mainFolder+"/dicImages/"
                if not os.path.exists(imagedirNew): os.mkdir(imagedirNew)
                    
                imagefileNew = "dic_image_"+str(num)+ext
                imageLocationNew =  imagedirNew+imagefileNew
                copyfile(image, imageLocationNew)
                metalex.fileImages.append(imageLocationNew)
                num += 1
            else :
                message = "getImages(images) >> The input image *"+imageroot+ext+"* is not a file image"
                metalex.logs.manageLog.write_log(message, typ='error')
                 
        imagestr = str(images)
        message  = ' *'+imagestr +'* >> are append for the current treatment' 
        metalex.logs.manageLog.write_log(message)
    else: 
        message = 'getImages(images) >> They are not images for the current treatment : input images !!' 
        metalex.logs.manageLog.write_log(message, typ='error')
        messageExit = 'FATAL ERROR! We cannot continue, resolve the previous error'
        sys.exit(metalex.logs.manageLog.write_log(messageExit, typ='error'))
    return metalex
    
        
   
class EnhanceImages ():
    """This Class enhance image file and save them to 'dicTemp'
    
    :param fileImages: file
    
    :return inst object 
    """
    
    def __init__(self): 
        self.images = metalex.fileImages
        print(u'\n %s %s %s \n\n' %('---', 
                                    colored('Part 1 : EnhanceImages', 
                                            attrs=['bold']), '---'*12))
        
    def contrast(self, value, show=False, save=False):
        """ Enhance image file with the contrast value
        
        :param value: int
        :param show: Bool
        :param save: Bool
        
        :return file: imagecontrast   
        """
        if self.images >= 1 : 
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = metalex.utils.get_part_file(image)
                tempname = u'img_contrast_'+str(num)+ext
                enh = ImageEnhance.Contrast(img)
                
                if show : enh.enhance(value).show()
                elif save :
                    metalex.utils.create_temp()
                    if metalex.utils.in_dir(tempname) :
                        enh.enhance(value).save(tempname)
                        metalex.utils.treat_image_append(tempname)
                        message = u'*'+imagename+u'* is modified with contrast (' +str(value)+\
                         u') > *'+tempname+u'* > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        num += 1
                    else :
                        metalex.utils.treat_image_append(tempname)
                        message = u'*'+imagename+u'* is modified with contrast (' +str(value)+\
                         u') > *'+tempname+u'* > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        num += 1
                else :
                    message = u'contrast(value, show=False, save=False) -->'+\
                    u' You must define one action for the current treatment : show=true or save=true '
                    metalex.logs.manageLog.write_log(message, typ='warm')
        else:
            message = u'contrast(images) >> They are not images for the'+\
                    u'current treatment : please input images !! ' 
            metalex.logs.manageLog.write_log(message, typ='error')
                        
    def sharp(self, value, show=False, save=False):
        """Enhance image file with the sharp value
        
        :param value: int
        :param show: Bool
        :param save: Bool
          
        :return file: imagesharp   
        """
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img_conv = self.convert(image, save=True)
                img = Image.open(img_conv)
                imagename, ext = metalex.utils.get_part_file(image)
                tempname = u'img_sharp_'+str(num)+ext
                enh = ImageEnhance.Sharpness(img)

                if show: enh.enhance(value).show()
                elif save :
                    metalex.utils.create_temp()
                    if metalex.utils.in_dir(tempname) :
                        enh.enhance(value).save(tempname)
                        metalex.utils.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = u'*'+imagename+u'* is modified with sharp ( ' +str(value)+\
                         u') > *'+tempname+u'* > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        num += 1 
                    else :
                        metalex.utils.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = u'*'+imagename+u'* is modified with contrast (' +str(value)+\
                         u') > *'+tempname+u'* > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        num += 1
                else :
                    message = u'sharp(value, show=False, save=False) --> You must '+\
                    'define one action for the current treatment : show=true or save=true'
                    metalex.logs.manageLog.write_log(message, typ='warm')
        else:
            message = u'sharp(images) >> They are not images for the current treatment : please input images !! ' 
            metalex.logs.manageLog.write_log(message, typ='error')
                       
    def bright(self, value, show=False, save=False):
        """Enhance image file with the bright value
        
        :param value: int
        :param show: Bool
        :param save: Bool
        
        :return file: imagebright   
        """
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img_conv = self.convert(image, save=True)
                img = Image.open(img_conv)
                imagename, ext = metalex.utils.get_part_file(image)
                tempname = 'img_bright_'+str(num)+ext
                enh = ImageEnhance.Brightness(img)

                if show: enh.enhance(value).show()
                elif save :
                    metalex.utils.create_temp()
                    if metalex.utils.in_dir(tempname) :
                        enh.enhance(value).save(tempname)
                        metalex.utils.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = '*'+imagename+'* is modified with bright (' +str(value)+\
                         ') > *'+tempname+'* > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        num += 1 
                    else :
                        metalex.utils.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = '*'+imagename+'* is modified with contrast (' +str(value)+\
                         ') > *'+tempname+'* > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        num += 1
                else :
                    message =  'bright(value, show=False, save=False) -->'+\
                    ' You must define one action for the current treatment : show=true or save=true '
                    metalex.logs.manageLog.write_log(message, typ='warm')
        else:
            message = 'bright(images) >> They are not images for the current treatment : input images!!' 
            metalex.logs.manageLog.write_log(message, typ='error')
                       
    def contrast_bright(self, contrast, bright, show=False, save=False):
        """Enhance image file with the contrast_bright value
          
        :param constrast: int
        :param bright: int
        :param show: Bool
        :param save: Bool
          
        :return file: imagecontrastbright   
        """
        
        if len(self.images) >= 1 :
            num = 1
            for i, image in  enumerate(self.images) :
                img_conv = self.removeColor(i, image, save=True)
                imgpil = Image.open(img_conv)
                imagename, ext = metalex.utils.get_part_file(image)
                tempname = 'img_bright_'+str(num)+ext
                enhbright = ImageEnhance.Brightness(imgpil)
                metalex.utils.create_temp()
                enhbright.enhance(bright).save(tempname)
                img2 = Image.open(tempname)
                enhconst = ImageEnhance.Contrast(img2)
                img_conv_part = metalex.utils.get_part_file(img_conv)
                img_conv_file = img_conv_part[0]+img_conv_part[1]
                if show :
                    enhconst.enhance(contrast).show()
                    metalex.utils.create_temp()
                    os.remove(tempname)
                    os.remove(img_conv_file)
                if save :
                    tempname2 = 'img_contrast_bright_'+str(num)+ext
                    metalex.utils.create_temp()
                    if metalex.utils.in_dir(tempname2) :
                        enhconst.enhance(contrast).save(tempname2)
                        os.remove(tempname)
                        os.remove(img_conv_file)
                        metalex.utils.treat_image_append(tempname2)
                        message = '*'+imagename+'* is modified with  contrast (' +str(contrast)+\
                         ') and  bright ('+str(bright)+') > '+tempname2+' > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        imgpil.close()
                        num += 1
                    else :
                        os.remove(img_conv_file)
                        os.remove(tempname)
                        metalex.utils.treat_image_append(tempname2)
                        message = '*'+imagename+'* is modified with  contrast (' +str(contrast)+\
                         ') and  bright ('+str(bright)+') > *'+tempname2+'* > Saved in dicTemp folder'  
                        metalex.logs.manageLog.write_log(message) 
                        imgpil.close()
                        num += 1
        else:
            message = 'contrastBright() >> They are not images for the current treatment : input images!!' 
            metalex.logs.manageLog.write_log(message, typ='error')  
                      
    def convert (self, img, show=False, save=False):
        """Convert image file to white/black image
        
        :param img: file
        :param show: Bool
        :param save: Bool
        
        :return file: imageconvert  
        """
        num = 1
        if len(self.images) >= 1 :
            for image in  self.images :
                img = Image.open(image)
                imagepart = metalex.utils.get_part_file(image)
                tempname = u'img_convert_'+str(num)+imagepart[1]
                if show: img.convert("L").show()
                if save:
                    metalex.utils.create_temp()
                    if metalex.utils.in_dir(tempname) :
                        img.convert("L").save(tempname)
                        return tempname
                    else: return tempname
                    
        else:
            message = u'convert() >> They are not images for the current treatment : input images!!' 
            metalex.logs.manageLog.write_log(message, typ='error')
                                           
    def filter (self, imgfilter, show=False):
        """Filter image file with specific filter value
        
        :param imgfilter: int
        :param show: Bool
          
        :return file: imagefilter  
        """
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img_conv = self.convert(image, save=True)
                img = Image.open(img_conv)
                imagename, ext = metalex.utils.get_part_file(image)
                tempname = 'img_filter_'+str(num)+ext
                metalex.utils.create_temp()
                if show: img.filter(imgfilter).show()
                elif not show and metalex.utils.in_dir(tempname) :
                    img.filter(imgfilter).save(tempname)
                metalex.utils.treat_image_append(tempname)
                message = '*'+imagename+'* is modified with  filter (' +str(imgfilter)+ ')  > *'+tempname+u'* > Saved in dicTemp folder'  
                metalex.logs.manageLog.write_log(message)
                #img.close()
                num += 1
        else:
            message = 'filter() >> They are not images for the current treatment : input images!!' 
            metalex.logs.manageLog.write_log(message, typ='error')
                                              
    def removeColor(self, i, img, show=False, save=False):
        """Remove color in image file to enhance its quality
        
        :param i: int
        :param img: file
        :param show: Bool
        :param save: Bool
          
        :return file: imageremovecolor
        """
        if img :
            imagepart = metalex.utils.get_part_file(img)
            tempname = 'img_color_remove_'+str(i)+imagepart[1]
            
            imgpil = Image.open(img)
            replace_color = (255, 255, 255)
            find_color = (0, 0, 0)
            new_image_data = []
            for color in list(imgpil.getdata()) :
                if color == find_color or color == replace_color :
                    new_image_data += [color]
                else: pass
            
            imgdir = os.path.dirname(img)
            namestore = ""
            for tep in imgdir.split('/')[:-1]: namestore += tep +"/"
            namestore = namestore+"dicTemp/"+tempname
            imgpil.putdata(new_image_data)
            if show: imgpil.show()
            if save :
                metalex.utils.create_temp()
                if metalex.utils.in_dir(tempname) : 
                    imgpil.save(tempname)
                    return namestore
                else: return namestore
        else:
            message = 'removeColor() >> They are not images for the current treatment : input images!!' 
            metalex.logs.manageLog.write_log(message, typ='error')
            
                    
