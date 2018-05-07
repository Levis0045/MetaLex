#!/usr/bin/env python
# coding: utf8

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

"""metalex is general tool for lexicographic and metalexicographic activities

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

Contact: levismboning@yahoo.fr

---------------------------------------------------------------------------

ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing


Usage:
    >>> import metalex as dico
    >>> projet = dico.newProject('LarousseMemoire')
     
"""

# ----External Modules------------------------------------------------------

import os
import codecs
import re
import pickle
import sys
from termcolor import colored
from datetime import datetime
import utilspie
from utilspie import iterutils

# ----Internal Modules------------------------------------------------------

import metalex

# -----Exported Functions---------------------------------------------------

__all__ = ['NewProject']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------
       
        
class NewProject:
    """Create new environment project and its configuration
    
    :param projectname: str
    
    :return new environment project
    """
    
    import metalex
        
    def __init__ (self, projectname):
        self.name = projectname
        metalex.allProjectNames.append(self.name)
        metalex.projectName = self.name
        self.fileImages = []
        self.resultOcr = u""
        self.resultText = u""
        self.resultXmlised = u""
        self.resultLog = u""
        self.lang = u""
        self.dicoType = u""
        self.project_folder()
        print('\n %s %s %s \n\n' %('---', colored('Part 0 : Build project', 
                                    attrs=['bold']), '--'*18))

        
    def project_folder(self):
        """Create folder of new environment project
        
        :return project folder
        """
        folderName = 'metalex_'+self.name
        metalex.projectFolder[folderName] = os.getcwd()
        currentdir = os.listdir('.')
        if folderName in currentdir: os.chdir(folderName)
        else:
            try: 
                os.mkdir(folderName)
                os.chdir(folderName)
            except os.error:
                message =  u"We can can't create "+folderName+u" folder in this directory ! It is right exception ?"
                metalex.logs.manageLog.write_log(message, typ='error')
                  
    def set_conf_project (self, author, comment, contrib):
        """Set parameters of new environment project
        
        :param author: str
        :param comment: str
        :param contrib: str
        
        :return file: normalize file path
        """
        metalex.projectAuthor = author
        projectF = metalex.projectFolder.items()[0][0]
        projectD = metalex.projectFolder.items()[0][1]
        acessDF  = projectF+' | '+projectD
        project  = metalex.projectName
        Cdate    = metalex.logs.manageLog.get_date()
        Ctime    = metalex.utils.get_hour()
        dateInit = Cdate.decode('ascii')+' à '+Ctime
        log      = '/logs'+' | '+projectD+'/'+projectF+'/logs'
        temp     = '/dicTemp'+' | '+projectD+'/'+projectF+'/dicTemp'
        images   = '/dicImages'+' | '+projectD+'/'+projectF+'/dicImages'
        Intro    = '***************** metalex project configuration *****************\n\n'
        access   = '%-15s: %-10s \n' %('\Project folder', acessDF)
        end      = '***************************************************************** \n\n'
   
        os.chdir(metalex.utils.get_root_project())
        contentdir = os.listdir('.')
        if 'metalex.cnf' not in contentdir:
            with codecs.open('metalex.cnf', 'w', 'utf-8') as conf:
                conf.write(Intro)
                conf.write(access)
                conf.write('%-15s: %-10s \n'   %('\Project name', project))
                conf.write('%-15s: %-10s \n'   %('\Creation date', dateInit))
                conf.write('%-15s: %-10s \n'   %('\Author', author))
                conf.write('%-15s: %-10s \n'   %('\Contributors', contrib))
                conf.write('%-15s: %-10s \n'   %('\Comment', comment))
                conf.write('%-15s: %-10s \n'   %('\Folder log', log))
                conf.write('%-15s: %-10s \n'   %('\Folder temp', temp))
                conf.write('%-15s: %-10s \n\n' %('\Folder images', images))
                conf.write(end)
                
    def get_project_name(self): return metalex.projectName 

    def get_file_images (self):
        if (len(metalex.fileImages)>= 1):
            self.fileImages = metalex.fileImages
            return self.fileImages
    
    def get_treat_images (self):
        if (len(metalex.ocrtext.fileImages)>= 1):
            self.treatImageFile  = metalex.ocrtext.treatImageFile 
            return self.treatImageFile 
    
    def get_text_ocr (self):
        if (metalex.ocrtext.textOcr):
            self.resultOcr += metalex.ocrtext.textOcr
            return self.resultOcr
        
    def get_ocr_text (self): return metalex.ocrtext.makeOcr

       
        
   
