#Made by the
# ____ ____ ____ 
#||E |||N |||H ||
#||__|||__|||__||
#|/__\|/__\|/__\|

import wx
import os
from wx.lib.wordwrap import wordwrap

wildcard = "Text Files (*.txt)|*.txt|"     \
           "All files (*.*)|*.*"

licenseText = "DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE\nVersion 2, December 2004\n\nCopyright (C) 2004 Sam Hocevar <sam@hocevar.net>\n\nEveryone is permitted to copy and distribute verbatim or modified\ncopies of this license document, and changing it is allowed as long\nas the name is changed.\n\nDO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE\nTERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION\n\n 0. You just DO WHAT THE FUCK YOU WANT TO.\n\n/* This program is free software. It comes without any warranty, to\n* the extent permitted by applicable law. You can redistribute it\n* and/or modify it under the terms of the Do What The Fuck You Want\n* To Public License, Version 2, as published by Sam Hocevar. See\n* http://www.wtfpl.net/ for more details. */"

     
class NotPad(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(NotPad, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        
    def InitUI(self):

        self.openfile = ""

        menubar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        newi = fileMenu.Append(wx.ID_ANY, '&New\tCtrl+N', 'Create an new file.')
        openi = fileMenu.Append(wx.ID_ANY, '&Open\tCtrl+O', 'Open a file.')
        savei = fileMenu.Append(wx.ID_ANY, '&Save\tCtrl+S', 'Save the current file.')
        saveasi = fileMenu.Append(wx.ID_ANY, '&Save As...', 'Save the current file with a diffrent filename.')
        fileMenu.AppendSeparator()
        quiti = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit NotPad.')

        editMenu = wx.Menu()
        undoi = editMenu.Append(wx.ID_ANY, '&UnDo\tCtrl+Z', 'Undo your last action.')
        redoi = editMenu.Append(wx.ID_ANY, '&ReDo\tCtrl+Y', 'Redo your last action.')
        editMenu.AppendSeparator()
        cuti = editMenu.Append(wx.ID_ANY, '&Cut\tCtrl+X', 'Cut the text to the clipboard.')
        copyi = editMenu.Append(wx.ID_ANY, '&Copy\tCtrl+C', 'Copy the text to the clipboard.')
        pastei = editMenu.Append(wx.ID_ANY, '&Paste\tCtrl+V', 'Paste text from the clipboard.')
        editMenu.AppendSeparator()
        selalli = editMenu.Append(wx.ID_ANY, '&Select All\tCtrl+A', 'Select all the text.')

        helpMenu = wx.Menu()
        helpi = helpMenu.Append(wx.ID_ANY, '&Help', 'Help on using NotPad.')
        abouti = helpMenu.Append(wx.ID_ANY, '&About', 'Read about NotPad.')
        
        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(helpMenu, '&Help')
        
        self.SetMenuBar(menubar)

        self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.HSCROLL)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, quiti)
        self.Bind(wx.EVT_MENU, self.OpenFile, openi)
        self.Bind(wx.EVT_MENU, self.NewFile, newi)
        self.Bind(wx.EVT_MENU, self.SaveFile, savei)
        self.Bind(wx.EVT_MENU, self.SaveFileAs, saveasi)
        
        self.Bind(wx.EVT_MENU, self.CopyText, copyi)
        self.Bind(wx.EVT_MENU, self.CutText, cuti)
        self.Bind(wx.EVT_MENU, self.PasteText, pastei)

        self.Bind(wx.EVT_MENU, self.UndoAct, undoi)
        self.Bind(wx.EVT_MENU, self.RedoAct, redoi)
        self.Bind(wx.EVT_MENU, self.SelectAllAct, selalli)

        self.Bind(wx.EVT_MENU, self.HelpBox, helpi)
        self.Bind(wx.EVT_MENU, self.AboutBox, abouti)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.Show()

        self.SetSize((500, 500))
        self.SetTitle('NotPad')
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e):
        self.Close()

    def OpenFile(self, evt):
        self.CheckFile()
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.txt.ChangeValue(open(dlg.GetPaths()[0]).read())
            self.openfile = dlg.GetPaths()[0]
            self.SetStatusText("file \""+str(dlg.GetPaths()[0])+"\" opened.", 0)

        dlg.Destroy()

    def NewFile(self, evt):
        self.CheckFile()
        self.openfile == ""
        self.txt.ChangeValue("")
        self.SetStatusText("New file created.", 0)

    def CheckFile(self):
        if not self.openfile == "":
            if not self.txt.GetValue() == open(self.openfile).read():
                dial = wx.MessageDialog(None, 'Do you want to save the current file?', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                result = dial.ShowModal()
                if result == wx.ID_YES:
                    self.SaveFile(self.txt.GetValue())
                    return

    def SaveFile(self, evt):
        if self.openfile == "":
            dlg = wx.FileDialog(
                self, message="Save file as ...", defaultDir=os.getcwd(), 
                defaultFile="", wildcard=wildcard, style=wx.SAVE
                )
        
            dlg.SetFilterIndex(2)

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                fp = file(path, 'w')
                fp.write(self.txt.GetValue())
                fp.close()
            
            dlg.Destroy()
        else:
            fp = file(self.openfile, 'w')
            fp.write(self.txt.GetValue())
            fp.close()

    def SaveFileAs(self, evt):
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )
        
        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            fp = file(path, 'w')
            fp.write(self.txt.GetValue())
            fp.close()
            
        dlg.Destroy()

    def CopyText(self, evt):
        self.txt.Copy()

    def CutText(self, evt):
        self.txt.Cut()

    def PasteText(self, evt):
        self.txt.Paste()

    def UndoAct(self, evt):
        self.txt.Undo()

    def UndoAct(self, evt):
        self.txt.Undo()

    def RedoAct(self, evt):
        self.txt.Redo()

    def SelectAllAct(self, evt):
        self.txt.SetSelection(-1, -1)

    def AboutBox(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = "NotPad"
        info.Version = "1.0.0"
        info.Copyright = "(C) 2013 Nsmurf"
        info.Description = wordwrap(
            "NotPad is a simple notepad  program, much like the one built into windows. "
            "NotPad is open source, and programmed with python and wxpython.\n"
            "NotPad ToDo List:\n*Tabs\n*A real-ish help dialog.\n*Syntax highlighting\n*A Mono-width font\n*Awesomeness",
            350, wx.ClientDC(self))
        info.WebSite = ("nsmurf.wordpress.com", "Nsmurf's Blog")
        info.Developers = ["Nsmurf"]

        info.License = licenseText

        wx.AboutBox(info)

    def HelpBox(self, evt):
        dlg = wx.MessageDialog(self, "I haven't made a help menu yet, but it shoulden't be that hard to figure out!\n\nGood Luck!",
                               'Help',
                               wx.OK
                               )
        dlg.ShowModal()
        dlg.Destroy()


def main():
    np = wx.App()
    NotPad(None)
    np.MainLoop()    


if __name__ == '__main__':
    main()
