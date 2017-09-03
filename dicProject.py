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


def readConf():
    """
      Extract data configuration of the project
      @return: dict:data configuration text
    """
    confData = {}
    with codecs.open(u'MetaLex.cnf', 'r', 'utf-8') as conf :
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
      
    contentdir     = os.listdir('.')
    parentdir      = os.listdir('..')
    if 'dicLogs' in contentdir and 'dicTemp' not in contentdir :
        try:
            os.mkdir('dicTemp')
        except os.error :
            print 'Error :  We can cannot create dicTemp folder in this directory ! It s right exception ?'
            pass
        message = u'dicTemp folder' + u'  > is created an initialised' 
        MetaLex.dicLog.manageLog.writelog(message)
        os.chdir('dicTemp/')

    elif 'dicLogs' in contentdir and 'dicTemp' in contentdir :
        os.chdir('dicTemp/') 
    elif 'dicLogs' not in contentdir and 'dicLogs' in parentdir and 'dicTemp' in parentdir :
        os.chdir('..')
        os.chdir('dicTemp/')
    elif 'dicLogs' not in contentdir and 'dicLogs' in parentdir and 'dicTemp' not in parentdir :
        os.chdir('..')
        try:
            os.mkdir('dicTemp')
        except os.error :
            print 'Error :  We can cannot create dicTemp folder in this directory ! It s right exception ?'
            pass
        os.chdir('dicTemp/') 
        

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
    
    def setConfProject (self, author, comment, contrib):
        """
          Set parameters of new environment project
          @keyword author:str
          @keyword comment:str
          @keyword contrib:str
          @return: file:normalize file path
        """
        MetaLex.projectAuthor = author
        project  = MetaLex.projectName
        dateInit = MetaLex.manageLog.getDate()
        Intro    = u'***************** MetaLex project configuration *****************\n\n'
        end      = u'***************************************************************** \n\n'
        #content  = Intro+'\n\n'+'\Project name  : '+project+'\n'+'\Creation date : '+dateInit+'\n'+'\Author  : '+author+'\n'+'\Contributors  : '+contrib+'\n'+'\Comment       : '+comment+'\n\n'+end
        #print type(dateInit), dateInit
        MetaLex.dicProject.createtemp()
        if MetaLex.dicProject.inDir('MetaLex.cnf') :
            with codecs.open('MetaLex.cnf', 'w', 'utf-8') as conf :
                conf.write(Intro)
                conf.write('%-15s : %-10s \n'   %(u'\Project name', project))
                conf.write('%10s : %s \n'   %(u'\Creation date', dateInit.decode('ascii')))
                conf.write('%-15s : %-10s \n'   %(u'\Author', author))
                conf.write('%-15s : %-10s \n'   %(u'\Contributors', contrib))
                conf.write('%-15s : %-10s \n\n' %(u'\Comment', comment))
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

       
        
   
