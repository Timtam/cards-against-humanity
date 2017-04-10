#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


class MainWindow(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.initUI()

  def initUI(self):
    menubar = wx.MenuBar()
    file_menu = wx.Menu()
    menu_item = file_menu.Append(wx.ID_EXIT, 'Quit',
                                 'Quit application')
    menubar.Append(file_menu, '&File')
    self.SetMenuBar(menubar)

    self.Bind(wx.EVT_MENU, self.onQuit, menu_item)

    self.SetSize((1280, 720))
    self.SetTitle('Card-Editor')
    self.Centre()
    self.Show(True)

  def onQuit(self, e):
    self.Close()


def main():
  app = wx.App()
  MainWindow(None)
  app.MainLoop()


if __name__ == '__main__':
  main()
