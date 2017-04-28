from .const import *
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

    self.button_save_all = wx.Button(self, label="save changes")
    self.button_save_all.Bind(wx.EVT_BUTTON, self.onSaveAll)
    self.button_undo_all = wx.Button(self, label="undo all")
    self.button_undo_all.Bind(wx.EVT_BUTTON, self.onUndoAll)

    self.AddControl(self.checkbox_black)

    self.AddControl(self.checkbox_white)

    self.AddSeparator()

    self.AddControl(self.button_new_card)
    self.AddControl(self.button_save_all)
    self.AddControl(self.button_undo_all)

    self.AddSeparator()

    self.AddStretchableSpace()
    self.search_ctrl = SearchCtrl(parent=self)
    self.AddControl(self.search_ctrl)
    self.Realize()

  def newCard(self, event):
    frame = self.GetTopLevelParent()
    if frame.right_window.maySetCard()==False:
      return
    frame.right_window.related_card = None
    cursor = frame.database.cursor()
    cursor.execute("""
                   INSERT INTO cards (
                     text, type) VALUES (
                     ?,?)
                   """, ('', CARD_WHITE, ))
    panel = frame.left_window.card_grid.addCard(id=cursor.lastrowid, text='', card_type=CARD_WHITE)
    #frame.left_window.card_grid.createGrid()
    frame.left_window.Layout()
    frame.right_window.setCard(panel)

  def onSaveAll(self, e):

    frame = self.GetTopLevelParent()

    if frame.right_window.saved==False:
      frame.Message(caption="unapplied changes", text="Apply your latest changes first before saving", style=MSG_INFO)
      return

    frame.database.cursor().execute('VACUUM')
    frame.database.commit()

    frame.unsaved_changes = False

  def onUndoAll(self, e):

    frame = self.GetTopLevelParent()

    if not frame.right_window.saved:
      frame.Message(caption="unapplied changes", text="Your edit window contains unapplied changes. You need to apply your changes or revert them in order to undo all your applied changes.", style=MSG_WARN)
      return

    frame.database.rollback()

    frame.right_window.Disable()

    frame.loadCards()

    frame.unsaved_changes = False
