#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools

import wx

from const import ELEMENT_SIZE, BORDER, FULL_ELEMENT

# elements have the border on all sides and are centered only horizontally
FLAG = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL


class SearchCtrl(wx.SearchCtrl):
  def __init__(self, *args, **kwargs):
    wx.SearchCtrl.__init__(self, *args, **kwargs)


class CardListWindow(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent,
                               name="card list panel (this is a name")

    self.toolbar = wx.ToolBar(self, -1)
    self.toolbar.SetToolBitmapSize((30, 30))

    self.toolbar.AddStretchableSpace()
    self.search_ctrl = SearchCtrl(parent=self.toolbar)
    self.toolbar.AddControl(self.search_ctrl)
    self.toolbar.Realize()

    self.card_grid = ScrolledGrid(self)


    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.toolbar, proportion=0, flag=wx.EXPAND)
    self.vbox.Add(self.card_grid, proportion=1, flag=wx.EXPAND)

    self.SetSizer(self.vbox)

    self.SetLabel("card list panel(this is a label)")
    self.SetBackgroundColour("black")


class ScrolledGrid(wx.ScrolledWindow):
  def __init__(self, parent):
    wx.ScrolledWindow.__init__(self, parent=parent,
                               name="card list grid(this is a name")

    self.SetLabel("card list grid(this is a label)")
    self.SetBackgroundColour("white")
    self.item_list = []
    # next 2 just for initialization (don't ask about the numbers)
    self.grid = wx.GridSizer(0, 5, 0, 0)
    self.Height = 500


  def initList(self):
    # create list with dummy objects
    for _ in itertools.repeat(None, 55):
      panel = wx.Panel(self, size=(ELEMENT_SIZE, ELEMENT_SIZE),
                                       name="Dummy")
      panel.SetBackgroundColour("black")
      self.item_list.append((panel, 0, FLAG, BORDER))

  def calcBestColumns(self, available_height):
    # this method calculates the number of columns depending on the existence of
    #   a scrollbar, which again depends on the number of elements that fits the
    #   available screen
    # it's kind of a mastermind-method^^ ;)

    # at first calculate columns from the available width and let the grid calc
    #   the rows
    columns = self.ClientSize.width / FULL_ELEMENT
    rows = 0
    self.grid.SetCols(columns)
    (rows, columns) = self.grid.CalcRowsCols()

    # then calculate the possible row from the available height
    possible_rows = available_height / FULL_ELEMENT

    # if rows > possible rows -> there are more rows than rows fitting the
    #   current screen -> scrollbar is needed -> width - 20px as the scrollbar
    #   takes 20 px
    if rows > possible_rows:
      columns = (self.ClientSize.width - 20) / FULL_ELEMENT

    # finally also set the number of columns and return them just to be on the
    #   safe side
    self.grid.SetCols(columns)
    return columns

  def createGrid(self, available_height):
    # this method creates the actual grid with the items

    self.grid.AddMany(self.item_list)

    columns = self.calcBestColumns(available_height)

    # calc and set the virtual height to make the window scrollable
    self.Height = (self.item_list.__len__() / columns) * FULL_ELEMENT
    self.SetVirtualSize((0, self.Height))
    self.SetScrollRate(10, 20)

    # need a horizontal box sizer to make the grid horizontal flexible; i don't
    #   know exactly why, but it works^^
    # otherwise the elements are also centered vertically
    box = wx.BoxSizer(wx.HORIZONTAL)
    box.Add(self.grid, proportion=1)
    self.SetSizer(box)
