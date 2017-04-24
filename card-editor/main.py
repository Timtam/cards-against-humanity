#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

from cardlist import CardListWindow
from const import WIDTH, HEIGHT

APP_EXIT = 1


class CurrCardWindow(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent,
                       name="current card panel(this is a name)")

    self.SetLabel("current card panel(this is a label)")
    self.SetBackgroundColour("white")

    #self.current_card = wx.Panel(parent=self, size=(200, 200), name="current card (name)")
    #self.current_card.SetLabel("current card (label)")
    #self.current_card.SetBackgroundColour("black")

    self.box = wx.BoxSizer(wx.VERTICAL)
    self.box.Add(wx.RadioButton(self, label="black card"))
    self.box.Add(wx.RadioButton(self, label="white card"))
    self.box.AddStretchSpacer(1)
    #self.box.Add(self.current_card, 0, wx.ALIGN_CENTER)
    self.box.AddStretchSpacer(1)
    self.hbox = wx.BoxSizer()
    self.hbox.Add(wx.Button(self, label="Delete Text"), 1)
    self.hbox.AddStretchSpacer(5)
    self.hbox.Add(wx.Button(self, label="Delete Card"), 1)
    self.hbox.AddStretchSpacer(5)
    self.hbox.Add(wx.Button(self, label="Insert Placeholder"), 1)
    self.box.Add(self.hbox)
    self.SetSizer(self.box)


class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, title="Card Editor", size=(WIDTH, HEIGHT))

    # add menubar
    self.initUI()
    self.Center()

    # create a splitter and the teo sub-windows
    splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE | wx.SP_NO_XP_THEME | wx.SP_3D, name="vertical splitter")
    self.left_window = CardListWindow(splitter)
    self.right_window = CurrCardWindow(splitter)
    #self.left_window.card_grid.initList()

    # split the frame
    splitter.SplitVertically(self.left_window, self.right_window, (0.70 * WIDTH))
    splitter.SetMinimumPaneSize((WIDTH / 8))  # just to prevent moving sash to
    #   the very right or left and so
    #   you can't move it back
    splitter.SetSashGravity(0.0)
    self.left_window.card_grid.createGrid(self.ClientSize.height)

    # listen to changing sash
    splitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.onSashChanging)


  def initUI(self):
    menubar = wx.MenuBar()
    file_menu = wx.Menu()
    # menu_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
    menu_item = wx.MenuItem(file_menu, APP_EXIT,
                            "&Quit\tCtrl+Q")  # an underlined and linked Q (Ctrl
    #   + Q also quits)
    file_menu.AppendItem(menu_item)

    self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)
    menubar.Append(file_menu, "&File")
    self.SetMenuBar(menubar)

    # self.Bind(wx.EVT_MENU, self.onQuit, menu_item)


  def onQuit(self, e):
    self.Close()


  def onSashChanging(self, e):
    self.left_window.card_grid.calcBestColumns(self.ClientSize.height)


def main():
  app = wx.App(False)
  frame = MainFrame()
  frame.Show()
  app.MainLoop()


if __name__ == "__main__":
  main()
