#! usr/bin/env python
# coding: utf8

"""
    MetaLex-vagrant test : tool for metalexicographers
    
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

# Do this if MetaLex folder is in the parent of the current folder

#import sys
#sys.path.append('..')


#-----If MetaLex is in the same file, import MetaLex------------------------

import MetaLex as dico

# ----External Modules------------------------------------------------------

import ImageFilter as f
import os, glob
import argparse, textwrap 
from termcolor import colored

# ----Functions to run MetaLex in system args------------------------------------------------------

class parseM():
    pass

def run_MetaLex_test ():
    
    #------------------ Argparse commands configuration -------------------------
    
    MetaLexArgsParser = argparse.ArgumentParser(prog='MetaLex',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(colored('''
            ---------------------------------------------------------------
            | * *    * *    * * *  * * *   * *     *      * * *   **   ** |
            | *   * *  *   * *      *    * * *    *      * *        *     |
            | *        *  * * *    *   *     *   * * *  * * *  **    **   |
            ---------------------------------------------------------------
    MetaLex is general tool for lexicographics and metalexicographics activities
                                    
                                    ''', 'blue', attrs=['blink', 'bold'])),
                                     epilog=textwrap.dedent('''
                                     ------------------------------------------------------------------------------
                                         MetaLex project : special Thank to Bill for MetaLex-vagrant version
                                     ------------------------------------------------------------------------------
                                     '''),
                                     prefix_chars='-')
    
    MetaLexArgsParser.add_argument('-v', '--version', action='version', version='%(prog)s v0.2')
    MetaLexArgsParser.add_argument('-p', '--project',  help='Defined  %(prog)s project name', 
                        dest='projectName', action='store', required=True)
    MetaLexArgsParser.add_argument('-c', '--confproject', action='store', help='Defined  %(prog)s configuration for the current project', 
                        dest='confProject', required=True, nargs=3, metavar=('author', 'comment', 'contributors'))
    MetaLexArgsParser.add_argument('-i', '--dicimage', dest='imageFile', action='append', nargs='?', 
                        help='Input one or multiple dictionary image(s) file(s) for current  %(prog)s project')
    MetaLexArgsParser.add_argument('-d', '--imagedir', help='Input folder name of dictionary image files for current  %(prog)s project',
                        type=str, required=True, action='store', dest='imagesDir')
    MetaLexArgsParser.add_argument('-r', '--filerule', dest='fileRule', type=str, required=True)
    MetaLexArgsParser.add_argument('-l', '--lang', help='Set language for optical characters recognition and others  %(prog)s treatment',
                        type=str, required=True, )
    MetaLexArgsParser.add_argument('-s', '--save', help='Save output result of the current project in files', 
                        action='store_true')
    MetaLexArgsParser.add_argument('-t', '--terminal', help='Show  result of the current treatment in the terminal', 
                        action='store_true', default=False)
    """
    subparsers = MetaLexArgsParser.add_subparsers(title='MetaLex subcommands', help='sub-commands for specific MetaLex treatment')
    
    parser_ocr = subparsers.add_parser('dicOcrText', help='Plugin for optical recognition character and normalization')
    parser_ocr.add_argument('-s', '--save', type=str, help='Plugin for optical recognition character and normalization')
    
    parser_xml = subparsers.add_parser('dicXmlised', help='Plugin for xml and html file generator')
    parser_xml.add_argument('-s', '--save', type=str, help='bar help')
    
    #MetaLexArgsParser.print_help()
    """
    
    # ----Build contains args------------------------------------------------
    MetaLexArgs = MetaLexArgsParser.parse_args()
    
    
    # ----Generate real path of images---------------------------------------
    imagelist = []
    if MetaLexArgs.imageFile :
        imagelist.append(MetaLexArgs.imageFile)
            
    if MetaLexArgs.imagesDir:
        content = './'+MetaLexArgs.imagesDir+'/*.jpg'
        for imagefile in glob.glob(content) :
            name = os.getcwd()+'/'+imagefile
            imagelist.append(name)
            
            
    # ----Defined New project name-------------------------------------------
    if MetaLexArgs.projectName :
        project = dico.newProject(MetaLexArgs.projectName)
    else :
        project = dico.newProject(u'MetaLex_projectName')
        
    # ----Set metadata for the current project-------------------------------
    if MetaLexArgs.confProject :
        author, comment, contrib = MetaLexArgs.confProject[0], MetaLexArgs.confProject[1], MetaLexArgs.confProject[2]
        project.setConfProject(author, comment, contrib)
    else :
        hour = dico.dicProject.getHour() 
        log = u'[MetaLexLog - '+hour+u']'
        message = u'Error : please set metadata for the current project. default name data must be apply' 
        print u'\n%-10s  %-30s %s \n' %(colored(log, u'red', attrs=['reverse', 'blink', 'bold']), message)
        project.setConfProject(u'MetaLex_user', u'Comment_user', u'MetaLex_contributors')
        
   
    # ----Input dictionary images to project---------------------------------
    images  = project.MetaLex.getImages(imagelist)
    
    # ----Enhance quality of dictionary image files -------------------------
    images.enhanceImages().filter(f.DETAIL)
    
    # ----Start optical recognition of dictionary image files----------------
    if MetaLexArgs.save and MetaLexArgs.lang :
        images.imageToText(save=True, langIn=MetaLexArgs.lang)
    elif MetaLexArgs.lang :
        images.imageToText(save=False, langIn=MetaLexArgs.lang)
    elif MetaLexArgs.terminal and MetaLexArgs.lang :
        images.imageToText(show=True, langIn=MetaLexArgs.lang)
    else :
        images.imageToText(save=True, langIn='fra')
    
    # ----Normalize result of ocr files ------------------------------------
    if MetaLexArgs.fileRule :
        images.makeTextWell(MetaLexArgs.fileRule)
    else :
        images.makeTextWell(u'file_Rule.dic')
    
    #-----Produce HTML output file for project------------------------------
    if MetaLexArgs.save :
        images.dicoHtml(save=MetaLexArgs.save)
    else :
        images.dicoHtml(save=False)



#------------RUN APPLICATION-----------------------------------------------

if __name__ == '__main__':
    run_MetaLex_test()