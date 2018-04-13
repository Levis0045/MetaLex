#!/usr/bin/python
# coding: utf8 

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

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

MetaLex module

Ce module améliore la qualité des images soumises en entrée
du programme, et les ocrisent par la suite.

Functions :
    * Traitment of image files with PIL.image
    * Ocrisation of image files with tesseract
        
"""

__version__ = "1.9.0"


# ----Internal Modules------------------------------------------------------

from .normalizeImage  import EnhanceImages, get_images
from .makeOcr         import run_img_to_text
from .normalizeText   import BuildTextWell, FileRule
from .wordsCorrection import correct_word, caract_replace, word_replace 

# -----Global Variables-----------------------------------------------------

lang = u""
treatImageFile = object
textOcr = u""

# ----------------------------------------------------------

def version():
    return "normalizeImage package is in a version : %s \n" %__version__
