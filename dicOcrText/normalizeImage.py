#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
    Normalization tool for images.
 
    Package:
        >>> pip install pillow
    
    Usage:
        >>> import MetaLex as dico
        >>> import ImageFilter
        >>> project = dico.newProject(project_name)
        >>> images = project.MetaLex.getImages(imagelist)
        >>> images.enhanceImages().filter(f.DETAIL)
        >>> images.enhanceImages().bright(1, save=True)
    
    ImageFilter.filters:
        'BLUR', 'BuiltinFilter', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 
        'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'Filter', 
        'GaussianBlur', 'Kernel', 'MaxFilter', 'MedianFilter', 
        'MinFilter', 'ModeFilter', 'RankFilter', 
        'SHARPEN', 'SMOOTH', 'SMOOTH_MORE', 'UnsharpMask'
          
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import Image, os
import ImageEnhance
from shutil import copyfile

# ----Exported Functions-----------------------------------------------------

__all__ = ['getImages', 'enhanceImages']

# ----------------------------------------------------------


def getImages(images):
    """
        Take input image list and save it in the scope
        @param   images:file
        @return: file:images 
    """
    
    if len(images) >= 1 :
        num = 1
        for image in images : 
            exts = (u'.png', u'.jpg', u'.JPG', u'.jpeg', u'.PNG', u'.JPEG', u'.tif', u'.gif')
            imageroot, ext = MetaLex.dicProject.get_part_file(image)
            if os.path.isfile(image) and ext in exts:
                imagedir = os.path.dirname(image)
                
                imagedirNew = u""
                for tep in imagedir.split('/')[:-1] :
                    imagedirNew += tep +u"/"
                imagedirNew = imagedirNew+u"dicImages/"
                
                if not os.path.exists(imagedirNew) :
                    os.mkdir(imagedirNew)
                    
                imagefileNew     = u"dic_image_"+str(num)+ext
                imageLocationNew =  imagedirNew+imagefileNew
                copyfile(image, imageLocationNew)
                MetaLex.fileImages.append(imageLocationNew)
                num += 1
            else :
                message = u"getImages(images) >> The input image '"+imageroot+ext+u"' is not a file image"
                MetaLex.dicLog.manageLog.writelog(message, typ='error')
                 
        imagestr = str(images)
        message  = imagestr + u' > are append for the current treatment' 
        MetaLex.dicLog.manageLog.writelog(message)
    else: 
        message = u'getImages(images) >> They are not images for the current treatment : input images !!' 
        MetaLex.dicLog.manageLog.writelog(message, typ='error')
        
    return MetaLex
    
        
   
