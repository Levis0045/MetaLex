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
    
    metalex test : tool for lexicographers and metalexicographers
    
    Usage :
        >>> sudo apt-get install build-essential libssl-dev libffi-dev python-dev
        >>> sudo apt-get install libtesseract-dev libleptonica-dev 
        >>> sudo apt-get install python-html5lib
        >>> sudo apt-get install python-lxml
        >>> sudo apt-get install python-bs4
        >>> sudo apt-get install tesseract-ocr-all
        >>> sudo pip install pillow
        >>> sudo pip install Cython
        >>> sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
        >>> sudo pip install termcolor
"""

import sys 

sys.path.append('..')

import metalex as dico

# ----External Modules------------------------------------------------------

import os
import glob
import ImageFilter as f
import argparse
import textwrap
from termcolor import colored

# ----Functions to run metalex in system args------------------------------------------------------

class TestMetalex:

    def run_metalex_test (self):
        
        #------------------ Argparse commands configuration -------------------------
        
        metalexArgsParser = argparse.ArgumentParser(prog='metalex',
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(colored('''
                ---------------------------------------------------------------
                | * *    * *    * * *  * * *   * *     *      * * *   **   ** |
                | *   * *  *   * *      *    * * *    *      * *        *     |
                | *        *  * * *    *   *     *   * * *  * * *  **    **   |
                ---------------------------------------------------------------
        metalex is general tool for lexicographics and metalexicographics activities
                                        
        ''', 'blue', attrs=['blink', 'bold'])),
         epilog=textwrap.dedent('''
         ------------------------------------------------------------------------------
             metalex project : special Thank to Bill for metalex-vagrant version
         ------------------------------------------------------------------------------
         '''),
         prefix_chars='-')
        
        metalexArgsParser.add_argument('-v', '--version', action='version', version='%(prog)s v0.2')
        
        metalexArgsParser.add_argument('-p', '--project',  help='Defined  %(prog)s project name', 
                            dest='projectName', action='store')
        
        metalexArgsParser.add_argument('-c', '--confproject', action='store', 
                                       help='Defined  %(prog)s configuration for the current project', 
                            dest='confProject', nargs=3, metavar=('author', 'comment', 'contributors'))
        
        metalexArgsParser.add_argument('-i', '--dicimage', dest='imageFile', action='append', nargs='?', 
                            help='Input one or multiple dictionary image(s) file(s) for current  %(prog)s project')
        
        metalexArgsParser.add_argument('-o', '--ocrtype', dest='ocrType', choices=('ocropy', 'tesserocr'), 
                                       help='OCR type to use for current  %(prog)s project', type=str)
        
        metalexArgsParser.add_argument('-m', '--model', dest='modelRef', choices=('modeldef', ''), 
                                       help='OCR LSTM model to use for current  %(prog)s project', type=str)
        
        metalexArgsParser.add_argument('-d', '--imagedir', required=True, action='store', 
                                       help='Input folder name of dictionary image files for current  %(prog)s project',
                                       type=str, dest='imagesDir')
        
        metalexArgsParser.add_argument('--imgalg', type=str, action='store', nargs=2, dest='imgalg',
                                       help='Set algorithm for enhancing dictionary image files for current'+\
                                       '  %(prog)s project (actiontype must be : contrast or bright or filter)',
                                       metavar=('actiontype', 'value'), choices=('contrast', 'bright', 'filter'))
        
        metalexArgsParser.add_argument('-r', '--filerule', dest='fileRule', type=str,
                                       help='Defined file rules that we use to enhance quality of OCR result')
        
        metalexArgsParser.add_argument('-l', '--lang', type=str, 
                                       help='Set language for optical characters recognition and others  %(prog)s treatment')
        
        metalexArgsParser.add_argument('-x', '--xml', help='Defined output result treatment of  %(prog)s',
                            type=str, nargs=1, choices=('xml', 'lmf', 'tei'))
         
        metalexArgsParser.add_argument('-s', '--save', help='Save output result of the current project in files', 
                            action='store_true')
        
        metalexArgsParser.add_argument('-t', '--terminal', help='Show  result of the current treatment in the terminal', 
                            action='store_true', default=False)
        
        
        
        # ----Build contains args------------------------------------------------
        metalexArgs = metalexArgsParser.parse_args()
        
        
        # ----Generate real path of images---------------------------------------
        imagelist = []
        
        if metalexArgs.imageFile :
            files = [cpath+x for x in metalexArgs.imageFile]
            imagelist = files
            
        elif metalexArgs.imagesDir:
            content = './'+metalexArgs.imagesDir+'/*.*'
            for imagefile in glob.glob(content) :
                name = cpath+imagefile
                imagelist.append(name)
            if len(imagelist) < 1 :   
                message = u"Your current directory don't have image(s)" 
                dico.logs.manageLog.write_log(message, typ='warm')
        else :
            message = u"You must define folder containing image of dictionary or image"+\
            u" of dictionary for your project otherwise default folder must be use" 
            dico.logs.manageLog.write_log(message, typ='warm')
            for imagefile in glob.glob('testImages/*.*') :
                name = os.getcwd()+'/'+imagefile
                imagelist.append(name)
                print(imagelist)
            if len(imagelist) < 1 :   
                message = u"Your current directory don't have image(s)" 
                dico.logs.manageLog.write_log(message, typ='warm')
                
                
        # ----Defined New project name-------------------------------------------
        if metalexArgs.projectName :
            project = dico.NewProject(metalexArgs.projectName)
        else :
            message = u"Your current project name is not set! Please correct it otherwise default name must be use" 
            project = dico.NewProject(u'metalex_projectName')
            dico.logs.manageLog.write_log(message, typ='warm')
            
            
        # ----Set metadata for the current project-------------------------------
        if metalexArgs.confProject :
            author, comment, contrib = metalexArgs.confProject[0], metalexArgs.confProject[1], metalexArgs.confProject[2]
            project.set_conf_project(author, comment, contrib)
        else :
            message = u'Please set metadata for the current project. Default metadata data must be apply' 
            dico.logs.manageLog.write_log(message, typ='error')
            project.set_conf_project(u'metalex_user', u'Comment_user', u'metalex_contributors')
            
       
        # ----Input dictionary images to project---------------------------------
        images  = project.metalex.get_images(imagelist)
              
            
        # ----Enhance quality  and Start optical recognition of dictionary image files----------------
        model = ''
        if metalexArgs.modelRef: model = metalexArgs.modelRef
            
            
        if metalexArgs.save and metalexArgs.lang :
            execOcr = images.run_img_to_text(typ=metalexArgs.ocrType, save=True, 
                                             langIn=metalexArgs.lang)
            
            if metalexArgs.imgalg :
                actionType, value = metalexArgs.imgalg
                if actionType == 'contrast' :
                    execOcr.enhance_img_quality(typ='contrast', value=value)
                elif actionType == 'bright' :
                    execOcr.enhance_img_quality(typ='bright', value=value)
                elif actionType == 'filter' :
                    execOcr.enhance_img_quality(typ='filter')
                else :
                    message = u"Your input string 'actiontype' don't match (constrat or bright or filter)" 
                    dico.logs.manageLog.write_log(message, typ='warm')
            else:    
                execOcr.enhance_img(typ='filter')
            
        elif metalexArgs.lang :
            execOcr = images.run_img_to_text(typ=metalexArgs.ocrType, save=False, 
                                             langIn=metalexArgs.lang)
            execOcr.run_ocr(model)
        elif metalexArgs.terminal and metalexArgs.lang :
            execOcr = images.run_img_to_text(typ=metalexArgs.ocrType, save=False, 
                                             langIn=metalexArgs.lang)
            execOcr.run_ocr(model)
        else :
            execOcr = images.run_img_to_text(typ=metalexArgs.ocrType, save=True, 
                                             langIn='fra')
            execOcr.run_ocr(model)
        
        # ----Normalize result of ocr files ------------------------------------
        if metalexArgs.fileRule :
            execNormalize = images.BuildTextWell(metalexArgs.fileRule)
            execNormalize.make_text_well()
        else :
            message = u"FileRule() >> You don't defined file rules for this project. *file_Rule.dic* will be used instead" 
            execNormalize = images.BuildTextWell(u'../../file_Rule.dic')
            dico.logs.manageLog.write_log(message, typ='warm')
            execNormalize.make_text_well()
        
        #-----Produce HTML output file for project------------------------------
        if metalexArgs.save :
            images.dico_html(save=metalexArgs.save)
            baliseXML = images.BaliseXML()
            if metalexArgs.xml :
                baliseXML.put_xml(save=metalexArgs.save, typ=metalexArgs.xml)
        else :
            images.dico_html(save=False)
    
    
    
#------------RUN FUNCTION-----------------------------------------------

def run_metalex():
    test = TestMetalex()
    test.run_metalex_test()
    
    
#------------RUN APPLICATION-----------------------------------------------

if __name__ == '__main__':
    run_metalex()
    