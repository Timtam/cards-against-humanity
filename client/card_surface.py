import pygame
from scrolled_text_panel import ScrolledTextPanel

from shared.card import CARD_WHITE, CARD_BLACK

BORDER = 5
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
BORDER_COLOR_HOVER = (255, 0, 0)
BORDER_COLOR_CHOSEN = (0, 255, 0)

TEXT_PADDING = 10



class CardSurface(pygame.Surface):
  def __init__(self, display, x, y, width, height, card_type=CARD_WHITE):
    pygame.Surface.__init__(self, (width, height))
    
    self.callback = None
    self.display = display
    self.enabled = True
    self.label = ""
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.card_type = card_type
    self.card = None
    self.chosen = False
    
    self.border = pygame.Rect(0, 0, self.width, self.height)
    if self.card_type is CARD_WHITE:
      self.color = COLOR_WHITE
    elif self.card_type is CARD_BLACK:
      self.color = COLOR_BLACK
    self.border_color = COLOR_BLACK
    
    if self.card_type is CARD_WHITE:
      self.text_color = COLOR_BLACK
    elif self.card_type is CARD_BLACK:
      self.text_color = COLOR_WHITE
    self.card_text = ScrolledTextPanel(self.display, self.x + TEXT_PADDING, self.y + TEXT_PADDING, self.width - 2 * TEXT_PADDING, self.height - 2 * TEXT_PADDING, self.color)
  
  
  def addText(self, text, color=(0, 0, 0)):
    self.card_text.addText(text, color)
  
  
  def clearText(self):
    self.card_text.clearText()
  
  
  def setLabel(self, label):
    self.label = label
  
  
  def getLabel(self):
    label = ""
    if len(self.label)>0:
      label += self.label + " "

    if self.chosen:
      label += "(selected)"

    label += ": " + self.card_text.getLabel()

    return label

  
  def setFocus(self, value):
    self.card_text.setFocus(value)
  
  
  def setSpeakLines(self, value):
    self.card_text.setSpeakLines(value)
  
  
  def getCardText(self):
    return self.card_text
  
  
  def setCard(self, card):
    
    self.clearText()
    self.card = card
    if self.card is not None:
      if card.type is CARD_BLACK:
        self.card_text.addText(card.getCardText(), COLOR_WHITE)
      else:
        self.card_text.addText(card.getCardText())
  
  
  def getCard(self):
    return self.card
  
  
  def handleEvent(self, event):
    # hover over card
    if event.type == pygame.MOUSEMOTION and not self.chosen:
      if self.get_rect().collidepoint(event.pos[0] - self.x, event.pos[1] - self.y):
        self.border_color = BORDER_COLOR_HOVER
      else:
        self.border_color = COLOR_BLACK
      
    # click on card / chose
    if self.getEnable() and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self.get_rect().collidepoint(event.pos[0] - self.x, event.pos[1] - self.y):
        if self.callback:
          self.callback()
        else:
          self.toggleChosen()
        if not self.chosen:
          self.border_color = BORDER_COLOR_HOVER

      
    self.card_text.handleEvent(event)
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.fill(self.color)
    self.card_text.render()
    self.blit(self.card_text, (TEXT_PADDING, TEXT_PADDING))
    pygame.draw.rect(self, self.border_color, self.border, BORDER)

  # a bit dirty here
  # getCallback() doesn't return the value of setCallback(),
  # but self.toggleChosen() instead, which then calls the actual callback
  def setCallback(self, cb):
    self.callback = cb

  def getCallback(self):
    return self.callback


  def setEnable(self, value):
    self.enabled = value


  def getEnable(self):
    return self.card is not None and self.enabled

  def toggleChosen(self):
    if not self.getEnable():
      return

    if self.chosen:
      self.border_color = COLOR_BLACK
    else:
      self.border_color = BORDER_COLOR_CHOSEN

    self.chosen = not self.chosen
