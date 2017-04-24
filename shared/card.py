from .exceptions import CardValidityError

import string

CARD_WHITE=0
CARD_BLACK=1

class Card(object):
  def __init__(self, id=-1, text='', type=CARD_WHITE):
    self.id=id
    self.text=text
    self.type=type

  def isValid(self):
    # implementing some safety
    # if the card is white, no wildcards are allowed
    # if the card is black, wildcards are allowed, but
    # they may only be integers and need to start with 0
    # and need to be continuous
    format_iterator = string.Formatter().parse(self.text)
    placeholders = [f[2] for f in format_iterator]
    if self.type==CARD_WHITE and len(placeholders)>0:
      raise CardValidityError({'id':self.id, 'text': 'White cards may not have any placeholders ( {...} ).'})
    elif self.type==CARD_BLACK:
      for i in range(len(placeholders)):
        try:
          if i != int(placeholders[i]):
            raise CardValidityError({'id': self.id, 'text': 'Black card's placeholders must follow a continuous scheme, starting from zero ( {0}, {1}, {2} ... )'})
        except ValueError:
          # occurs always if the placeholder isn't an integer, which may not happen
          raise CardValidityError({'id': self.id, 'text': 'Black cards may only contain placeholders which consist of integer enumerations ( {0}, {1}, {2}, ... )'})
    return True
