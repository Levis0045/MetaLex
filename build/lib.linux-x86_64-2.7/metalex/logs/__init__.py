#!/usr/bin/python
# coding: utf8

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

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

MetaLex logs module

dicLog enrégistre toutes les opérations déclenchées tout au long du processus
de traitement métalexicographique
     
"""


__version__ = "1.6.0"


# ----External Modules------------------------------------------------------

import sys

# ----Internal Modules------------------------------------------------------

from .. import *
from .manageLog import *

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

def version():
    return "dicLog package is in a version : %s \n" %__version__
