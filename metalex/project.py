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
from termcolor import colored

# ----Internal Modules------------------------------------------------------

import metalex

# -----Exported Functions---------------------------------------------------

__all__ = ['create_temp', 'NewProject', 'treat_image_append', 'get_part_file', 
           'in_dir', 'write_temp_file', 'read_temp_file', 'save_normalized_data']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

        
def get_part_file(namefile):
    """Extract file image name and file image extension
    
    :param namefile: str
    
    :return list: (imageroot, ext)
    """
    (imageroot, ext) = os.path.splitext(os.path.basename(namefile))
    return (imageroot, ext)


def save_normalized_data(name, typ, form=None, data=None):
    """Saved normalized text in text format (*.art) or in pickle format (*.pickle) 
    
    :param name: str file
    :param typ: str
    
    :return file: texts extracted
    """
    dicArticles = []
    if data:
        for k, v in data.items():
            result = {k:v}
            dicArticles.append(result)
    else: dicArticles = read_temp_file(form)
        
    create_temp()
    if typ == 'text':
        if in_dir(name):
            with codecs.open(name, 'a', 'utf-8') as fil:
                num = 1
                for art in dicArticles:
                    for k, v in art.items():
                        if k != 'article_1': fil.write('%10s: %s\n' %(k, v))
                        else:
                            if not data: fil.write('\n----- FILE: %s ---------------------------------------------------------------------------------\n\n' %num)
                            fil.write('%10s: %s\n' %(k, v))
                            num += 1
            message = 'save_normalize() >> '+'*'+name+'* is created and contain all text format data from html files > Saved in dicTemp folder'  
            metalex.logs.manageLog.write_log(message) 
        else:
            message = 'save_normalize() >> '+'*'+name+'* is created and contain all text format data from html files > Saved in dicTemp folder'  
            metalex.logs.manageLog.write_log(message) 
    
    if typ == 'pickle':  
        if in_dir(name) and file_pickle(dicArticles, name):
            message = 'save_normalize() >> '+'*'+name+'* is created and contain pickle data object from html files > Saved in dicTemp folder'  
            metalex.logs.manageLog.write_log(message)         
        else:
            message = 'save_normalize() >> '+'*'+name+'* is created and contain pickle data object from html files > Saved in dicTemp folder'  
            metalex.logs.manageLog.write_log(message)    
            

def get_hour():
    """Get the current system time 
    
    :return str: hour
    """
    datefile = os.popen('date').read()
    try:
        datetab = datefile.split(',')[1].split(' ')
        hour = datetab[1]
        return hour
    except:
        datetab = datefile.split(' ')[3]
        hour = datetab
        return hour
    
    
def write_temp_file(path, typ):
    """Append result path of files to 'save.txt' temporaly file
      
    :param path: str path of file
    
    :return ...
    """
    create_temp()
    if typ == 'ocr':
        with codecs.open('temp_ocr.txt', 'a', 'utf-8') as s:
            s.write('%s\n' %path)
    elif typ == 'norm':
        with codecs.open('temp_norm.txt', 'a', 'utf-8') as s:
            s.write('%s\n' %path)


def read_temp_file(typ):
    """Append image result files to 'save.txt' temporaly file
      
    :param path: str path of file
    
    :return ...
    """
    create_temp()
    result = []
    if typ == 'ocr':
        with codecs.open('temp_ocr.txt', 'r', 'utf-8') as s:
            for line in s: treat_ocr_append(line.strip())
        os.remove('temp_ocr.txt')
    elif typ == 'norm': 
        with codecs.open('temp_norm.txt', 'r', 'utf-8') as s:
            for line in s:
                part = line.split('==')
                resultTemp = {part[0]:part[1]}
                result.append(resultTemp)
        return result
    
        
        
def treat_image_append(namefile):
    """Append image result files to the global variable at the scope
      
    :param namefile: str
    
    :return ...
    """
    tempnameLocation =  os.getcwd()+'/'+namefile
    metalex.treatImages.append(tempnameLocation)


def treat_ocr_append(namefile):
    """Append ocr result files to the global variable
    
    :param namefile: str
    
    :return ...
    """
    parentdir = os.listdir('..')
    if 'logs' in parentdir:
        os.chdir('../dicTemp')
        tempnameLocation =  os.getcwd()+'/'+namefile
        metalex.resultOcrFiles.append(tempnameLocation)
    else:
        tempnameLocation =  os.getcwd()+'/'+namefile
        metalex.resultOcrFiles.append(tempnameLocation)
     
     
