from .const import *
from shared.card import CARD_BLACK, CARD_WHITE

import wx

class SearchCtrl(wx.SearchCtrl):
  def __init__(self, *args, **kwargs):
    wx.SearchCtrl.__init__(self, *args, **kwargs)

    self.search_card_types = [CARD_BLACK, CARD_WHITE]
    self.search_text = ''

    self.ShowSearchButton(True)
    self.ShowCancelButton(True)

    self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearch)
    self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onCancel)
    self.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

  def onSearch(self, e):

    if not self.searchCheck():
      return

    self.search_card_types=[]

    self.search_text = self.GetValue()

    if self.GetParent().checkbox_black.GetValue():
      self.search_card_types.append(CARD_BLACK)

    if self.GetParent().checkbox_white.GetValue():
      self.search_card_types.append(CARD_WHITE)

    self.GetTopLevelParent().loadCards()

    self.GetParent().button_new_card.Disable()

  def onCancel(self, e):
    
    if not self.searchCheck():
      return

    self.search_card_types = [CARD_BLACK, CARD_WHITE]

    self.search_text = ''

    self.SetValue(self.search_text)
    self.GetParent().checkbox_black.SetValue(True)
    self.GetParent().checkbox_white.SetValue(True)

    self.GetTopLevelParent().loadCards()

    self.GetParent().button_new_card.Enable()

  def searchCheck(self):

    frame = self.GetTopLevelParent()

    if not frame.right_window.saved:
      frame.Message(caption="unapplied changes", text="Apply your changes before changing search parameters.", style=MSG_WARN)
      return False

    return True

class CardListToolbar(wx.ToolBar):
  def __init__(self, parent, id=wx.ID_ANY):
    wx.ToolBar.__init__(self, parent=parent, id=id)
    self.SetToolBitmapSize((30, 30))
    self.checkbox_black = wx.CheckBox(self, label="show black cards")
    self.checkbox_black.SetValue(True)
    self.checkbox_white = wx.CheckBox(self, label="show white cards")
    self.checkbox_white.SetValue(True)
    self.button_new_card = wx.Button(self, label="new card")
    self.button_new_card.Bind(wx.EVT_BUTTON, self.onNewCard)

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
    self.search_ctrl = SearchCtrl(parent=self, style=wx.TE_PROCESS_ENTER)
    self.AddControl(self.search_ctrl)
    self.Realize()

  def onNewCard(self, event):
    frame = self.GetTopLevelParent()
    if frame.right_window.maySetCard()==False:
      return
    frame.right_window.related_card = None

    if frame.right_window.radio_black.GetValue():
      card_type = CARD_BLACK
    else:
      card_type = CARD_WHITE

    cursor = frame.database.cursor()
    cursor.execute("""
                   INSERT INTO cards (
                     text, type) VALUES (
                     ?,?)
                   """, ('', card_type, ))
    panel = frame.left_window.card_grid.addCard(id=cursor.lastrowid, text='', card_type=card_type)
    #frame.left_window.card_grid.createGrid()
    frame.left_window.Layout()
    frame.right_window.setCard(panel.card)

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
