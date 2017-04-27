import wx

from shared.card import CARD_PLACEHOLDER_LENGTH


class CurrCardWindow(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent,
                      name="current card panel(this is a name)")

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
    # self.button_del_card.Bind(wx.EVT_BUTTON, self.DeleteCard)
    self.button_save_card = wx.Button(self, label="save card")
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

  # def DeleteCard(self, event):


  def SaveCard(self, event):
    # get value of textctrl with
    string = self.current_card_text.GetValue()
    # get value of radiobuttons with
    # bool = self.radio_black.GetValue() and
    # bool = self.radio_black.GetValue()

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
    self.current_card_text.SetEditable(False)
    for b in [self.radio_black, self.radio_white, self.button_del_text, self.button_del_card, self.button_save_card, self.button_ins_ph]:
      b.Disable()
