import pygame

BORDER = 3
COLOR_BLACK = (0, 0, 0)



class GameEntry(pygame.Surface):
  def __init__(self, display, width, height):
    pygame.Surface.__init__(self, (width, height))
    
    self.display = display
    self.width = width
    self.height = height
    
    self.border = pygame.Rect(0, 0, self.width, self.height)
    self.border_color = COLOR_BLACK
    
    self.text = self.display.getFont().render("This is a looooooooooooooooooooooooooooooooooooooooooooooooooooooong dummy entry", 1, (0, 0, 0))
    
    
  def handleEvent(self, event):
    pass
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.fill((255, 255, 255))
    pygame.draw.rect(self, self.border_color, self.border, BORDER)
    self.blit(self.text, (10, 10))