def in_dir(fil):
    """Verify if an input file is in a 'dicTemp' folder 
    
    :return Bool
    """
    currentdir = os.listdir('.')
    if fil in currentdir:
        return False
    else:
        return True


def name_file(tab, ext):
    """Generate name file to saved result of articles extraction  
    
    :param tab: array
    :param ext: str
      
    :return str: namepickle 
    """
    name  = str(tab[0]).split('/')[-1].split(',')[0].split('_')[:-1]
    if ext == '.art':
        nametxt    = 'articles_'+'_'.join(name)+'.art'
        return nametxt
    elif ext == '.pickle':
        namepickle = 'articles_'+'_'.join(name)+'.pickle'
        return namepickle
        

def file_pickle(data, name):
    """Create pickle file of the articles data
    
    :param data: dictionary
    :param name: str
    
    :return Bool: True 
    """
    with codecs.open(name, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return True
    
    
def file_unpickle(fil):
    """Unpack pickle file of articles data
    
    :param fil: str
    
    :return dict: data articles object
    """
    with codecs.open(fil, 'rb') as f:
        data = pickle.load(f)
        return data 


def file_get_text(fil):
    """Extract articles data into file text
    
    :return dict: data articles text
    """
    datatext = {}
    with codecs.open(fil, 'r', 'utf-8') as f:
        for line in f:
            if re.search(r'article_', line):
                partline = line.split(':')
                datatext[partline[0].strip()] = partline[1].strip()
    return datatext


def get_root_project():
    """Go to the root path of current project
    
    :return root path of current project
    """
    projectF = metalex.projectFolder.items()[0][0]
    projectD = metalex.projectFolder.items()[0][1]
    projetPath = projectD+'/'+projectF
    return projetPath


def read_conf():
    """Extract data configuration of the project
    
    :return dict: data configuration text
    """
    confData = {}
    rootPath = get_root_project()
    confPath = rootPath+'/metalex.cnf'
    with codecs.open(confPath, 'r', 'utf-8') as conf:
        for line in conf:
            if line[0] == '\\': 
                part  = line.strip().split(':')
                title = part[0][1:].replace(' ', '')
                val   = part[1]
                confData[title] = val
    return confData
        
        
def create_temp():
    """Create a 'dicTemp' folder if it doesn't exist at the parent folder at the scope
    
    :return path: place in dicTemp folder
    """
    parentdir = os.listdir('..')
    projectF = metalex.projectFolder.items()[0][0]
    projectD = metalex.projectFolder.items()[0][1]
    rootProject = projectD+'/'+projectF
    dicTemp = rootProject+'/dicTemp'
    contentdir = os.listdir(rootProject)
    if 'dicTemp' not in contentdir:
        try:
            os.mkdir(dicTemp)
        except os.error:
            message = 'We can cannot create dicTemp folder in this directory ! It s right exception ?'
            metalex.logs.manageLog.write_log(message, typ='error')
            pass
        message = 'dicTemp folder >> is created an initialised with' 
        metalex.logs.manageLog.write_log(message)
        os.chdir(dicTemp)
    else:
        os.chdir(dicTemp) 
        

def dic_file(fil):
    """Take the current script path and join it to file path
    
    :param fil: str
    
    :return path: normalize file path
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, fil)
       
        
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
        print('\n %s %s %s \n\n' %('--', colored('Part 0: New project', attrs=['bold']), '--'*20))

        
    def project_folder(self):
        """Create folder of new environment project
        
        :return project folder
        """
        folderName = 'metalex_'+self.name
        metalex.projectFolder[folderName] = os.getcwd()
        currentdir = os.listdir('.')
        if folderName in currentdir:
            os.chdir(folderName)
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
        Ctime    = get_hour()
        dateInit = Cdate.decode('ascii')+' à '+Ctime
        log      = '/logs'+' | '+projectD+'/'+projectF+'/logs'
        temp     = '/dicTemp'+' | '+projectD+'/'+projectF+'/dicTemp'
        images   = '/dicImages'+' | '+projectD+'/'+projectF+'/dicImages'
        Intro    = '***************** metalex project configuration *****************\n\n'
        access   = '%-15s: %-10s \n' %('\Project folder', acessDF)
        end      = '***************************************************************** \n\n'
   
        os.chdir(get_root_project())
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

       
        
   
