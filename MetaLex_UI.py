#!/usr/bin/env python
# coding: utf8

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


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
    
    ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing
    
    Package :
        >>> sudo pip install termcolor
        
    Usage:
        >>> from metalex import manageLog
        >>> manageLog.writelog()

"""

# ----Internal Modules------------------------------------------------------

#import metalex

# ----External Modules------------------------------------------------------

import codecs
import os
import re
#import wx
import string
import termcolor

# -----Exported Functions-----------------------------------------------------

__all__ = ['']

# -----Global Variables-------------------------------------------------------


# ----------------------------------------------------------------------------

#print(dir(wx))

import wxversion
import wx, wx.html
from wx.lib.intctrl import IntCtrl
import sys

aboutText = ''


class OcrTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        ocr = wx.StaticText(self, -1, "FPCs OCR Process", (20,20))
 
class TrainingTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        training = wx.StaticText(self, -1, "FPCs Training Model Tools", (20,20))
 
class EvaluationTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        evaluation = wx.StaticText(self, -1, "FPCs Evaluation Tools", (20,20))
        
class ScanRexsHtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(900,700)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
     
        
class StartDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "ScanRexs Workspace",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        startSizer = wx.BoxSizer(wx.HORIZONTAL)
        createWorkspace = wx.Button(self, wx.ID_ANY, 'Create workspace', pos=(10, 10))
        openWorkspace = wx.Button(self, wx.ID_ANY, 'Open workspace', pos=(10,10))
        createWorkspace.Bind(wx.EVT_BUTTON, self.OnCreatetWorkspace)
        openWorkspace.Bind(wx.EVT_BUTTON, self.OnOpentWorkspace)
        startSizer.Add(createWorkspace, 1, wx.TOP | wx.CENTER)
        startSizer.Add(openWorkspace, 1, wx.BOTTOM | wx.CENTER)
        self.SetClientSize((300,100))
        self.SetSizer(startSizer)
        self.CentreOnParent(wx.CENTER)
        self.SetFocus() 
            
    def OnOpentWorkspace(self, event):
        self.dirname="."
        dialog = wx.FileDialog(self.GetParent(),
                      "Choose your workspace configuration",
                      style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            save_path = dialog.GetPath()
            if isfile("scanrexs.config".format(save_path)):
                file = open("scanrexs.config".format(save_path),'rb')
                model_settings = load(file)
                file.close()
            else:
                model_settings = (2,1,50)
            self.set_current_project(save_path,*model_settings)
        dialog.Destroy()
    
    def OnCreatetWorkspace(self, event):
        self.Destroy()
        dialog = wx.Dialog(None, -1, "Create new ScanRexs Workspace",
            style=wx.OK|wx.CANCEL|wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        
        if dialog.ShowModal() == wx.ID_OK:
            save_path = dialog.GetPath()
            if isfile("scanrexs.pickle.config".format(save_path)):
                file = open("scanrexs.pickle.config".format(save_path),'rb')
                model_settings = load(file)
                file.close()
            else:
                model_settings = (2,1,50)
            self.set_current_project(save_path,*model_settings)
        dialog.Destroy()
               
               
               
class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About [CNES] ScanRexs ",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = ScanRexsHtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        #btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()


class ScanRexs(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ScanRexs, self).__init__(size=(940,680),*args, **kwargs)        
        self.CreateStatusBar()
        self.scanrexsMenuBar()
        self.bindScanrexsActions()
        self.ScanrexsUiTabs()
        self.Show()
        self.Disable()
        self.start()
        
        
    def ScanrexsUiTabs(self):
        panel = wx.Panel(self)
        nb = wx.Notebook(panel)
        # Create the process tab of ScanRexs
        tab1 = OcrTab(nb)
        tab2 = TrainingTab(nb)
        tab3 = EvaluationTab(nb)
        # Add process tab to ScanRexs
        nb.AddPage(tab1, "FPCs OCR Process")
        nb.AddPage(tab2, "FPCs Training Model Tools")
        nb.AddPage(tab3, "FPCs Evaluation Tools")
        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        
    def start(self):
        dialogStart = StartDialog()
        dialogStart.ShowModal()
        dialogStart.Destroy()
    
    def bindScanrexsActions(self):
        self.Bind(wx.EVT_MENU, self.OnCreateWorkspace, self.createWorkspace)
        self.Bind(wx.EVT_MENU, self.OnOpenWorkspace, self.openWorkspace)
        self.Bind(wx.EVT_MENU, self.OnSaveData, self.saveData)
        self.Bind(wx.EVT_MENU, self.OnClose, self.exitProgram)
        self.Bind(wx.EVT_MENU, self.OnEditHtml, self.editHtml)
        self.Bind(wx.EVT_MENU, self.OnViewCorrectedHtml, self.viewCorrectedHtml)
        self.Bind(wx.EVT_MENU, self.OnViewUncorrectedHtml, self.viewUncorrectedHtml)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.about)
        self.Bind(wx.EVT_MENU, self.OnDocumentation, self.documentation)
        self.Bind(wx.EVT_MENU, self.OnVersion, self.version)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def scanrexsMenuBar(self):        
        self.menuMain = wx.Menu()
        self.menuEdit = wx.Menu()
        self.menuTools = wx.Menu()
        self.menuHelp = wx.Menu()
        
        self.createWorkspace = self.menuMain.Append(wx.ID_NEW, "&Create\tCtrl-N", "Create new workspace.")
        self.openWorkspace = self.menuMain.Append(wx.ID_OPEN, "&Open\tCtrl-O", "Open existing workspace.")
        self.saveData = self.menuMain.Append(wx.ID_SAVE, "&Export\tCtrl-S", "Export data to appropriate format.")
        self.exitProgram = self.menuMain.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        
        self.editHtml = self.menuEdit.Append(wx.ID_EDIT, "&Edit Html", "Correct the output of HTML files")
        self.viewCorrectedHtml = self.menuEdit.Append(wx.ID_VIEW_DETAILS, "&View corrected Html", "View all corrected HTML files")
        self.viewUncorrectedHtml = self.menuEdit.Append(wx.ID_ANY, "&View uncorrected Html", "View all uncorrected HTML files")
        
        self.trainingTools = self.menuTools.Append(wx.ID_ANY, "&Training model", "Training model for recognition")
        self.ocrTools = self.menuTools.Append(wx.ID_EDIT, "&Ocropy OCR", "OCR with Ocropy")
        self.evaluationTools = self.menuTools.Append(wx.ID_EDIT, "&Evaluation", "Evaluation of all results")
                
        self.about = self.menuHelp.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.version = self.menuHelp.Append(wx.ID_ANY, "&Version", "Information version about this program")
        self.documentation = self.menuHelp.Append(wx.ID_ANY, "&Documentation", "Documentation about this program")
        
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.menuMain, "&Main")
        self.menuBar.Append(self.menuEdit, "&Results")
        self.menuBar.Append(self.menuTools, "&Tools")
        self.menuBar.Append(self.menuHelp, "&Help")
        self.SetMenuBar(self.menuBar)

    
    def OnSaveData(self, event):
        return None
    
    def OnVersion(self, event):
        return None
    
    def OnEditHtml(self, event):
        return None
    
    def OnViewCorrectedHtml(self, event):
        return None
    
    def OnViewUncorrectedHtml(self, event):
        return None
    
    def OnDocumentation(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()
    
    
        
    def OnOpenWorkspace(self, event):
        self.dirname="."
        dialog = wx.DirDialog(self.GetParent(),
                      "Choose your current workspace",
                      style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            save_path = dialog.GetPath()
            if isfile("scanrexs.config".format(save_path)):
                file = open("scanrexs.config".format(save_path),'rb')
                model_settings = load(file)
                file.close()
            else:
                model_settings = (2,1,50)
            self.set_current_project(save_path,*model_settings)
        dialog.Destroy()
       
       
    def OnCreateWorkspace(self, event):
        dialog = wx.Dialog(self, -1,"Paramètres d'entraînement")
        
            
    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close your Workspace and ScanRexs application ?",
            "Confirm ScanRexs Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()  




def run_app():
    app = wx.App()
    ScanRexs(None, -1, "ScanRexs Tool")
    app.MainLoop()







# -- Lancement de l'application

if __name__ == '__main__':
    run_app()
