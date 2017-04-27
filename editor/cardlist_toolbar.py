from shared.card import CARD_BLACK, CARD_WHITE

import wx

class SearchCtrl(wx.SearchCtrl):
  def __init__(self, *args, **kwargs):
    wx.SearchCtrl.__init__(self, *args, **kwargs)

    self.ShowSearchButton(True)
    self.ShowCancelButton(True)

class CardListToolbar(wx.ToolBar):
  def __init__(self, parent, id=wx.ID_ANY):
    wx.ToolBar.__init__(self, parent=parent, id=id)
    self.SetToolBitmapSize((30, 30))
    self.checkbox_black = wx.CheckBox(self, label="show black cards")
    self.checkbox_black.SetValue(True)
    self.checkbox_white = wx.CheckBox(self, label="show white cards")
    self.checkbox_white.SetValue(True)
    self.button_new_card = wx.Button(self, label="new card")
    self.button_new_card.Bind(wx.EVT_BUTTON, self.newCard)

    self.AddControl(self.checkbox_black)
    self.AddControl(self.checkbox_white)

    self.AddSeparator()

    self.AddControl(self.button_new_card)
    self.AddControl(wx.Button(self, label="reset all"))
    self.AddControl(wx.Button(self, label="undo all"))

    self.AddSeparator()

    self.AddStretchableSpace()
    self.search_ctrl = SearchCtrl(parent=self)
    self.AddControl(self.search_ctrl)
    self.Realize()

  def newCard(self, event):
    frame = self.GetTopLevelParent()
    cursor = frame.database.cursor()
    cursor.execute("""
                   INSERT INTO cards (
                     text, type) VALUES (
                     ?,?)
                   """, ('', CARD_WHITE, ))
    panel = frame.left_window.card_grid.addCard(id=cursor.lastrowid, text='', card_type=CARD_WHITE)
    frame.left_window.card_grid.createGrid()
    frame.left_window.card_grid.Refresh()
    panel.SetFocus()
