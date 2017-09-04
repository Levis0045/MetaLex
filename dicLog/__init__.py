#!/usr/bin/python
# coding: utf8


"""
    dicLog enrégistre toutes les opérations déclenchées tout au long du processus
    de traitement métalexicographique
     
"""


__version__ = "0.0.3"


# ----Internal Modules------------------------------------------------------

from .. import *
from manageLog import *

# ----External Modules------------------------------------------------------

import sys

# -----Global Variables-----------------------------------------------------


# ----------------------------------------------------------


def version():
    return "dicLog package is in a version : %s \n" %__version__
