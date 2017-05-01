from shared.card import CARD_BLACK, CARD_PLACEHOLDER_LENGTH, CARD_WHITE
from shared.exceptions import CardValidityError
from .const import *



class CurrCardWindow(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent,
                      name="current card panel(this is a name)")
    self.related_card = None
    
    self.SetLabel("no card to be edited")
    self.SetBackgroundColour("white")
    self.SetMinSize((274, -1))
    
    # radio buttons
    self.radio_black = wx.RadioButton(self, label="black card", )
    self.radio_black.SetValue(True)
    self.Bind(wx.EVT_RADIOBUTTON, self.SetColors)
    self.radio_white = wx.RadioButton(self, label="white card")
    
    # pane and text control for card
    self.current_card_panel = wx.Panel(parent=self, size=(200, 200),
                                       name="current card (name)",
                                       style=wx.SIMPLE_BORDER)
    self.current_card_panel.SetLabel("current card (label)")
    self.current_card_panel.SetBackgroundColour("black")
    self.current_card_text = wx.TextCtrl(parent=self.current_card_panel, id=-1,
                                         size=(150, 150),
                                         style=wx.TE_MULTILINE | wx.NO_BORDER,
                                         name="text control for current card")
    self.current_card_text.SetBackgroundColour(
      self.current_card_panel.GetBackgroundColour())
    self.current_card_text.SetForegroundColour("white")
    text_box = wx.BoxSizer()
    text_box.Add(self.current_card_text, 1, wx.ALL | wx.EXPAND, 20)
    self.current_card_panel.SetSizer(text_box)
    
    # card edit buttons
    self.button_del_text = wx.Button(self, label="delete text")
    self.button_del_text.Bind(wx.EVT_BUTTON, self.DeleteCardText)
    self.button_del_card = wx.Button(self, label="delete card")
    self.button_del_card.Bind(wx.EVT_BUTTON, self.DeleteCard)
    self.button_save_card = wx.Button(self, label="apply card changes")
    self.button_save_card.Bind(wx.EVT_BUTTON, self.SaveCard)
    self.button_ins_ph = wx.Button(self, label="insert placeholder")
    self.button_ins_ph.Bind(wx.EVT_BUTTON, self.InsertPlaceholder)
    
    # sizers:
    # radio buttons
    self.radiobox_black = wx.BoxSizer(wx.HORIZONTAL)
    self.radiobox_black.AddSpacer(20)
    self.radiobox_black.Add(self.radio_black)
    self.radiobox_white = wx.BoxSizer(wx.HORIZONTAL)
    self.radiobox_white.AddSpacer(20)
    self.radiobox_white.Add(self.radio_white)
    self.radios = wx.WrapSizer()
    self.radios.AddMany([self.radiobox_black, self.radiobox_white])
    
    # card box
    self.cardbox = wx.BoxSizer(wx.HORIZONTAL)
    self.cardbox.AddSpacer(20)
    self.cardbox.Add(self.current_card_panel, 1, wx.ALIGN_CENTER | wx.SHAPED)
    self.cardbox.AddSpacer(20)
    
    # buttons
    self.buttongrid = wx.GridBagSizer(5, 5)
    self.buttongrid.Add(self.button_del_text, (0, 0), flag=wx.ALIGN_LEFT)
    self.buttongrid.Add(self.button_ins_ph, (0, 2), flag=wx.ALIGN_RIGHT)
    self.buttongrid.Add(self.button_del_card, (1, 0), flag=wx.ALIGN_LEFT)
    self.buttongrid.Add(self.button_save_card, (1, 2), flag=wx.ALIGN_RIGHT)
    self.buttongrid.AddGrowableCol(1)
    
    self.buttonbox = wx.BoxSizer(wx.HORIZONTAL)
    self.buttonbox.Add(self.buttongrid, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL,
                       5)
    
    # main sizer
    self.mainbox = wx.BoxSizer(wx.VERTICAL)
    self.mainbox.AddSpacer(20)
    self.mainbox.Add(self.radios)
    self.mainbox.Add(wx.StaticLine(self), 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 20)
    self.mainbox.Add(self.cardbox, 1, wx.EXPAND)
    self.mainbox.Add(wx.StaticLine(self), 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 20)
    self.mainbox.Add(self.buttonbox, 0, wx.EXPAND)
    
    self.SetSizer(self.mainbox)
    
    self.SetAutoLayout(True)
    
    # disable all elements at the very beginning
    self.Disable()
  
  
  def SetColors(self, event):
    if self.radio_black.GetValue():
      self.current_card_panel.SetBackgroundColour("black")
      self.current_card_text.SetBackgroundColour("black")
      self.current_card_text.SetForegroundColour("white")
      self.button_ins_ph.Enable()
    else:
      self.current_card_panel.SetBackgroundColour("white")
      self.current_card_text.SetBackgroundColour("white")
      self.current_card_text.SetForegroundColour("black")
      self.button_ins_ph.Disable()
    
    self.Refresh()
  
  
  def DeleteCardText(self, event):
    self.current_card_text.SetValue('')
  
  
  def DeleteCard(self, event):
    
    frame = self.GetTopLevelParent()
    cursor = frame.database.cursor()
    cursor.execute('DELETE FROM cards WHERE id = ?', (self.related_card.id,))
    
    frame.left_window.card_grid.deleteCard(self.related_card)
    self.Disable()
    
    frame.unsaved_changes = True
  
  
  def SaveCard(self, event):
    
    if self.saved:
      return False
    
    frame = self.GetTopLevelParent()
    
    old_type = self.related_card.type
    
    if self.radio_black.GetValue():
      self.related_card.type = CARD_BLACK
    elif self.radio_white.GetValue():
      self.related_card.type = CARD_WHITE
    
    try:
      self.related_card.setCardText(self.current_card_text.GetValue())
    except CardValidityError as e:
      frame.Message(caption="card text error", text=e.message['text'],
                    style=MSG_WARN)
      self.related_card.type = old_type
      return False
    
    grid_card_panel = frame.left_window.card_grid.getCard(self.related_card)
    grid_card_panel.text.SetLabel(self.related_card.getCardText())
    grid_card_panel.setColors()
    grid_card_panel.Refresh()
    frame.left_window.Layout()
    
    cursor = frame.database.cursor()
    cursor.execute('UPDATE cards SET text = ?, type = ? WHERE id = ?', (
      self.related_card.getInternalText(), self.related_card.type,
      self.related_card.id,))
    
    frame.unsaved_changes = True
    
    return True
  
  
  def InsertPlaceholder(self, event):
    current_text = self.current_card_text.GetValue()
    current_position = self.current_card_text.GetInsertionPoint()
    current_text = current_text[
                   :current_position] + "_" * CARD_PLACEHOLDER_LENGTH + \
                   current_text[
                   current_position:]
    self.current_card_text.SetValue(current_text)
    self.current_card_text.SetInsertionPoint(
      current_position + CARD_PLACEHOLDER_LENGTH)
    self.current_card_text.SetFocus()
  
  
  # will disable all components
  # will be default at creation time, since no card is actually selected
  def Disable(self):
    self.related_card = None
    self.current_card_panel.Hide()
    
    self.GetTopLevelParent().getMenuItem("&File", "Apply changes").Enable(False)
    
    for b in [self.radio_black, self.radio_white, self.button_del_text,
              self.button_del_card, self.button_save_card, self.button_ins_ph]:
      b.Disable()
  
  
  def Enable(self):
    self.current_card_panel.Show()
    self.Layout()
    for b in [self.radio_black, self.radio_white, self.button_del_text,
              self.button_del_card, self.button_save_card, self.button_ins_ph,
              self.GetTopLevelParent().getMenuItem("&File", "Apply changes")]:
      b.Enable()
  
  
  def setCard(self, card):
    
    if self.related_card is not card:
      
      if self.maySetCard() is False:
        return
      
      self.related_card = card
    
    self.current_card_text.SetValue(card.getCardText())
    if card.type == CARD_BLACK:
      self.radio_black.SetValue(True)
      self.radio_white.SetValue(False)
      self.button_ins_ph.Enable()
    elif card.type == CARD_WHITE:
      self.radio_black.SetValue(False)
      self.radio_white.SetValue(True)
      self.button_ins_ph.Disable()
    
    self.SetColors(None)
    self.Enable()
    self.current_card_text.SetFocus()
  
  
  # this will check if the current card was saved already
  # and if not, the user will be asked to dump his changes
  def maySetCard(self):
    
    if self.related_card is None:
      return True
    
    if self.saved:
      return True
    
    frame = self.GetTopLevelParent()
    if frame.Message(caption="Unsaved changes",
                     text="You didn't save the currently editing card yet. Do "
                          "you want to discard your changes?",
                     style=MSG_YES_NO) == wx.ID_YES:
      # that's a newly created card
      # we can't leave them alive, since they would be blank
      if self.related_card.getCardText() == '':
        cursor = frame.database.cursor()
        cursor.execute(
          'DELETE FROM cards WHERE id = ? AND text = ? AND type = ?', (
            self.related_card.id, self.related_card.getInternalText(),
            self.related_card.type,))
        frame.left_window.card_grid.deleteCard(self.related_card)
      return True
    
    return False
  
  
  @property
  def saved(self):
    
    if self.related_card is None:
      return True
    
    # all cards without text can't be saved yet
    if self.current_card_text.GetValue().strip(' ') == '':
      return False
    
    if self.radio_black.GetValue():
      card_type = CARD_BLACK
    elif self.radio_white.GetValue():
      card_type = CARD_WHITE
    
    if self.related_card.formatInternalText(
            self.current_card_text.GetValue()) != \
            self.related_card.getInternalText() or card_type != \
            self.related_card.type:
      return False
    
    return True
  
  
  def setColors(self, card_panel):
    if card_panel.card.type is CARD_BLACK:
      card_panel.SetBackgroundColour("black")
      card_panel.text.SetBackgroundColour("black")
      card_panel.text.SetForegroundColour("white")
    else:
      card_panel.SetBackgroundColour("white")
      card_panel.text.SetBackgroundColour("white")
      card_panel.text.SetForegroundColour("black")



def onEraseBackGround(e):
  # do nothing
  # for flicker-fix
  None
