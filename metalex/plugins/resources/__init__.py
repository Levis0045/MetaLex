#!/usr/bin/python
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

metalex module

dicPlugins contains all extra-functions and class for metalex Tool
     
"""


__version__ = "1.6.0"


# ----External Modules------------------------------------------------------

import sys, os

# -----Global Variables-----------------------------------------------------

__all__ = ['html_template', 'css_template']

# --------------------------------------------------------------------------


html_template = os.path.dirname(os.path.abspath(__file__))+'/metalex-template.html'
css_template = os.path.dirname(os.path.abspath(__file__))+'/w3.css'
