#!/usr/bin/env python
# coding: utf8


"""
    ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing


    Usage:
        >>> import MetaLex as dico
        >>> projet = dico.newProject('LarousseMemoire')
     
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import os, codecs, re
import pickle

# -----Exported Functions---------------------------------------------------

__all__ = ['createtemp', 'newProject', 'treat_image_append', 'get_part_file', 'inDir']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

        
def get_part_file(namefile):
    """
      Extract file image name and file image extension
      @keyword namefile:str
      @return: list:(imageroot, ext)
    """
    (imageroot, ext) = os.path.splitext(os.path.basename(namefile))
    return (imageroot, ext)

def getHour():
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
    """
      Append image result files to the global variable at the scope
      @keyword namefile:str
      @return: ...
    """
    tempnameLocation =  os.getcwd()+u'/'+namefile
    MetaLex.treatImages.append(tempnameLocation)


def treat_ocr_append(namefile) :
    """
      Append ocr result files to the global variable
      @keyword namefile:str
      @return: ...
    """
    parentdir = os.listdir('..')
    if u'dicLogs' in parentdir :
        os.chdir('../dicTemp')
        tempnameLocation =  os.getcwd()+u'/'+namefile
        MetaLex.resultOcrFiles.append(tempnameLocation)
    else :
        tempnameLocation =  os.getcwd()+u'/'+namefile
        MetaLex.resultOcrFiles.append(tempnameLocation)
     
     
def inDir(fil):
    """
      Verify if an input file is in a 'dicTemp' folder 
      @return: Bool
    """
    currentdir = os.listdir('.')
    if fil in currentdir :
        return False
    else :
        return True


def nameFile(tab, ext):
    """
      Generate name file to saved result of articles extraction  
      @keyword tab:array
      @keyword ext:str
      @return: str:namepickle 
    """
    name  = str(tab[0]).split(u'/')[-1].split(u',')[0].split(u'_')[:-1]
    if ext == u'.art' :
        nametxt    = u'articles_'+u'_'.join(name)+u'.art'
        return nametxt
    elif ext == u'.pickle' :
        namepickle = u'articles_'+u'_'.join(name)+u'.pickle'
        return namepickle
        

def filePickle(data, name):
    """
      Create pickle file of the articles data
      @keyword data:dictionary
      @keyword name:str
      @return: Bool:True 
    """
    with codecs.open(name, 'wb') as f :
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return True
    
    
def fileUnpickle(fil):
    """
      Unpack pickle file of articles data
      @keyword fil:str
      @return: dict:data articles object
    """
    with codecs.open(fil, 'rb') as f :
        data = pickle.load(f)
        return data 


def fileGettext(fil):
    """
      Extract articles data into file text
      @return: dict:data articles text
    """
    datatext = {}
    with codecs.open(fil, 'r', 'utf-8') as f :
        for line in f :
            if re.search(ur'article_', line) :
                partline = line.split(u':')
                datatext[partline[0].strip()] = partline[1].strip()
    return datatext


def getRootProject():
    """
      Go to the root path of current project
      @return: root path of current project
    """
    projectF = MetaLex.projectFolder.items()[0][0]
    projectD = MetaLex.projectFolder.items()[0][1]
    projetPath = projectD+u'/'+projectF
    return projetPath


def readConf():
    """
      Extract data configuration of the project
      @return: dict:data configuration text
    """
    confData = {}
    rootPath = getRootProject()
    confPath = rootPath+u'/MetaLex.cnf'
    with codecs.open(confPath, 'r', 'utf-8') as conf :
        for line in conf :
            if line[0] == u'\\' : 
                part  = line.strip().split(u':')
                title = part[0][1:].replace(u' ', u'')
                val   = part[1]
                confData[title] = val
    return confData
        
        
def createtemp():
    """
      Create a 'dicTemp' folder if it doesn't exist at the parent folder at the scope
      @return: path:place in dicTemp folder
    """
    parentdir     = os.listdir('..')
    projectF      = MetaLex.projectFolder.items()[0][0]
    projectD      = MetaLex.projectFolder.items()[0][1]
    rootProject   = projectD+'/'+projectF
    dicTemp       = rootProject+'/dicTemp'
    contentdir    = os.listdir(rootProject)
    if 'dicTemp' not in contentdir :
        try:
            os.mkdir(dicTemp)
        except os.error :
            message = u'We can cannot create dicTemp folder in this directory ! It s right exception ?'
            MetaLex.dicLog.manageLog.writelog(message, typ='error')
            pass
        message = u'dicTemp folder >> is created an initialised with' 
        MetaLex.dicLog.manageLog.writelog(message)
        os.chdir(dicTemp)
    else :
        os.chdir(dicTemp) 
        

def dicFile(fil):
    """
      Take the current script path and join it to file path
      @keyword fil:str
      @return: path:normalize file path
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, fil)
       
        
class newProject :
    """
       Create new environment project and its configuration
       @keyword projectname: str
       @return: new environment project
    """
    
    import MetaLex
        
    def __init__ (self, projectname):
        self.name = projectname
        MetaLex.allProjectNames.append(self.name)
        MetaLex.projectName = self.name
        self.fileImages     = []
        self.resultOcr      = u""
        self.resultText     = u""
        self.resultXmlised  = u""
        self.resultLog      = u""
        self.lang           = u""
        self.dicoType       = u""
        self.projetFolder()
         
    def projetFolder(self):
        """
          Create folder of new environment project
          @return: project folder
        """
        folderName = 'MetaLex_'+self.name
        MetaLex.projectFolder[folderName] = os.getcwd()
        currentdir = os.listdir('.')
        if folderName in currentdir :
            os.chdir(folderName)
        else :
            try : 
                os.mkdir(folderName)
                os.chdir(folderName)
            except os.error :
                message =  u"We can can't create "+folderName+u" folder in this directory ! It is right exception ?"
                MetaLex.dicLog.manageLog.writelog(message, typ='error')
                
        
    def setConfProject (self, author, comment, contrib):
        """
          Set parameters of new environment project
          @keyword author:str
          @keyword comment:str
          @keyword contrib:str
          @return: file:normalize file path
        """
        MetaLex.projectAuthor = author
        projectF = MetaLex.projectFolder.items()[0][0]
        projectD = MetaLex.projectFolder.items()[0][1]
        acessDF  = projectF+u' | '+projectD
        project  = MetaLex.projectName
        Cdate    = MetaLex.manageLog.getDate()
        Ctime    = getHour()
        dateInit = Cdate.decode('ascii')+u' à '+Ctime
        log      = u'/dicLogs'+u' | '+projectD+u'/'+projectF+u'/dicLogs'
        temp     = u'/dicTemp'+u' | '+projectD+u'/'+projectF+u'/dicTemp'
        images   = u'/dicImages'+u' | '+projectD+u'/'+projectF+u'/dicImages'
        Intro    = u'***************** MetaLex project configuration *****************\n\n'
        access   = u'%-15s : %-10s \n' %(u'\Project folder', acessDF)
        end      = u'***************************************************************** \n\n'
   
        os.chdir(getRootProject())
        contentdir = os.listdir('.')
        if 'MetaLex.cnf' not in contentdir :
            with codecs.open('MetaLex.cnf', 'w', 'utf-8') as conf :
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
                
    def getProjectName(self):
        return MetaLex.projectName 

    def getFileImages (self):
        if (len(MetaLex.fileImages)>= 1) :
            self.fileImages = MetaLex.fileImages
            return self.fileImages
    
    def getTreatImages (self):
        if (len(MetaLex.dicOcrText.fileImages)>= 1) :
            self.treatImageFile  = MetaLex.dicOcrText.treatImageFile 
            return self.treatImageFile 
    
    def getTextOcr (self):
        if (MetaLex.dicOcrText.textOcr) :
            self.resultOcr += MetaLex.dicOcrText.textOcr
            return self.resultOcr
        
    def getOcrText (self):
        return MetaLex.dicOcrText.makeOcr

       
        
   
