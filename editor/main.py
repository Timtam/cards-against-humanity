#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import sqlite3

from cardlist import CardListWindow
from const import *
from current_card import CurrCardWindow
from shared.path import getScriptDirectory

APP_EXIT = 1


class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, title="Card Editor", size=(WIDTH, HEIGHT))

    self.database = None

    # add menubar
    self.initUI()
    self.Center()

    # create a splitter and the teo sub-windows
    splitter = wx.SplitterWindow(self,
                                 style=wx.SP_LIVE_UPDATE | wx.SP_NO_XP_THEME | wx.SP_3D,
                                 name="vertical splitter")
    self.left_window = CardListWindow(splitter)
    self.right_window = CurrCardWindow(splitter)
    # self.left_window.card_grid.buildList()

    # split the frame
    splitter.SplitVertically(self.left_window, self.right_window,
                             (0.7 * WIDTH))
    splitter.SetMinimumPaneSize((WIDTH / 8))  # just to prevent moving sash to
    #   the very right or left and so
    #   you can't move it back
    splitter.SetSashGravity(0.0)
    self.left_window.card_grid.createGrid()

    # listen to changing sash
    splitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.onSashChanging)
    # splitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.onSashChanged)

    # calling the database loading algorithm directly after the window appears
    wx.CallAfter(self.initDatabase)

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

  def initDatabase(self):
    # if no database exists, we will ask to create a new one
    if not os.path.exists(os.path.join(getScriptDirectory(), 'cards.db')):
      result = self.Message(caption="No database found",
                            text="We couldn't find a cards.db file inside the editor's working directory. Do you want us to create a new one for you which you can edit directly afterwards?\nIf no, the editor will close immediately.",
                            style=MSG_YES_NO)
      if result == wx.ID_NO:
        self.Close()
      else:
        self.database = sqlite3.connect(
          os.path.join(getScriptDirectory(), 'cards.db'))
        cursor = self.database.cursor()
        cursor.execute("""
                       CREATE TABLE 'cards' (
                         'id' INTEGER PRIMARY KEY NOT NULL,
                         'text' VARCHAR(1000),
                         'type' TINYINT(1))
                       """)
        cursor.execute("""
                       CREATE TABLE 'config' (
                         'key' VARCHAR(30),
                         'value' VARCHAR(30))
                       """)
        cursor.execute("""
                       INSERT INTO 'config' (
                         'key', 'value') VALUES (
                         ?, ?)
                       """, ('version', '1',))
        self.database.commit()
    else:
      self.database = sqlite3.connect(
        os.path.join(getScriptDirectory(), 'cards.db'))

  def Message(self, caption, text, style):
    message = wx.MessageDialog(parent=self, caption=caption, message=text,
                               style=style)
    result = message.ShowModal()
    message.Destroy()
    return result

  def onQuit(self, e):
    self.Message(caption="Test Error", text="This is a test for errors...",
                 style=MSG_ERROR)
    self.Message(caption="Test Warning", text="This is a test for warnings...",
                 style=MSG_WARN)
    self.Message(caption="Test Information",
                 text="This is a test for information...", style=MSG_INFO)
    self.Message(caption="Test Question",
                 text="This is a test for questions...", style=MSG_YES_NO)
    self.Close()

  def onSashChanging(self, e):
    self.left_window.card_grid.calcBestColumns(self.ClientSize.height)

    # def onSashChanged(self, e):
    # self.Refresh()


def main():
  app = wx.App(False)
  frame = MainFrame()
  frame.Show()
  app.MainLoop()
