#!/usr/bin/python
# coding: utf8 


"""
    dicPlugings contains all extra-module fo Metalex Tool
     
"""


__version__ = "0.0.4"


# ----Internal Modules------------------------------------------------------


# ----External Modules------------------------------------------------------

import sys, os

# -----Global Variables-----------------------------------------------------


# ----------------------------------------------------------

pytesserocr = os.path.dirname(os.path.abspath(__file__))+'/pytesseocr'
resources = pytesserocr = os.path.dirname(os.path.abspath(__file__))+'/resources'

sys.path.append(pytesserocr)
sys.path.append(resources)
