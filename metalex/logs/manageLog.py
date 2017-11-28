#!/usr/bin/env python
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
    
    ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing
    
    Package :
        >>> sudo pip install termcolor
        
    Usage:
        >>> from metalex import manageLog
        >>> manageLog.writelog()

"""

# ----Internal Modules------------------------------------------------------

import metalex

# ----External Modules------------------------------------------------------

import codecs
import os
import re
import unicodedata
from string import maketrans
from termcolor import colored, cprint

# -----Exported Functions-----------------------------------------------------

__all__ = ['write_log', 'log_name', 'folder_log', 'get_date']

# -----Global Variables-------------------------------------------------------


# ----------------------------------------------------------------------------

def get_date():
    strdate  = ''
    datefile = os.popen('date').read()

    if re.search(ur'.+\(UTC+.*', datefile) :
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
    else :
        datetab = datefile.split(' ')
        day, month, year = datetab[2], datetab[1], datetab[5]
        strdate = day+'-'+month+'-'+year
        return strdate


def get_time():
    datefile = os.popen('date').read()
    datetab  = datefile.split(' ')
    time = datetab[4]
    return time  
    
    
def log_name():
    strdate = get_date()
    projectName = metalex.projectName
    log_name = projectName+'_'+strdate+'.logs'
    return log_name


def folder_log():
    hour = metalex.project.get_hour()
    name = log_name()
    parentdir = os.listdir('..')
    projectF = metalex.projectFolder.items()[0][0]
    projectD = metalex.projectFolder.items()[0][1]
    rootProject = projectD+'/'+projectF
    logs = rootProject+'/logs'
    contentdir = os.listdir(rootProject)
    logsMessage = u'[metalexLog - '+hour+u']'
    if 'logs' not in contentdir :
        try :
            os.mkdir(logs)
            os.chdir(logs)
        except os.error :
            message = u'We can cannot create logs folder in this directory ! It s right exception ?'
            print u'%-8s : %-30s\n' %(colored(logsMessage, u'red', attrs=['reverse', 'blink', 'bold']), message)
            pass
    else:
        os.chdir(logs)

    currentdirlog = os.listdir(u'.')
    if name not in currentdirlog:
        logfile = codecs.open(name.replace('\n', ''), 'a', 'utf-8')
        return logfile
    else:
        pass



def write_log(content, typ=u'ok'):
    name = log_name()
    hour = metalex.project.get_hour()

    folder_log()
    currentdirlog = os.listdir(u'.')
    if name in currentdirlog :
        with codecs.open(name, 'a', 'utf-8') as log :
            message = u'[metalex - '+hour+u'] '+content+u'\n\n'
            log.write(message)
    else:
        pass
    message = u'[metalexLog - '+hour+u']'
    if typ == 'warm' :
        print u'%-10s  %-30s\n' %(colored(message, u'yellow', attrs=['reverse', 'blink', 'bold']), content)
    elif typ == 'error' :
        print u'%-10s  %-30s\n' %(colored(message, u'red', attrs=['reverse', 'blink', 'bold']), content)
    else :
        print u'%-10s  %-30s\n' %(colored(message, u'green', attrs=['reverse', 'blink', 'bold']), content)
    
    
    
    
    
    
