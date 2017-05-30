import pygame
from scrolled_text_panel import ScrolledTextPanel

CARD_WHITE = 0
CARD_BLACK = 1

BORDER = 5
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
BORDER_COLOR_HOVER = (255, 0, 0)
BORDER_COLOR_CHOSEN = (0, 255, 0)

TEXT_PADDING = 10



class CardSurface(pygame.Surface):
  def __init__(self, display, x, y, width, height, card_type=CARD_WHITE):
    pygame.Surface.__init__(self, (width, height))
    
    self.display = display
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.card_type = card_type
    
    self.border = pygame.Rect(self.x, self.y, self.width, self.height)
    if self.card_type is CARD_WHITE:
      self.color = COLOR_WHITE
    elif self.card_type is CARD_BLACK:
      self.color = COLOR_BLACK
    self.border_color = self.color
    
    if self.card_type is CARD_WHITE:
      self.text_color = COLOR_BLACK
    elif self.card_type is CARD_BLACK:
      self.text_color = COLOR_WHITE
    self.card_text = ScrolledTextPanel(self.display, self.x + TEXT_PADDING, self.y + TEXT_PADDING, self.width - 2 * TEXT_PADDING, self.height - 2 * TEXT_PADDING, self.color)
  
  
  def addText(self, text, color=(0, 0, 0)):
    self.card_text.addText(text, color)
  
  
  def handleEvent(self, event):
    # hover over button and click events
    if event.type == pygame.MOUSEMOTION and self.get_rect().collidepoint(
            event.pos):
      self.border_color = BORDER_COLOR_HOVER
      
    else:
      self.border_color = self.color
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.fill(self.color)
    pygame.draw.rect(self, self.border_color, self.border, BORDER)
    self.card_text.render()
    self.blit(self.card_text, (TEXT_PADDING, TEXT_PADDING))