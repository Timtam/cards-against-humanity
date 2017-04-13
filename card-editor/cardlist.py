#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

STYLE = wx.ALL
BORDER = 0


class CardListWindow(wx.Window):
  def __init__(self, parent):
    wx.Window.__init__(self, parent=parent,
                       name="card list")

    self.SetLabel("card list (this is a label)")
    self.SetBackgroundColour("white")

    box = wx.BoxSizer(wx.VERTICAL)
    self.grid = wx.GridSizer(0, 9, 0, 0)

    # fill list with 12 dummy objects
    item_list = \
      [(wx.Window(self, size=(100, 100), name="Dummy 1"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 2"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 3"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 4"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 5"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 6"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 7"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 8"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 9"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 10"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 11"), 0, STYLE, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 12"), 0, STYLE, BORDER)]

    self.grid.AddMany(item_list)

    box.Add(self.grid, proportion=1, flag=wx.EXPAND)
    self.SetSizer(box)
