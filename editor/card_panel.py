from const import *
from shared.card import CARD_BLACK, CARD_WHITE, Card



class CardPanel(wx.Panel):
  def __init__(self, parent, card_id=-1, size=(ELEMENT_SIZE, ELEMENT_SIZE),
               text="",
               card_type=CARD_WHITE):
    wx.Panel.__init__(self, parent=parent, id=card_id, size=size,
                      name=("card " + `card_id`), style=wx.SIMPLE_BORDER)
    self.card = Card(id=card_id, text=text, type=card_type)
    self.box = wx.BoxSizer(wx.VERTICAL)
    self.text = CardText(parent=self, text=self.card.getCardText())
    
    self.setColors()
    
    self.box.Add(self.text, 1, wx.ALL | wx.EXPAND, 3)
    self.SetSizer(self.box)
    
    self.Bind(wx.EVT_LEFT_UP, self.onClick)
    self.text.Bind(wx.EVT_LEFT_UP, self.onClick)
    # self.Bind(wx.EVT_ENTER_WINDOW, self.onEntering)
    # self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaving)
    self.text.Bind(wx.EVT_ENTER_WINDOW, self.onEntering)
    self.text.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaving)
    
    self.Bind(wx.EVT_KEY_UP, self.onKeyPress)
  
  
  def onClick(self, event):
    frame = self.GetTopLevelParent()
    frame.right_window.setCard(self.card)
    frame.right_window.current_card_text.SetFocus()
  
  
  def onEntering(self, event):
    # print("entered " + self.GetName())
    self.SetBackgroundColour("red")
    self.Refresh()
  
  
  def onLeaving(self, event):
    # print("leaved " + self.GetName())
    self.setColors()
    self.Refresh()
  
  
  def onKeyPress(self, e):
    
    key_code = e.GetKeyCode()
    
    frame = self.GetTopLevelParent()
    
    if key_code == wx.WXK_RETURN:
      frame.right_window.setCard(self.card)
    
    e.Skip()
  
  
  def setColors(self):
    if self.card.type is CARD_BLACK:
      self.SetBackgroundColour("black")
      self.text.SetBackgroundColour("black")
      self.text.SetForegroundColour("white")
    else:
      self.SetBackgroundColour("white")
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
