#! usr/bin/env python
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

----------------------------------------------------
entry_points={
  'console_scripts': [
      'metalex=metalex.runMetaLex -h',
      'metalex=metalex.runMetaLex -d testImages -s',
  ],
}
----------------------------------------------------
"""

from  setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name="metalex",
      version='2.0',
      description='MetaLex is general tool for lexicographic and metalexicographic activities',
      author='Elvis MBONING',
      author_email='levismboning@yahoo.fr',
      packages=['metalex', 'metalex.logs', 'metalex.ocrtext', 'metalex.plugins', 
                'metalex.xmlised', 'metalex.plugins.ocropy', 'metalex.plugins.resources',
                'metalex.plugins.ocropy.ocrolib', 'metalex.plugins.ocropy.tests',
                'metalex.plugins.ocropy.models'],
      license='AGPL',
      url='https://github.com/Levis0045/MetaLex',
      long_description=long_description,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers - Lexicographers - Metalexicographers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: AGPL License',
        'Programming Language :: Python :: 2.7',
      ],
      install_requires=['tesserocr', 'bs4', 'lxml', 'beautifulsoup4', 'PIL', 
                        'html5lib', 'Pillow', 'termcolor', 'Cython', 'termcolor', 
                        'imagesize', 'psutil'],
      extras_require={
        'dev': [''],
        'test': [''],
      },
      package_data={
        'metalex.plugins.resources': ['metalex-template.html','metalexSchemaXml.xsd','w3.css',
                                      'METALEX_words-corpus.txt', 'METALEX_words-corpus2.txt'],
        'metalex.plugins.ocropy.models': ['en-default.pyrnn.gz', 'REX-models_00287000_5-653.pyrnn.gz', 
                                        'REX-models_00290000_4-271.pyrnn.gz', 'README.md'],
        'metalex.plugins.ocropy': ['ocropus-dewarp', 'ocropus-econf', 'ocropus-errs', 'ocropus-gpageseg',
                                 'ocropus-gtedit', 'ocropus-hocr', 'ocropus-linegen', 'ocropus-lpred',
                                 'ocropus-ltrain', 'ocropus-nlbin', 'ocropus-rpred', 'ocropus-rtrain',
                                 'ocropus-visualize-results', 'LICENSE', 'PACKAGES', 'README.md', 
                                 'circle.yml', 'requirements.txt'],
        '.': ['README.rst'],
      },
      entry_points={
            'console_scripts': [
                'metalex=metalex.runMetaLex:run_metalex_test',
            ]
      },
      
    )


__author__ = 'Elvis MBONING'
