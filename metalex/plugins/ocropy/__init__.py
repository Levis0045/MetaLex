#!/home/elvis/Documents/Dev/ScanRexs/bin/python
# coding: utf8


"""Ocropy initialisation to """

# ---------Exported functions ---------------------------------------------

__all__ = ['ocropusRpred', 'ocropusLpred', 'ocropusGpageseg', 'ocropusRtrain', 
           'ocropusVisualizeResults', 'ocropusLtrain', 'ocropusHocr', 'ocropusGtedit', 
           'ocropusLinegen', 'ocropusCnfErrs', 'ocropusNlbin', 'modelDef',
           'ocropusErrs',]


__author__ = 'Elvis MBONING'
__version__ = '0.1' 

# ----External Module------------------------------------------------------

import os, sys
import platform

# -----Global Variables-----------------------------------------------------

currentFile = ''

# --------------------------------------------------------------------------

if platform.system() == 'Linux':
    currentFile = os.path.dirname(os.path.abspath(__file__)).replace(' ', '\\ ')
else:
    currentFile = os.path.dirname(os.path.abspath(__file__)).replace(' ', '\\ ')
    
ocropusNlbin = os.path.join(currentFile,'ocropus-nlbin')
ocropusRpred = os.path.join(currentFile, 'ocropus-rpred')
ocropusLpred = os.path.join(currentFile, 'ocropus-lpred')
ocropusGpageseg = os.path.join(currentFile, 'ocropus-gpageseg')
ocropusRtrain = os.path.join(currentFile, 'ocropus-rtrain')
ocropusVisualizeResults = os.path.join(currentFile, 'ocropus-visualize-results')
ocropusLtrain = os.path.join(currentFile, 'ocropus-ltrain')
ocropusHocr = os.path.join(currentFile, 'ocropus-hocr')
ocropusGtedit = os.path.join(currentFile, 'ocropus-gtedit')
ocropusErrs = os.path.join(currentFile, 'ocropus-errs')
ocropusCnfErrs = os.path.join(currentFile, 'ocropus-econf')
ocropusLinegen = os.path.join(currentFile, 'ocropus-linegen')
modelDef = os.path.join(currentFile, os.path.join('models', 'en-default.pyrnn.gz'))
#model4 = os.path.join(currentFile, os.path.join('models', 'REX-models_00290000_4-271.pyrnn.gz'))

 
# -------------------------------------------------------------------------
