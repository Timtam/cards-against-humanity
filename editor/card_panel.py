from const import *
from shared.card import Card, CARD_BLACK, CARD_WHITE


class CardPanel(wx.Panel):
  def __init__(self, parent, ID=-1, size=(ELEMENT_SIZE, ELEMENT_SIZE), text="",
               card_type=CARD_WHITE):
    wx.Panel.__init__(self, parent=parent, id=ID, size=size,
                      name=("card " + `ID`), style=wx.SIMPLE_BORDER)
    self.card = Card(id=ID, text=text, type=card_type)
    self.box = wx.BoxSizer(wx.VERTICAL)
    self.text = CardText(parent=self, text=text)

    if card_type is CARD_BLACK:
      self.SetBackgroundColour("black")
      self.text.SetBackgroundColour("black")
      self.text.SetForegroundColour("white")
    else:
      self.SetBackgroundColour("white")
      self.text.SetBackgroundColour("white")
      self.text.SetForegroundColour("black")

    self.box.Add(self.text, 1, wx.ALL | wx.EXPAND, 10)
    self.SetSizer(self.box)

    self.Bind(wx.EVT_LEFT_UP, self.onClick)

  def onClick(self, event):
    print(self.GetName())


class CardText(wx.StaticText):
  def __init__(self, parent, text):
    wx.StaticText.__init__(self, parent=parent, label=text)
    # self.SetBackgroundColour("grey") #(debug)
    self.Bind(wx.EVT_LEFT_UP, self.onClick)

  def onClick(self, event):
    self.Parent.onClick(wx.EVT_LEFT_UP)
