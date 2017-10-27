#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""MetaLex is general tool for lexicographic and metalexicographic activities

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

MetaLex main package

Ce package implémente tous les plugins de MetaLex
    
"""
 
__version__ = u"1.6.0"

# ----Internal Modules------------------------------------------------------

import codifications
from .ocrtext    import *
from .xmlised    import *
from .logs       import *
from .plugins    import *
from  project    import *

# -----Global Variables-----------------------------------------------------

projectName = u''
projectAuthor = u''
allProjectNames = [] 
fileImages = []
treatImages  = []
resultOcrFiles = []
resultOcrData = {}
codifications = {}
projectFolder = {}

# ----------------------------------------------------------

version = u"MetaLex package is in a version : %s " %__version__

    