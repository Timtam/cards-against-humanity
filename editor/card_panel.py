from const import *
from shared.card import Card, CARD_BLACK, CARD_WHITE


class CardPanel(wx.Panel):
  def __init__(self, parent, card_id=-1, size=(ELEMENT_SIZE, ELEMENT_SIZE), text="",
               card_type=CARD_WHITE):
    wx.Panel.__init__(self, parent=parent, id=card_id, size=size,
                      name=("card " + `card_id`), style=wx.SIMPLE_BORDER)
    self.card = Card(id=card_id, text=text, type=card_type)
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

    self.box.Add(self.text, 1, wx.ALL | wx.EXPAND, 3)
    self.SetSizer(self.box)


    self.color = self.GetBackgroundColour()

    self.Bind(wx.EVT_LEFT_UP, self.onClick)
    self.text.Bind(wx.EVT_LEFT_UP, self.onClick)
    self.Bind(wx.EVT_ENTER_WINDOW, self.onEntering)
    #self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaving)
    self.text.Bind(wx.EVT_ENTER_WINDOW, self.onEntering)
    self.text.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaving)

  def onClick(self, event):
    print("clicked on " + self.GetName())

  def onEntering(self, event):
    print("entered " + self.GetName())
    self.SetBackgroundColour("red")
    self.Refresh()

  def onLeaving(self, event):
    print("leaved " + self.GetName())
    self.SetBackgroundColour(self.color)
    self.Refresh()


class CardText(wx.StaticText):
  def __init__(self, parent, text):
    wx.StaticText.__init__(self, parent=parent, label=text)
    # self.SetBackgroundColour("grey") #(debug)

