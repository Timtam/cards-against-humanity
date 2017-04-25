import wx


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
    self.current_card_text.CenterOnParent()


    self.radio_black = wx.RadioButton(self, label="black card", )
    self.radio_black.SetValue(True)
    self.radio_black.Bind(wx.EVT_RADIOBUTTON, self.SetColors)
    self.radio_white = wx.RadioButton(self, label="white card")
    self.radio_white.Bind(wx.EVT_RADIOBUTTON, self.SetColors)


    self.button_del_text = wx.Button(self, label="delete text")
    #self.button_del_text.Bind(wx.EVT_BUTTON, self.DeleteCardText)
    self.button_del_card = wx.Button(self, label="delete card")
    #self.button_del_card.Bind(wx.EVT_BUTTON, self.DeleteCard)
    self.button_save_card = wx.Button(self, label="save card")
    self.button_save_card.Bind(wx.EVT_BUTTON, self.SaveCard)
    self.button_ins_ph = wx.Button(self, label="insert placeholder")
    #self.button_ins_ph.Bind(wx.EVT_BUTTON, self.InsertPlacholder)


    self.box = wx.BoxSizer(wx.VERTICAL)

    self.box.Add(self.radio_black)
    self.box.Add(self.radio_white)

    self.box.AddStretchSpacer(1)
    self.box.Add(self.current_card_panel, 0, wx.ALIGN_CENTER)
    self.box.AddStretchSpacer(1)

    self.hbox = wx.BoxSizer()
    self.grid = wx.GridBagSizer()
    self.grid.Add(self.button_del_text, (0, 0))
    self.grid.Add(self.button_ins_ph, (0, 2), flag=wx.ALIGN_RIGHT)
    self.grid.Add(self.button_del_card, (1, 0))
    self.grid.Add(self.button_save_card, (1, 2), flag=wx.ALIGN_RIGHT)
    self.grid.AddGrowableCol(1)

    self.hbox.Add(self.grid, 1, wx.EXPAND)
    self.box.Add(self.hbox, 0, wx.EXPAND)
    self.SetSizer(self.box)


  def SetColors(self, event):
    if self.radio_black.GetValue():
      self.current_card_panel.SetBackgroundColour("black")
      self.current_card_text.SetBackgroundColour("black")
      self.current_card_text.SetForegroundColour("white")
    else:
      self.current_card_panel.SetBackgroundColour("white")
      self.current_card_text.SetBackgroundColour("white")
      self.current_card_text.SetForegroundColour("black")

    self.Refresh()


  #def DeleteCardText(self, event):


  #def DeleteCard(self, event):


  def SaveCard(self, event):
    # get value of textctrl with
    string = self.current_card_text.GetValue()
    # get value of radiobuttons with
    #bool = self.radio_black.GetValue() and
    #bool = self.radio_black.GetValue()

  #def InsertPlaceholder(self, event):

