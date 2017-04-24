import string

CARD_WHITE=0
CARD_BLACK=1

class Card(object):
  def __init__(self, id=-1, text='', type=CARD_WHITE):
    self.id=id
    self.text=text
    self.type=type

  # TODO: no return values, but use exceptions with helpful texts instead
  def isValid(self):
    # implementing some safety
    # if the card is white, no wildcards are allowed
    # if the card is black, wildcards are allowed, but
    # they may only be integers and need to start with 0
    # and need to be continuous
    format_iterator = string.Formatter().parse(self.text)
    placeholders = [f[2] for f in format_iterator]
    if self.type==CARD_WHITE and len(placeholders)>0:
      return False
    elif self.type==CARD_BLACK:
      for i in range(len(placeholders)):
        try:
          if i != int(placeholders[i]):
            return False
        except ValueError:
          # occurs always if the placeholder isn't an integer, which may not happen
          return False
    return True
