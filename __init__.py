#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
    Ce package implémente tous les plugins de MetaLex
    
"""
 
__version__ = u"0.0.1"

# ----Internal Modules------------------------------------------------------

import codifications
from .dicOcrText    import *
from .dicXmlised    import *
from .dicLog        import *
from .dicPlugins    import *
from  dicProject    import *

# -----Global Variables-----------------------------------------------------

projectName        = u''
projectAuthor      = u''
allProjectNames    = [] 
fileImages         = []
treatImages        = []
resultOcrFiles     = []
resultOcrData      = {}
codifications      = {}

# ----------------------------------------------------------

version = u"MetaLex package is in a version : %s " %__version__

    