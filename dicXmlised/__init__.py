#!/usr/bin/python
# coding: utf8 




__version__ = "0.0.2"

# ----Internal Modules------------------------------------------------------

from composeArticle import parseArticle, structuredWithCodif
from handleStat     import *
from makeBalise     import *

# -----Global Variables-----------------------------------------------------

balise_norm  = ""
treatXmlFile = []
textXml      = ""

# ----------------------------------------------------------

def version():
    return "dicXmlised package is in a version : %s \n" %__version__
