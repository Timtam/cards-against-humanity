#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

# elements have the border on all sides and are centered only horizontally
FLAG = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL
BORDER = 10


class CardListWindow(wx.Window):
  def __init__(self, parent):
    wx.Window.__init__(self, parent=parent, name="card list (this is a name")

    self.SetLabel("card list (this is a label)")
    self.SetBackgroundColour("white")

    columns = 960 / 120  # TODO: calculate dividend from screen width and sash position, divisor from element size (+ border)

    # need a horizontal box sizer, i don't know exactly why, but it works^^
    # otherwise the elements are also centered vertically
    box = wx.BoxSizer(wx.HORIZONTAL)
    self.grid = wx.GridSizer(0, columns, 0, 0)

    # fill list with 13 dummy objects
    self.item_list = \
      [(wx.Window(self, size=(100, 100), name="Dummy 1"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 2"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 3"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 4"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 5"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 6"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 7"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 8"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 9"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 10"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 11"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 12"), 0, FLAG, BORDER),
       (wx.Window(self, size=(100, 100), name="Dummy 13"), 0, FLAG, BORDER)]

    self.grid.AddMany(self.item_list)

    box.Add(self.grid, proportion=1)
    self.SetSizer(box)
