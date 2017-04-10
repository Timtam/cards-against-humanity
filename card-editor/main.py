#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


class mainWindow(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(mainWindow, self).__init__(*args, **kwargs)

    self.InitUI()

  def InitUI(self):
    menubar = wx.MenuBar()
    fileMenu = wx.Menu()
    fitem = fileMenu.Append(wx.ID_EXIT, 'Schließen',
                            'Karteneditor schließen')
    menubar.Append(fileMenu, '&File')
    self.SetMenuBar(menubar)

    self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

    self.SetSize((1280, 720))
    self.SetTitle('Karteneditor')
    self.Centre()
    self.Show(True)

  def OnQuit(self, e):
    self.Close()


def main():
  mainApp = wx.App()
  mainWindow(None)
  mainApp.MainLoop()


if __name__ == '__main__':
  main()