class enhanceImages ():
    """
      This Class enhance image file and save them to 'dicTemp'
      @param   fileImages:file
      @return: inst object 
    """
    
    def __init__(self): 
        self.images = MetaLex.fileImages
        
    def contrast(self, value, show=False, save=False):
        """
          Enhance image file with the contrast value
          @param   value:int
          @param   show:Bool
          @param   save:Bool
          @return: file:imagecontrast   
        """
        
        if self.images >= 1 : 
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = MetaLex.dicProject.get_part_file(image)
                tempname = u'img_contrast_'+str(num)+ext
                enh = ImageEnhance.Contrast(img)
                
                if show :
                    enh.enhance(value).show()
                elif save :
                    MetaLex.dicProject.createtemp()
                    if MetaLex.dicProject.inDir(tempname) :
                        enh.enhance(value).save(tempname)
                        MetaLex.dicProject.treat_image_append(tempname)
                        message = imagename + u'is modified with contrast (' +str(value)+ u') > '+tempname+u' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        num += 1
                    else :
                        MetaLex.dicProject.treat_image_append(tempname)
                        message = imagename + u'is modified with contrast (' +str(value)+ u') > '+tempname+u' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        num += 1
                else :
                    message = u'contrast(value, show=False, save=False) --> You must define one action for the current treatment : show=true or save=true '
                    MetaLex.dicLog.manageLog.writelog(message, typ='warm')
        else:
            message = u'contrast(images) >> They are not images for the current treatment : please input images !! ' 
            MetaLex.dicLog.manageLog.writelog(message, typ='error')
            
            
    def sharp(self, value, show=False, save=False):
        """
          Enhance image file with the sharp value
          @param   value:int
          @param   show:Bool
          @param   save:Bool
          @return: file:imagesharp   
        """
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img_conv = self.convert(image, save=True)
                img = Image.open(img_conv)
                imagename, ext = MetaLex.dicProject.get_part_file(image)
                tempname = u'img_sharp_'+str(num)+ext
                enh = ImageEnhance.Sharpness(img)

                if show :
                    enh.enhance(value).show()
                elif save :
                    MetaLex.dicProject.createtemp()
                    if MetaLex.dicProject.inDir(tempname) :
                        enh.enhance(value).save(tempname)
                        MetaLex.dicProject.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = imagename + u'is modified with sharp ( ' +str(value)+ ') > '+tempname+' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        num += 1 
                    else :
                        MetaLex.dicProject.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = imagename + u'is modified with contrast (' +str(value)+ u') > '+tempname+u' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        num += 1
                else :
                    message = u'Warning : sharp(value, show=False, save=False) --> You must define one action for the current treatment : show=true or save=true'
                    MetaLex.dicLog.manageLog.writelog(message, typ='warm')
        else:
            message = u'sharp(images) >> They are not images for the current treatment : please input images !! ' 
            MetaLex.dicLog.manageLog.writelog(message, typ='error')
            
            
    def bright(self, value, show=False, save=False):
        """
          Enhance image file with the bright value
          @param   value:int
          @param   show:Bool
          @param   save:Bool
          @return: file:imagebright   
        """
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img_conv = self.convert(image, save=True)
                img = Image.open(img_conv)
                imagename, ext = MetaLex.dicProject.get_part_file(image)
                tempname = u'img_bright_'+str(num)+ext
                enh = ImageEnhance.Brightness(img)

                if show :
                    enh.enhance(value).show()
                elif save :
                    MetaLex.dicProject.createtemp()
                    if MetaLex.dicProject.inDir(tempname) :
                        enh.enhance(value).save(tempname)
                        MetaLex.dicProject.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = imagename + u' is modified with bright (' +str(value)+ ') > '+tempname+' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        num += 1 
                    else :
                        MetaLex.dicProject.treat_image_append(tempname)
                        os.remove(img_conv)
                        message = imagename + u' is modified with contrast (' +str(value)+ u') > '+tempname+u' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        num += 1
                else :
                    message =  u'bright(value, show=False, save=False) --> You must define one action for the current treatment : show=true or save=true '
                    MetaLex.dicLog.manageLog.writelog(message, typ='warm')
        else:
            message = u'bright(images) >> They are not images for the current treatment : input images!!' 
            MetaLex.dicLog.manageLog.writelog(message, typ='error')
            
            
    def contrastBright(self, contrast, bright, show=False, save=False):
        """
          Enhance image file with the contrastBright value
          @param   constrast:int
          @param   bright:int
          @param   show:Bool
          @param   save:Bool
          @return: file:imagecontrastbright   
        """
        
        if len(self.images) >= 1 :
            num = 1
            for i, image in  enumerate(self.images) :
                img_conv = self.removeColor(i, image, save=True)
                imgpil = Image.open(img_conv)
                imagename, ext = MetaLex.dicProject.get_part_file(image)
                tempname = u'img_bright_'+str(num)+ext
                enhbright = ImageEnhance.Brightness(imgpil)
                MetaLex.dicProject.createtemp()
                enhbright.enhance(bright).save(tempname)
                img2 = Image.open(tempname)
                enhconst = ImageEnhance.Contrast(img2)
                img_conv_part = MetaLex.dicProject.get_part_file(img_conv)
                img_conv_file = img_conv_part[0]+img_conv_part[1]
                if show :
                    enhconst.enhance(contrast).show()
                    MetaLex.dicProject.createtemp()
                    os.remove(tempname)
                    os.remove(img_conv_file)
                if save :
                    tempname2 = u'img_contrast_bright_'+str(num)+ext
                    MetaLex.dicProject.createtemp()
                    if MetaLex.dicProject.inDir(tempname2) :
                        enhconst.enhance(contrast).save(tempname2)
                        os.remove(tempname)
                        os.remove(img_conv_file)
                        MetaLex.dicProject.treat_image_append(tempname2)
                        message = imagename + u' is modified with  contrast (' +str(contrast)+ ') and  bright ('+str(bright)+') > '+tempname2+' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        imgpil.close()
                        num += 1
                    else :
                        os.remove(img_conv_file)
                        os.remove(tempname)
                        MetaLex.dicProject.treat_image_append(tempname2)
                        message = imagename + u' is modified with  contrast (' +str(contrast)+ ') and  bright ('+str(bright)+') > '+tempname2+' > Saved in dicTemp folder'  
                        MetaLex.dicLog.manageLog.writelog(message) 
                        imgpil.close()
                        num += 1
        else:
            message = u'contrastBright() >> They are not images for the current treatment : input images!!' 
            MetaLex.dicLog.manageLog.writelog(message, typ='error')  
            
           
    def convert (self, img, show=False, save=False):
        """
          Convert image file to white/black image
          @param   img:file
          @param   show:Bool
          @param   save:Bool
          @return: file:imageconvert  
        """
        num = 1
        if len(self.images) >= 1 :
            for image in  self.images :
                img = Image.open(image)
                imagepart = MetaLex.dicProject.get_part_file(image)
                tempname = u'img_convert_'+str(num)+imagepart[1]
                if show : 
                    img.convert("L").show()
                if save :
                    MetaLex.dicProject.createtemp()
                    if MetaLex.dicProject.inDir(tempname) :
                        img.convert("L").save(tempname)
                        return tempname
                    else: 
                        return tempname
                    
        else:
            message = u'convert() >> They are not images for the current treatment : input images!!' 
            MetaLex.dicLog.manageLog.writelog(message, typ='error')
            
                  
                
    def filter (self, imgfilter, show=False):
        """
          Filter image file with specific filter value
          @param   imgfilter:int
          @param   show:Bool
          @return: file:imagefilter  
        """
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img_conv = self.convert(image, save=True)
                img = Image.open(img_conv)
                imagename, ext = MetaLex.dicProject.get_part_file(image)
                tempname = u'img_filter_'+str(num)+ext
                MetaLex.dicProject.createtemp()
                if show :
                    img.filter(imgfilter).show()
                elif not show and MetaLex.dicProject.inDir(tempname) :
                    img.filter(imgfilter).save(tempname)
                MetaLex.dicProject.treat_image_append(tempname)
                message = imagename + u' is modified with  filter (' +str(imgfilter)+ u')  > '+tempname+u' > Saved in dicTemp folder'  
                MetaLex.dicLog.manageLog.writelog(message)
                img.close()
                num += 1
        else:
            message = u'filter() >> They are not images for the current treatment : input images!!' 
            MetaLex.dicLog.manageLog.writelog(message, typ='error')
            
                    
                
    def removeColor(self, i, img, show=False, save=False):
        """
          Remove color in image file to enhance its quality
          @param   i:int
          @param   img:file
          @param   show:Bool
          @param   save:Bool
          @return: file:imageremovecolor
        """
        
        if img :
            imagepart = MetaLex.dicProject.get_part_file(img)
            tempname = u'img_color_remove_'+str(i)+imagepart[1]
            
            imgpil = Image.open(img)
            replace_color = (255, 255, 255)
            find_color = (0, 0, 0)
            new_image_data = []
            for color in list(imgpil.getdata()) :
                if color == find_color or color == replace_color :
                    new_image_data += [color]
                else:
                    pass
            
            imgdir = os.path.dirname(img)
            namestore = u""
            for tep in imgdir.split('/')[:-1] :
                namestore += tep +u"/"
            namestore = namestore+u"dicTemp/"+tempname
            imgpil.putdata(new_image_data)
            if show :
                imgpil.show()
            if save :
                MetaLex.dicProject.createtemp()
                if MetaLex.dicProject.inDir(tempname) : 
                    imgpil.save(tempname)
                    return namestore
                else :
                    return namestore
        else:
            message = u'removeColor() >> They are not images for the current treatment : input images!!' 
            MetaLex.dicLog.manageLog.writelog(message, typ='error')
            
                    
