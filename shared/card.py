from .exceptions import CardValidityError
from editor.const import *

import re
import string
import wx

CARD_WHITE=0
CARD_BLACK=1

CARD_PLACEHOLDER_LENGTH=3

class Card(object):
  def __init__(self, id=-1, text='', type=CARD_WHITE):
    self.id=id
    self.__text=text
    self.type=type

  def isValid(self, text=None):
    # implementing some safety
    # if the card is white, no wildcards are allowed
    # if the card is black, wildcards are allowed
    # there must even be at least one present
    
    # if text is None, use the current internal text
    if text is None:
      text = self.getInternalText()

    format_iterator = string.Formatter().parse(text)
    placeholders = [p[2] for p in format_iterator if p[2] is not None]
    if self.type==CARD_WHITE and len(placeholders)>0:
      raise CardValidityError({'id':self.id, 'text': 'White cards may not have any placeholders ( {...} ).'})
    elif self.type==CARD_BLACK and len(placeholders)==0:
      raise CardValidityError({'id': self.id, 'text': 'Black cards must contain at least one placeholder'})      
    return True

  # sets the internal text (usually just needed internally)
  def setInternalText(self, text):
    # will run through the isValid check
    if self.isValid(text):
      self.__text = text

  def getInternalText(self):
    return self.__text

  # retrieves the properly formatted card text
  def getCardText(self):
    return re.sub("{}", "_"*CARD_PLACEHOLDER_LENGTH, self.getInternalText())

  # parses the text and will set it internally too
  def setCardText(self, text):
    format_iterator = string.Formatter().parse(text)
    placeholders = [p[2] for p in format_iterator if p[2] is not None]
    # we don't accept already well formatted placeholders inside the actual card text
    if len(placeholders)>0:
       raise CardValidityError({'id':self.id, 'text': 'invalid text found inside the card text: {%s}'%(placeholders[0])})
    internal_text = re.sub(" __+ ", " {} ",text)
    self.setInternalText(internal_text)


class CardPanel(wx.Panel):
  def __init__(self, parent, ID=-1, size=(ELEMENT_SIZE, ELEMENT_SIZE), text="", card_type=CARD_WHITE):
    wx.Panel.__init__(self, parent=parent, id=ID, size=size, name=("card "+`ID`), style=wx.SIMPLE_BORDER)
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

class CardText(wx.StaticText):
  def __init__(self, parent, text):
    wx.StaticText.__init__(self, parent=parent, label=text)
    #self.SetBackgroundColour("grey") #(debug)
