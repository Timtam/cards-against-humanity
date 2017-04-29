from .const import *
from shared.card import CARD_PLACEHOLDER_LENGTH, CARD_BLACK, CARD_WHITE
from shared.exceptions import CardValidityError

import wx

class CurrCardWindow(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent,
                      name="current card panel(this is a name)")
    self.related_card = None

    self.SetLabel("current card panel(this is a label)")
    self.SetBackgroundColour("white")

    self.current_card_panel = wx.Panel(parent=self, size=(200, 200),
                                       name="current card (name)",
                                       style=wx.SIMPLE_BORDER)
    self.current_card_panel.SetLabel("current card (label)")
    self.current_card_panel.SetBackgroundColour("black")
    self.current_card_text = wx.TextCtrl(parent=self.current_card_panel, id=-1,
                                         size=(150, 150),
                                         style=wx.TE_MULTILINE,
                                         name="text control for current card")
    self.current_card_text.SetBackgroundColour(
      self.current_card_panel.GetBackgroundColour())
    self.current_card_text.SetForegroundColour("white")
    text_box = wx.BoxSizer()
    text_box.Add(self.current_card_text, 1, wx.ALL | wx.EXPAND, 30)
    self.current_card_panel.SetSizer(text_box)

    self.radio_black = wx.RadioButton(self, label="black card", )
    self.radio_black.SetValue(True)
    self.radio_black.Bind(wx.EVT_RADIOBUTTON, self.SetColors)
    self.radio_white = wx.RadioButton(self, label="white card")
    self.radio_white.Bind(wx.EVT_RADIOBUTTON, self.SetColors)

    self.button_del_text = wx.Button(self, label="delete text")
    self.button_del_text.Bind(wx.EVT_BUTTON, self.DeleteCardText)
    self.button_del_card = wx.Button(self, label="delete card")
    self.button_del_card.Bind(wx.EVT_BUTTON, self.DeleteCard)
    self.button_save_card = wx.Button(self, label="apply card changes")
    self.button_save_card.Bind(wx.EVT_BUTTON, self.SaveCard)
    self.button_ins_ph = wx.Button(self, label="insert placeholder")
    self.button_ins_ph.Bind(wx.EVT_BUTTON, self.InsertPlaceholder)

    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.AddSpacer(20)
    self.vbox.Add(self.radio_black)
    self.vbox.Add(self.radio_white)

    self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    self.vbox.Add(wx.StaticLine(self), 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 20)
    self.hbox2.AddSpacer(20)
    self.hbox2.Add(self.current_card_panel, 1, wx.ALIGN_CENTER | wx.SHAPED)
    self.hbox2.AddSpacer(20)
    self.vbox.Add(self.hbox2, 1, wx.EXPAND)
    self.vbox.Add(wx.StaticLine(self), 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 20)

    self.hbox = wx.BoxSizer()
    self.grid = wx.GridBagSizer()
    self.grid.Add(self.button_del_text, (0, 0))
    self.grid.Add(self.button_ins_ph, (0, 2), flag=wx.ALIGN_RIGHT)
    self.grid.Add(self.button_del_card, (1, 0))
    self.grid.Add(self.button_save_card, (1, 2), flag=wx.ALIGN_RIGHT)
    self.grid.AddGrowableCol(1)

    self.hbox.Add(self.grid, 1, wx.EXPAND)
    self.vbox.Add(self.hbox, 0, wx.EXPAND)
    self.SetSizer(self.vbox)

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
    cursor.execute('DELETE FROM cards WHERE id = ?', (self.related_card.id, ))

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
      frame.Message(caption="card text error", text=e.message['text'], style=MSG_WARN)
      self.related_card.type = old_type
      return False

    frame.left_window.card_grid.getCard(self.related_card).text.SetLabel(self.related_card.getCardText())

    cursor = frame.database.cursor()
    cursor.execute('UPDATE cards SET text = ?, type = ? WHERE id = ?', (self.related_card.getInternalText(), self.related_card.type, self.related_card.id, ))

    frame.unsaved_changes = True

    return True

  def InsertPlaceholder(self, event):
    current_text = self.current_card_text.GetValue()
    current_position = self.current_card_text.GetInsertionPoint()
    current_text = current_text[
                   :current_position] + "_" * CARD_PLACEHOLDER_LENGTH + current_text[
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
    for b in [self.radio_black, self.radio_white, self.button_del_text, self.button_del_card, self.button_save_card, self.button_ins_ph]:
      b.Disable()

  def Enable(self):
    self.current_card_panel.Show()
    self.Layout()
    for b in [self.radio_black, self.radio_white, self.button_del_text, self.button_del_card, self.button_save_card, self.button_ins_ph]:
      b.Enable()

  def setCard(self, card):

    if self.related_card is not card:

      if self.maySetCard()==False:
        return

      self.related_card = card

    self.current_card_text.SetValue(card.getCardText())
    if card.type == CARD_BLACK:
      self.radio_black.SetValue(True)
      self.radio_white.SetValue(False)
    elif card.type == CARD_WHITE:
      self.radio_black.SetValue(False)
      self.radio_white.SetValue(True)

    self.SetColors(None)
    self.Enable()
    self.current_card_text.SetFocus()

  # this will check if the current card was saved already
  # and if not, the user will be asked to dump his changes
  def maySetCard(self):

    if self.related_card == None:
      return True

    if self.saved:
      return True

    frame = self.GetTopLevelParent()
    if frame.Message(caption="Unsaved changes", text="You didn't save the currently editing card yet. Do you want to discard your changes?", style=MSG_YES_NO) == wx.ID_YES:
      # that's a newly created card
      # we can't leave them alive, since they would be blank
      if self.related_card.getCardText()=='':
        cursor = frame.database.cursor()
        cursor.execute('DELETE FROM cards WHERE id = ? AND text = ? AND type = ?', (self.related_card.id, self.related_card.getInternalText(), self.related_card.type, ))
        frame.left_window.card_grid.deleteCard(self.related_card)
      return True

    return False

  @property
  def saved(self):

    if self.related_card == None:
      return True

    # all cards without text can't be saved yet
    if self.current_card_text.GetValue().strip(' ')=='':
      return False

    if self.radio_black.GetValue():
      card_type = CARD_BLACK
    elif self.radio_white.GetValue():
      card_type = CARD_WHITE

    if self.related_card.formatInternalText(self.current_card_text.GetValue()) != self.related_card.getInternalText() or card_type != self.related_card.type:
      return False

    return True
