#!/usr/bin/env python
# coding: utf8

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

Contact : levismboning@yahoo.fr

---------------------------------------------------------------------------

ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing


Usage:
    >>> import metalex as dico
    >>> projet = dico.newProject('LarousseMemoire')
     
"""

# ----Internal Modules------------------------------------------------------

import metalex

# ----External Modules------------------------------------------------------

import os
import codecs
import re
import pickle

# -----Exported Functions---------------------------------------------------

__all__ = ['create_temp', 'NewProject', 'treat_image_append', 'get_part_file', 'in_dir']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

        
def get_part_file(namefile):
    """Extract file image name and file image extension
    
    :param namefile: str
    
    :return list: (imageroot, ext)
    """
    (imageroot, ext) = os.path.splitext(os.path.basename(namefile))
    return (imageroot, ext)


def get_hour():
    """Get the current system time 
    
    :return str: hour
    """
    datefile = os.popen('date').read()
    try :
        datetab = datefile.split(',')[1].split(' ')
        hour = datetab[1]
        return hour
    except :
        datetab = datefile.split(' ')[3]
        hour = datetab
        return hour
    
    
def treat_image_append(namefile) :
    """Append image result files to the global variable at the scope
      
    :param namefile: str
    
    :return ...
    """
    tempnameLocation =  os.getcwd()+u'/'+namefile
    metalex.treatImages.append(tempnameLocation)


def treat_ocr_append(namefile) :
    """Append ocr result files to the global variable
    
    :param namefile: str
    
    :return ...
    """
    parentdir = os.listdir('..')
    if u'logs' in parentdir :
        os.chdir('../dicTemp')
        tempnameLocation =  os.getcwd()+u'/'+namefile
        metalex.resultOcrFiles.append(tempnameLocation)
    else :
        tempnameLocation =  os.getcwd()+u'/'+namefile
        metalex.resultOcrFiles.append(tempnameLocation)
     
     
def in_dir(fil):
    """Verify if an input file is in a 'dicTemp' folder 
    
    :return Bool
    """
    currentdir = os.listdir('.')
    if fil in currentdir :
        return False
    else :
        return True


def name_file(tab, ext):
    """Generate name file to saved result of articles extraction  
    
    :param tab: array
    :param ext: str
      
    :return str: namepickle 
    """
    name  = str(tab[0]).split(u'/')[-1].split(u',')[0].split(u'_')[:-1]
    if ext == u'.art' :
        nametxt    = u'articles_'+u'_'.join(name)+u'.art'
        return nametxt
    elif ext == u'.pickle' :
        namepickle = u'articles_'+u'_'.join(name)+u'.pickle'
        return namepickle
        

def file_pickle(data, name):
    """Create pickle file of the articles data
    
    :param data: dictionary
    :param name: str
    
    :return Bool: True 
    """
    with codecs.open(name, 'wb') as f :
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return True
    
    
def file_unpickle(fil):
    """Unpack pickle file of articles data
    
    :param fil: str
    
    :return dict: data articles object
    """
    with codecs.open(fil, 'rb') as f :
        data = pickle.load(f)
        return data 


def file_get_text(fil):
    """Extract articles data into file text
    
    :return dict: data articles text
    """
    datatext = {}
    with codecs.open(fil, 'r', 'utf-8') as f :
        for line in f :
            if re.search(ur'article_', line) :
                partline = line.split(u':')
                datatext[partline[0].strip()] = partline[1].strip()
    return datatext


def get_root_project():
    """Go to the root path of current project
    
    :return root path of current project
    """
    projectF = metalex.projectFolder.items()[0][0]
    projectD = metalex.projectFolder.items()[0][1]
    projetPath = projectD+u'/'+projectF
    return projetPath


def read_conf():
    """Extract data configuration of the project
    
    :return dict: data configuration text
    """
    confData = {}
    rootPath = get_root_project()
    confPath = rootPath+u'/metalex.cnf'
    with codecs.open(confPath, 'r', 'utf-8') as conf :
        for line in conf :
            if line[0] == u'\\' : 
                part  = line.strip().split(u':')
                title = part[0][1:].replace(u' ', u'')
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
    if 'dicTemp' not in contentdir :
        try:
            os.mkdir(dicTemp)
        except os.error :
            message = u'We can cannot create dicTemp folder in this directory ! It s right exception ?'
            metalex.logs.manageLog.write_log(message, typ='error')
            pass
        message = u'dicTemp folder >> is created an initialised with' 
        metalex.logs.manageLog.write_log(message)
        os.chdir(dicTemp)
    else :
        os.chdir(dicTemp) 
        

def dic_file(fil):
    """Take the current script path and join it to file path
    
    :param fil: str
    
    :return path: normalize file path
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, fil)
       
        
class NewProject :
    """Create new environment project and its configuration
    
    :param projectname: str
    
    :return new environment project
    """
    
    import metalex
        
    def __init__ (self, projectname):
        self.name = projectname
        metalex.allProjectNames.append(self.name)
        metalex.projectName = self.name
        self.fileImages     = []
        self.resultOcr      = u""
        self.resultText     = u""
        self.resultXmlised  = u""
        self.resultLog      = u""
        self.lang           = u""
        self.dicoType       = u""
        self.project_folder()
         
    def project_folder(self):
        """Create folder of new environment project
        
        :return project folder
        """
        folderName = 'metalex_'+self.name
        metalex.projectFolder[folderName] = os.getcwd()
        currentdir = os.listdir('.')
        if folderName in currentdir :
            os.chdir(folderName)
        else :
            try : 
                os.mkdir(folderName)
                os.chdir(folderName)
            except os.error :
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
        acessDF  = projectF+u' | '+projectD
        project  = metalex.projectName
        Cdate    = metalex.logs.manageLog.get_date()
        Ctime    = get_hour()
        dateInit = Cdate.decode('ascii')+u' à '+Ctime
        log      = u'/logs'+u' | '+projectD+u'/'+projectF+u'/logs'
        temp     = u'/dicTemp'+u' | '+projectD+u'/'+projectF+u'/dicTemp'
        images   = u'/dicImages'+u' | '+projectD+u'/'+projectF+u'/dicImages'
        Intro    = u'***************** metalex project configuration *****************\n\n'
        access   = u'%-15s : %-10s \n' %(u'\Project folder', acessDF)
        end      = u'***************************************************************** \n\n'
   
        os.chdir(get_root_project())
        contentdir = os.listdir('.')
        if 'metalex.cnf' not in contentdir :
            with codecs.open('metalex.cnf', 'w', 'utf-8') as conf :
                conf.write(Intro)
                conf.write(access)
                conf.write(u'%-15s : %-10s \n'   %(u'\Project name', project))
                conf.write(u'%-15s : %-10s \n'   %(u'\Creation date', dateInit))
                conf.write(u'%-15s : %-10s \n'   %(u'\Author', author))
                conf.write(u'%-15s : %-10s \n'   %(u'\Contributors', contrib))
                conf.write(u'%-15s : %-10s \n'   %(u'\Comment', comment))
                conf.write(u'%-15s : %-10s \n'   %(u'\Folder log', log))
                conf.write(u'%-15s : %-10s \n'   %(u'\Folder temp', temp))
                conf.write(u'%-15s : %-10s \n\n' %(u'\Folder images', images))
                conf.write(end)
                
    def get_project_name(self):
        return metalex.projectName 

    def get_file_images (self):
        if (len(metalex.fileImages)>= 1) :
            self.fileImages = metalex.fileImages
            return self.fileImages
    
    def get_treat_images (self):
        if (len(metalex.ocrtext.fileImages)>= 1) :
            self.treatImageFile  = metalex.ocrtext.treatImageFile 
            return self.treatImageFile 
    
    def get_text_ocr (self):
        if (metalex.ocrtext.textOcr) :
            self.resultOcr += metalex.ocrtext.textOcr
            return self.resultOcr
        
    def get_ocr_text (self):
        return metalex.ocrtext.makeOcr

       
        
   
