import pygame

BUTTON_PADDING = 5
BUTTON_COLOR = (128, 128, 128)
BUTTON_COLOR_HOVER = (100, 100, 100)



class Button:
  def __init__(self, screen, text, font, tcolor, x, y, width=-1, height=-1):
    # init values
    self.screen = screen
    self.text = font.render(text, 1, tcolor)
    self.x = x
    self.y = y
    self.width = self.w = width
    self.height = self.h = height
    self.x_end = self.x + self.w
    self.y_end = self.y + self.h
    self.text_x = x + BUTTON_PADDING
    self.text_y = y + BUTTON_PADDING
    self.button_rect = (self.x, self.y, self.w, self.h)
    self.color = BUTTON_COLOR
    
    # calc positions and width + height
    self.setPosition(x, y)
  
  
  def getWidth(self):
    return self.w
  
  
  def getHeight(self):
    return self.h
  
  
  def setPosition(self, x, y):
    self.x = x
    self.y = y
    
    # if width or height == -1 -> width and height depend on text size
    if self.width == -1:
      self.w = self.text.get_width() + 2 * BUTTON_PADDING
      self.text_x = x + BUTTON_PADDING
    else:
      self.w = self.width
      self.text_x = x + self.width / 2 - self.text.get_width() / 2
    
    if self.height == -1:
      self.h = self.text.get_height() + 2 * BUTTON_PADDING
      self.text_y = y + BUTTON_PADDING
    else:
      self.h = self.height
      self.text_y = y + self.height / 2 - self.text.get_height() / 2
    
    self.x_end = self.x + self.w
    self.y_end = self.y + self.h
    
    self.button_rect = (self.x, self.y, self.w, self.h)
  
  
  def handleEvent(self, event):
    # hover over button
    if event.type == pygame.MOUSEMOTION:
      mouse = pygame.mouse.get_pos()
      if self.x < mouse[0] < self.x_end and self.y < mouse[1] < self.y_end:
        self.color = BUTTON_COLOR_HOVER
      else:
        self.color = BUTTON_COLOR
  
  
  def render(self):
    pygame.draw.rect(self.screen, self.color, self.button_rect, 0)
    self.screen.blit(self.text, (self.text_x, self.text_y))
