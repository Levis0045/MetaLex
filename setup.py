#! usr/bin/env python
# coding: utf8

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
"""

from  setuptools import setup


setup(name="metalex",
      version='1.6.0',
      description='MetaLex is general tool for lexicographic and metalexicographic activities',
      author='Elvis MBONING',
      author_email='levismboning@yahoo.fr',
      packages=['metalex', 'metalex.logs', 'metalex.ocrtext', 'metalex.plugins', 'metalex.xmlised']
    )


__author__ = 'Elvis MBONING'