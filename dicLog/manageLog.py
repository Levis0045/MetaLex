#!/usr/bin/env python
# coding: utf8


"""
    MetaLex is general tool for lexicographic and metalexicographic activities
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


def getTime():
    datefile = os.popen('date').read()
    datetab  = datefile.split(' ')
    time = datetab[4]
    return time  
    
    
def logname():
    strdate = getDate()
    projectName = MetaLex.projectName
    logName = projectName+'_'+strdate+'.dicLog'
    return logName


def folderlog():
    hour = MetaLex.dicProject.getHour()
    name          = logname()
    parentdir     = os.listdir('..')
    projectF      = MetaLex.projectFolder.items()[0][0]
    projectD      = MetaLex.projectFolder.items()[0][1]
    rootProject   = projectD+'/'+projectF
    dicLogs       = rootProject+'/dicLogs'
    contentdir    = os.listdir(rootProject)
    logs          = u'[MetaLexLog - '+hour+u']'
    if 'dicLogs' not in contentdir :
        try :
            os.mkdir(dicLogs)
            os.chdir(dicLogs)
        except os.error :
            message = u'We can cannot create dicLogs folder in this directory ! It s right exception ?'
            print u'%-8s : %-30s\n' %(colored(logs, u'red', attrs=['reverse', 'blink', 'bold']), message)
            pass
    else:
        os.chdir(dicLogs)

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
    message = u'[MetaLexLog - '+hour+u']'
    if typ == 'warm' :
        print u'%-10s  %-30s\n' %(colored(message, u'yellow', attrs=['reverse', 'blink', 'bold']), content)
    elif typ == 'error' :
        print u'%-10s  %-30s\n' %(colored(message, u'red', attrs=['reverse', 'blink', 'bold']), content)
    else :
        print u'%-10s  %-30s\n' %(colored(message, u'green', attrs=['reverse', 'blink', 'bold']), content)
    
    
    
    
    
    
