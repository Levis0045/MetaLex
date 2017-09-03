#!/usr/bin/python
# coding: utf8 


"""
    Ce module traite, c'est à dire améliore la qualité des images soumises en entrée
    du programme, et les ocrisent par la suite.
    
    Functions :
        * Traitment of image files with PIL.image
        * Ocrisation of image files with tesseract
        
"""


__version__ = "0.0.3"

# ----Internal Modules------------------------------------------------------

from normalizeImage  import enhanceImages, getImages
from makeOcr         import imageToText
from normalizeText   import makeTextWell, fileRule
from wordsCorrection import correctWord, caractReplace, wordReplace

# -----Global Variables-----------------------------------------------------

lang = u""
treatImageFile = object
textOcr = u""

# ----------------------------------------------------------

def version():
    return "normalizeImage package is in a version : %s \n" %__version__
