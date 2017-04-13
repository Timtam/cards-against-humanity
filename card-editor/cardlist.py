#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


class CardListWindow(wx.Window):
  def __init__(self, parent):
    wx.Window.__init__(self, parent=parent,
                       name="card list")

    self.SetLabel("card list (this is a label)")
    self.SetBackgroundColour("white")

    columns = 5

    box = wx.BoxSizer(wx.VERTICAL)
    grid = wx.GridSizer(0, columns, 0, 0)

    # fill list with 12 dummy objects
    item_list = [(wx.Window(self, size=(100, 100), name="Dummy 1"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 2"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 3"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 4"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 51"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 6"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 7"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 8"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 9"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 10"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 11"), 0,
                  wx.ALIGN_CENTER),
                 (wx.Window(self, size=(100, 100), name="Dummy 12"), 0,
                  wx.ALIGN_CENTER)]

    grid.AddMany(item_list)

    box.Add(grid, proportion=1, flag=wx.SHAPED)
    self.SetSizer(box)
