#!/usr/bin/env python
# coding: utf8


"""
    ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing
    
    Package :
        >>> sudo pip install termcolor
        
    Usage:
        >>> from MetaLex import manageLog
        >>> manageLog.writelog()

"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import codecs, os, re
import unicodedata
from string import maketrans
from termcolor import colored, cprint

# -----Exported Functions-----------------------------------------------------

__all__ = ['writelog', 'logname', 'folderlog', 'getDate']

# -----Global Variables-------------------------------------------------------


# ----------------------------------------------------------------------------

def getDate():
    strdate  = ''
    datefile = os.popen('date').read()

    try :
        datetab  = datefile.split(',')[0].split(' ')
        for date in datetab[1:] :
            strdate += date+'-'
        date = unicode(strdate.strip('-').translate(maketrans('û', 'u ')))
        date = unicodedata.normalize('NFKD', date).encode('ascii','ignore')
        return date
    except :
        datetab  = datefile.split(' ')
        for date in datetab :
            strdate += date+'-'
        date = unicode(strdate.strip('-'))
        return date  


def logname():
    strdate = getDate()
    projectName = MetaLex.projectName
    logName = projectName+'_'+strdate+'.dicLog'
    return logName


def folderlog():
    name       = logname()
    parentdir  = os.listdir('..')
    currentdir = os.listdir('.')

    if 'dicLogs' in currentdir :
        os.chdir('dicLogs')
    elif 'dicLogs' not in currentdir and 'dicTemp' in currentdir :
        try :
            os.mkdir('dicLogs')
        except os.error :
            message = 'We can cannot create dicLogs folder in this directory ! It s right exception ?'
            print u'%-8s : %-30s\n' %(colored(u'[MetaLexLog]', u'red', attrs=['reverse', 'blink', 'bold']), message)
            pass
        os.chdir(u'dicLogs/')
    elif 'dicLogs' not in currentdir and 'dicLogs' in parentdir :
        os.chdir(u'..')
        os.chdir(u'dicLogs/')
    else :
        try :
            os.mkdir(u'dicLogs')
        except os.error :
            message = 'We can cannot create dicLogs folder in this directory ! It s right exception ?'
            print u'%-8s : %-30s\n' %(colored(u'[MetaLexLog]', u'red', attrs=['reverse', 'blink', 'bold']), message)
            pass
        os.chdir(u'dicLogs/')

    currentdirlog = os.listdir(u'.')
    if name not in currentdirlog :
        logfile = codecs.open(name, 'a', 'utf-8')
        return logfile
    else:
        pass



def writelog(content, typ=u'ok'):
    name = logname()
    hour = MetaLex.dicProject.getHour()

    folderlog()
    currentdirlog = os.listdir(u'.')
    if name in currentdirlog :
        with codecs.open(name, 'a', 'utf-8') as log :
            message = u'[MetaLex - '+hour+u'] '+content+u'\n\n'
            log.write(message)
    else:
        pass
    #os.chdir('..')
    message = u'[MetaLexLog - '+hour+u']'
    if typ == 'warm' :
        print u'%-10s  %-30s\n' %(colored(message, u'yellow', attrs=['reverse', 'blink', 'bold']), content)
    elif typ == 'error' :
        print u'%-10s  %-30s\n' %(colored(message, u'red', attrs=['reverse', 'blink', 'bold']), content)
    else :
        print u'%-10s  %-30s\n' %(colored(message, u'green', attrs=['reverse', 'blink', 'bold']), content)
    
    
    
    
    
    
