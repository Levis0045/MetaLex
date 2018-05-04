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
from utilspie import iterutils
import multiprocessing


# ----Internal Modules------------------------------------------------------

import metalex

# -----Exported Functions---------------------------------------------------

__all__ = ['create_temp', 'treat_image_append', 'get_part_file', 'in_dir',
            'write_temp_file', 'read_temp_file', 'save_normalized_data', 
           'ocropy_command', 'calculate_process']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

def calculate_process():
    """Calculate a number of processes useful for OCR processing

    :return int: number of processes
    """
    processExec = 1
    try: processExec = multiprocessing.cpu_count()
    except: 
        import psutil
        processExec = psutil.cpu_count()
    return processExec

def ocropy_command(typ, param):
    """Command to execute to the terminal
    
    :param typ: ocropy function arg
    :param param: parameters of ocropy function arg
    
    :return execution for command
    """
    version = py_version()
    if typ == 'edit':
        command = version+' '+metalex.plugins.ocropy.ocropusGtedit+' '+param
        return os.system(command)
    elif typ == 'rpred':
        command = version+' '+metalex.plugins.ocropy.ocropusRpred+' '+param
        return os.system(command)
    elif typ == 'lpred':
        command = version+' '+metalex.plugins.ocropy.ocropusLpred+' '+param
        return os.system(command)
    elif typ == 'rtrain':
        command = version+' '+metalex.plugins.ocropy.ocropusRtrain+' '+param
        return os.system(command)
    elif typ == 'nlbin':
        command = version+' '+metalex.plugins.ocropy.ocropusNlbin+' '+param
        return os.system(command)
    elif typ == 'visual':
        command = version+' '+metalex.plugins.ocropy.ocropusVisualizeResults+' '+param
        return os.system(command)
    elif typ == 'hocr':
        command = version+' '+metalex.plugins.ocropy.ocropusHocr+' '+param
        return os.system(command)
    elif typ == 'pageseg':
        command = version+' '+metalex.plugins.ocropy.ocropusGpageseg+' '+param
        return os.system(command)
    elif typ == 'error':
        command = version+' '+metalex.plugins.ocropy.ocropusErrs+' '+param
        return os.system(command)
    elif typ == 'cnferror':
        command = version+' '+metalex.plugins.ocropy.ocropusCnfErrs+' '+param
        return os.system(command)
    elif typ == 'linegen':
        command = version+' '+metalex.plugins.ocropy.ocropusLinegen+' '+param
        return os.system(command)
     
def py_version():
    version = sys.version_info[:2]
    if version[0] == 2:
        return('python')
    elif version[0] == 3:
        return('python3')
                     
def get_part_file(namefile):
    """Extract file image name and file image extension
    
    :param namefile: str
    
    :return list: (imageroot, ext)
    """
    if type(namefile) is list: namefile = os.path.abspath(namefile[0])
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
    
    img = '* is created and contain pickle data object from html files > Saved in dicTemp folder' 
    create_temp()
    if typ == 'text':
        if in_dir(name):
            with codecs.open(name, 'a', 'utf-8') as fil:
                num = 1
                for art in dicArticles:
                    for k, v in art.items():
                        if k != 'article_1': fil.write('%10s: %s\n' %(k, v))
                        else:
                            if not data: fil.write('\n----- FILE: %s %s \n\n' %(num, '--'*20))
                            fil.write('%10s: %s\n' %(k, v))
                            num += 1
            message = 'save_normalize() >> '+'*'+name+img  
            metalex.logs.manageLog.write_log(message) 
        else:
            message = 'save_normalize() >> '+'*'+name+img
            metalex.logs.manageLog.write_log(message) 
    
    if typ == 'pickle':  
        if in_dir(name) and file_pickle(dicArticles, name):
            message = 'save_normalize() >> '+'*'+name+img
            metalex.logs.manageLog.write_log(message)         
        else:
            message = 'save_normalize() >> '+'*'+name+img 
            metalex.logs.manageLog.write_log(message)    
            
def get_hour():
    """Get the current system time 
    
    :return str: hour
    """
    date_time = datetime.now().isoformat()
    hour = date_time.split('T')[1].split('.')[0]
    return hour
      
def write_temp_file(path, typ):
    """Append result path of files to 'save.txt' temporally file
      
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
        tempnameLocation =  get_root_project()+'/dicResults/'+namefile
        metalex.resultOcrFiles.append(tempnameLocation)
    else:
        tempnameLocation =  os.getcwd()+'/'+namefile
        metalex.resultOcrFiles.append(tempnameLocation)
        
def in_dir(fil):
    """Verify if an input file is in a 'dicTemp' folder 
    
    :return Bool
    """
    currentdir = os.listdir('.')
    if fil in currentdir: return False
    else: return True

def go_to_dicresult():
    """Go to the 'dicResult' folder 
    
    :return dicResult folder
    """
    resultfolder = get_root_project()+'/dicResults'
    if 'dicResults' not in os.listdir(get_root_project()):
        os.mkdir(resultfolder)
    return os.chdir(resultfolder)
    
def name_file(tab, ext):
    """Generate name file to saved result of articles extraction  
    
    :param tab: array
    :param ext: str
      
    :return str: namepickle 
    """
    name  = str(tab[0]).split('/')[-1].split(',')[0].split('_')[:-1]
    if ext == '.art':
        if metalex.currentOcr == 'ocropy':
            nametxt  = 'articles_ocropy_'+'_'.join(name)+'.art'
            return nametxt
        else: return 'articles_'+'_'.join(name)+'.art'
    elif ext == '.pickle':
        if metalex.currentOcr == 'ocropy':
            nametxt  = 'articles_ocropy_'+'_'.join(name)+'.pickle'
            return nametxt
        else: return 'articles_'+'_'.join(name)+'.pickle'
        
def file_pickle(data, name):
    """Create pickle file of the articles data
    
    :param data: dictionary
    :param name: str
    
    :return Bool: True 
    """
    with codecs.open(name, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return True
    
def chunck_list(binFiles, group):
    """Generate a group of small element from big element
    
    :return list
    """
    return list(iterutils.get_chunks(binFiles, group))

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
        message = 'dicTemp folder -->> is created an initialised with' 
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
