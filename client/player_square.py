import pygame

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_WHITE = (255, 255, 255)



class PlayerSquare(pygame.Surface):
  def __init__(self, display, x, y, width, height, id):
    pygame.Surface.__init__(self, (width, height))
    
    self.display = display
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.id = id
    self.color = COLOR_WHITE
    self.czar = False
    self.chosen = False
    self.unchosen = False
    self.show_name = False
    self.text_surface = self.display.getFont().render(self.getName(), 1, COLOR_BLACK)
    self.text_background = pygame.Surface((self.text_surface.get_width() + 8, self.text_surface.get_height() + 6))
    self.text_bckgrnd_border = self.text_background.get_rect()
    self.text_x = self.x + self.width/2 - self.text_surface.get_width()/2
    self.border = pygame.Rect(0, 0, self.width, self.height)
    self.border_color = COLOR_BLACK
  
  
  def getName(self):
    return self.display.factory.findUsername(self.id)
  
  
  def showName(self):
    self.text_background.fill((255, 255, 255))
    pygame.draw.rect(self.text_background, COLOR_BLACK, self.text_bckgrnd_border, 1)
    self.display.screen.blit(self.text_background, (self.text_x - 4, self.y + self.width + 10 - 3))
    self.display.screen.blit(self.text_surface, (self.text_x, self.y + self.width + 10))
  
  
  def setCzar(self):
    self.czar = True
    self.unchosen = False
    self.chosen = False
  
  
  def setChosen(self):
    self.chosen = True
    self.unchosen = False
    self.czar = False
  
  
  def setUnchosen(self):
    self.unchosen = True
    self.chosen = False
    self.czar = False
  
  
  def handleEvent(self, event):
    if event.type == pygame.MOUSEMOTION:
      if self.get_rect().collidepoint(event.pos[0] - self.x,
                                      event.pos[1] - self.y):
        self.show_name = True
      else:
        self.show_name = False
  
  
  def update(self):
    if self.czar:
      self.color = COLOR_BLACK
    elif self.unchosen:
      self.color = COLOR_RED
    elif self.chosen:
      self.color = COLOR_GREEN
    else:
      self.color = COLOR_WHITE
  
  
  def render(self):
    self.fill(self.color)
    pygame.draw.rect(self, COLOR_BLACK, self.border, 5)
    if self.show_name:
      self.showName()