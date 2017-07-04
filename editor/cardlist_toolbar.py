from shared.card import CARD_BLACK, CARD_WHITE
from .const import *



class SearchCtrl(wx.SearchCtrl):
  def __init__(self, *args, **kwargs):
    wx.SearchCtrl.__init__(self, *args, **kwargs)
    
    frame = self.GetTopLevelParent()

    self.SetName(frame.translator.translate("Card search"))
    self.ShowSearchButton(False)
    self.ShowCancelButton(True)
    
    self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onCancel)
    self.Bind(wx.EVT_TEXT, self.GetParent().onSearch)
    
    # fix flickering
    for child in self.GetChildren():
      child.Bind(wx.EVT_ERASE_BACKGROUND, onEraseBackGround)
  
  
  def onCancel(self, e):
    parent = self.GetParent()
    frame = self.GetTopLevelParent()
    
    if not parent.searchCheck():
      return
    
    self.EvtHandlerEnabled = False
    parent.EvtHandlerEnabled = False
    self.SetValue('')
    parent.checkbox_black.SetValue(True)
    parent.checkbox_white.SetValue(True)
    self.EvtHandlerEnabled = True
    parent.EvtHandlerEnabled = True
    
    frame.loadCards()
    frame.right_window.Disable()
    
    frame.getMenuItem(frame.translator.translate("&File"), frame.translator.translate("New card")).Enable(True)
    parent.button_new_card.Enable()



class CardListToolbar(wx.ToolBar):
  def __init__(self, parent):
    wx.ToolBar.__init__(self, parent=parent, style=wx.TB_FLAT, name="car list toolbar")

    frame = self.GetTopLevelParent()

    self.SetToolBitmapSize((23, 23))
    
    # checkboxes for black and white
    self.checkbox_black = wx.CheckBox(self, label=frame.translator.translate("Show black cards"))
    self.checkbox_black.SetValue(True)
    self.checkbox_white = wx.CheckBox(self, label=frame.translator.translate("Show white cards"))
    self.checkbox_white.SetValue(True)
    self.Bind(wx.EVT_CHECKBOX, self.onSearch)
    
    # fix flickering
    self.checkbox_black.Bind(wx.EVT_ERASE_BACKGROUND, onEraseBackGround)
    self.checkbox_white.Bind(wx.EVT_ERASE_BACKGROUND, onEraseBackGround)
    
    # buttons
    self.button_new_card = wx.Button(self, label=frame.translator.translate("New card"))
    self.button_new_card.Bind(wx.EVT_BUTTON, self.onNewCard)
    self.button_save_all = wx.Button(self, label=frame.translator.translate("Save changes"))
    self.button_save_all.Bind(wx.EVT_BUTTON, self.onSaveAll)
    self.button_undo_all = wx.Button(self, label=frame.translator.translate("Undo all"))
    self.button_undo_all.Bind(wx.EVT_BUTTON, self.onUndoAll)
    
    # card counter
    self.card_counter = wx.StaticText(self, label=frame.translator.translate("Card counter") + ": 0")
    
    # search control
    self.search_ctrl = SearchCtrl(parent=self)
    
    # toolbar:
    # some space...
    self.AddSeparator()
    
    # checkboxes
    self.AddControl(self.checkbox_black)
    self.AddControl(self.checkbox_white)
    
    self.AddSeparator()
    
    # buttons
    self.AddControl(self.button_new_card)
    self.AddControl(self.button_save_all)
    self.AddControl(self.button_undo_all)
    
    self.AddSeparator()
    
    # card counter
    self.AddControl(self.card_counter)
    
    self.AddStretchableSpace()
    self.AddSeparator()
    
    # search control
    self.AddControl(self.search_ctrl)
    
    #self.Realize()
  
  
  def onNewCard(self, event):
    frame = self.GetTopLevelParent()
    if frame.right_window.maySetCard() is False:
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
                   """, ('', card_type,))
    panel = frame.left_window.card_grid.addCard(card_id=cursor.lastrowid, text='',
                                                card_type=card_type)
    frame.card_counter += 1
    self.updateCardCounter()
    frame.left_window.Layout()
    frame.right_window.setCard(panel.card)
    panel.onClick(event)
  
  
  def onSaveAll(self, e):
    
    frame = self.GetTopLevelParent()
    
    if frame.right_window.saved is False:
      frame.Message(caption="unapplied changes",
                    text="Apply your latest changes first before saving",
                    style=MSG_INFO)
      return
    
    cursor = frame.database.cursor()
    
    cursor.execute('VACUUM')
    
    frame.database.commit()
    
    frame.unsaved_changes = False
  
  
  def onUndoAll(self, e):
    
    frame = self.GetTopLevelParent()
    
    if not frame.right_window.saved:
      frame.Message(caption="unapplied changes",
                    text="Your edit window contains unapplied changes. You "
                         "need to apply your changes or revert them in order "
                         "to undo all your applied changes.",
                    style=MSG_WARN)
      return
    
    frame.database.rollback()
    
    frame.right_window.Disable()
    
    frame.loadCards()
    
    frame.unsaved_changes = False
  
  
  def onSearch(self, event):
    
    if self.searchCheck():
      frame = self.GetTopLevelParent()
      frame.loadCards(False)
      frame.right_window.Disable()
      if self.search_ctrl.GetValue() != '' or not \
              self.checkbox_black.GetValue() or not \
              self.checkbox_white.GetValue():
        frame.getMenuItem(frame.translator.translate("&File"), frame.translator.translate("New card")).Enable(False)
        self.button_new_card.Disable()
      else:
        frame.getMenuItem(frame.translator.translate("&File"), frame.translator.translate("New card")).Enable(True)
        self.button_new_card.Enable()
    
    else:
      # we need to reset black and white checkboxes to their original state
      # and also the textbox
      # but to prevent multiple error messages we must disable this event
      # handler for the time being
      self.EvtHandlerEnabled = False
      self.search_ctrl.EvtHandlerEnabled = False
      if event.GetEventObject() == self.checkbox_black:
        self.checkbox_black.SetValue(True)
      elif event.GetEventObject() == self.checkbox_white:
        self.checkbox_white.SetValue(True)
      elif event.GetEventObject() == self.search_ctrl:
        self.search_ctrl.SetValue(self.search_ctrl.GetValue()[:-1])
      self.EvtHandlerEnabled = True
      self.search_ctrl.EvtHandlerEnabled = True
  
  
  def searchCheck(self):
    
    frame = self.GetTopLevelParent()
    
    if not frame.right_window.saved:
      frame.Message(caption="unapplied changes",
                    text="Apply your changes before changing search parameters.",
                    style=MSG_WARN)
      return False
    
    return True

  def updateCardCounter(self):

    frame = self.GetTopLevelParent()

    self.card_counter.SetLabel(frame.translator.translate("Card counter")+": "+str(frame.card_counter))

    self.Realize()

def onEraseBackGround(e):
  # do nothing
  # for flicker-fix
  pass
