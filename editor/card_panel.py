from const import *
from shared.card import CARD_BLACK, CARD_WHITE, Card



class CardPanel(wx.Panel):
  def __init__(self, parent, card_id=-1, size=(ELEMENT_SIZE, ELEMENT_SIZE),
               text="",
               card_type=CARD_WHITE):
    wx.Panel.__init__(self, parent=parent, id=card_id, size=size,
                      name=("card " + `card_id`), style=wx.SIMPLE_BORDER)
    self.card = Card(id=card_id, text=text, type=card_type)
    
    # subpanel for more free space between panel-border and text
    self.subpanel = wx.Panel(self)
    self.text = CardText(parent=self.subpanel, text=self.card.getCardText())
    
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(self.text, 1, wx.ALL | wx.EXPAND, 10)
    self.subpanel.SetSizer(box)
    
    box2 = wx.BoxSizer(wx.VERTICAL)
    box2.Add(self.subpanel, 1, wx.ALL | wx.EXPAND, 10)
    self.SetSizer(box2)
    
    self.setColors()
    
    # click
    self.Bind(wx.EVT_LEFT_UP, self.onClick)
    self.subpanel.Bind(wx.EVT_LEFT_UP, self.onClick)
    self.text.Bind(wx.EVT_LEFT_UP, self.onClick)
    
    # hover - right, i need them all, because the text lays in the panel;
    # when you move mouse into the text, you will first enter the panel,
    # then enter the subpanel and in the same time leave the panel again,
    # then enter the text and leave the subpanel;
    # the same thing happens on leaving: in text -> enter subpanel & leave text
    # -> enter panel & leave subpanel
    # i solved this using the flags below, kind of strange that it needs so
    # much lines...
    self.Bind(wx.EVT_ENTER_WINDOW, self.onEnteringPanel)
    self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeavingPanel)
    self.subpanel.Bind(wx.EVT_ENTER_WINDOW, self.onEnteringSubPanel)
    self.subpanel.Bind(wx.EVT_LEAVE_WINDOW, self.onLeavingSubPanel)
    self.text.Bind(wx.EVT_ENTER_WINDOW, self.onEnteringText)
    self.text.Bind(wx.EVT_LEAVE_WINDOW, self.onLeavingText)
    # for navigation per keys
    self.Bind(wx.EVT_CHILD_FOCUS, self.onEnteringPanel)
    self.Bind(wx.EVT_KILL_FOCUS, self.onLeavingPanel)
    # some necessary flags
    self.entered_panel = self.entered_subpanel = self.entered_text = \
      self.clicked = False
    
    self.Bind(wx.EVT_KEY_UP, self.onKeyPress)
  
  
  def onClick(self, event):
    # print ("clicked on " + self.GetName())
    self.clicked = True
    # if there already is an other "active" card, we need to "deactivate" (
    # change colors to normal)
    parent = self.GetParent()
    if parent.active_card is not None and parent.active_card != self.card:
      active_card = parent.getCard(parent.active_card)
      active_card.clicked = False
      active_card.setColors()
      active_card.Refresh()
    # set a color for clicked card ("active")
    self.SetBackgroundColour("green")
    self.Refresh()
    parent.active_card = self.card
    
    frame = self.GetTopLevelParent()
    frame.right_window.setCard(self.card)
    frame.right_window.current_card_text.SetFocus()
  
  
  def onEnteringPanel(self, event):
    # print("entered panel " + self.GetName())
    if not self.clicked:
      self.SetBackgroundColour("red")
      self.Refresh()
      self.entered_panel = True
  
  
  def onLeavingPanel(self, event):
    # print("left panel " + self.GetName())
    if not self.clicked:
      if not self.entered_subpanel:
        self.setColors()
      self.Refresh()
      self.entered_subpanel = False  # fixing bug sometimes hover stays,
      # when mouse moved fast
      self.entered_panel = False
  
  
  def onEnteringSubPanel(self, event):
    # print("entered subpanel " + self.GetName())
    if not self.clicked:
      self.SetBackgroundColour("red")
      self.Refresh()
      self.entered_subpanel = True
  
  
  def onLeavingSubPanel(self, event):
    # print("left subpanel " + self.GetName())
    if not self.clicked:
      if not self.entered_text and not self.entered_panel:
        self.setColors()
      self.Refresh()
      self.entered_text = False
      self.entered_panel = False
      self.entered_subpanel = False
  
  
  def onEnteringText(self, event):
    # print("entered text " + self.GetName())
    if not self.clicked:
      self.SetBackgroundColour("red")
      self.Refresh()
      self.entered_text = True
  
  
  def onLeavingText(self, event):
    # print("left text " + self.GetName())
    if not self.clicked:
      if not self.entered_subpanel:
        self.setColors()
      self.Refresh()
      self.entered_subpanel = False
      self.entered_text = False
  
  
  def onKeyPress(self, e):
    
    key_code = e.GetKeyCode()
    
    frame = self.GetTopLevelParent()
    
    if key_code == wx.WXK_RETURN:
      frame.right_window.setCard(self.card)
    
    e.Skip()
  
  
  def setColors(self):
    if self.card.type is CARD_BLACK:
      self.SetBackgroundColour("black")
      self.subpanel.SetBackgroundColour("black")
      self.text.SetBackgroundColour("black")
      self.text.SetForegroundColour("white")
    else:
      self.SetBackgroundColour("white")
      self.subpanel.SetBackgroundColour("white")
      self.text.SetBackgroundColour("white")
      self.text.SetForegroundColour("black")



class CardText(wx.StaticText):
  def __init__(self, parent, text):
    wx.StaticText.__init__(self, parent=parent, label=text)
    # self.SetBackgroundColour("grey") #(debug)
    
    # fix flickering
    self.Bind(wx.EVT_ERASE_BACKGROUND, onEraseBackGround)



def onEraseBackGround(e):
  # do nothing
  # for flicker-fix
  None
