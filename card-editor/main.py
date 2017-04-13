#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

from cardlist import CardListWindow

APP_EXIT = 1


class CurrCardWindow(wx.Window):
  def __init__(self, parent):
    wx.Window.__init__(self, parent=parent,
                       name="current card (this is a name)")

    self.SetLabel("current card (this is a label)")
    self.SetBackgroundColour("white")


class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, title="Card Editor", size=(1280, 720))

    # add menubar
    self.initUI()
    self.Centre()

    # create a splitter and the teo sub-windows
    splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE,
                                 name="vertical splitter")
    self.left_window = CardListWindow(splitter)
    right_window = CurrCardWindow(splitter)

    # split the frame
    splitter.SplitVertically(self.left_window, right_window,
                             320)  # TODO: calculate initial sash position 75 % of frame width
    splitter.SetMinimumPaneSize(
      160)  # just to prevent moving sash to the very right or left and so you can't move it back
    splitter.SetSashGravity(0.5)

    # listen to changing sash
    splitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.onSashChanging)

  def initUI(self):
    menubar = wx.MenuBar()
    file_menu = wx.Menu()
    # menu_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
    menu_item = wx.MenuItem(file_menu, APP_EXIT,
                            "&Quit\tCtrl+Q")  # underlined Q
    file_menu.AppendItem(menu_item)

    self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)
    menubar.Append(file_menu, "&File")
    self.SetMenuBar(menubar)

    # self.Bind(wx.EVT_MENU, self.onQuit, menu_item)

  def onQuit(self, e):
    self.Close()

  def onSashChanging(self, e):
    # calculate new number of columns through the window has been resized
    columns = e.GetSashPosition() / 120  # TODO: calculate divisor from element size (+ border)

    # there shouldn't be more columns than item in the list (otherwise there would be free columns with size of the other elements
    if columns > self.left_window.item_list.__len__():
      columns = self.left_window.item_list.__len__()

    self.left_window.grid.SetCols(columns)


def main():
  app = wx.App(False)
  frame = MainFrame()
  frame.Show()
  app.MainLoop()


if __name__ == "__main__":
  main()
