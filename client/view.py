import pygame
import pygame.locals as pl



class View(object):
  def __init__(self, display):
    self.display = display
    self.tab_order = []
    self.tab_position = 0
  
  
  def update(self):
    pass
  
  
  def render(self):
    pass
  
  
  def handleEvent(self, event):

    if len(self.tab_order) == 0:
      return

    if event.type == pygame.KEYUP:
      if event.key == pl.K_TAB:
        if event.mod in [pl.KMOD_LSHIFT, pl.KMOD_RSHIFT]:
          self.tab_position -= 1
          if self.tab_position < 0:
            self.tab_position = len(self.tab_order)-1
        else:
          self.tab_position += 1
          if self.tab_position >= len(self.tab_order):
            self.tab_position = 0

        # TODO: speaking the currently selected item
  
  
  def loadImage(self, filename, colorkey=None):
    
    image = pygame.image.load(filename)
    
    if image.get_alpha() is None:
      image = image.convert()
    else:
      image = image.convert_alpha()
    
    if colorkey is not None:
      
      if colorkey == -1:
        colorkey = image.get_at((0, 0))
    
    image.set_colorkey(colorkey, pygame.RLEACCEL)
    
    return image
