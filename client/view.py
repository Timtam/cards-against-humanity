import accessible_output2.outputs.auto as speech
import pygame
import pygame.locals as pl



class View(object):
  def __init__(self, display):
    self.display = display
    self.first_call = False
    self.speaker = speech.Auto()
    self.tab_order = []
    self.tab_position = 0
  
  
  def update(self):
    if not self.first_call:
      self.first_update()
      self.first_call = True
  
  
  def render(self):
    pass
  
  
  def handleEvent(self, event):

    if not self.display.accessibility:
      return

    if len(self.tab_order) == 0:
      return

    if event.type == pygame.KEYDOWN:
      if event.key == pl.K_TAB:
        try:
          self.tab_order[self.tab_position].setFocus(False)
        except AttributeError:
          pass
        if event.mod in [pl.KMOD_LSHIFT, pl.KMOD_RSHIFT]:
          self.tab_position -= 1
          if self.tab_position < 0:
            self.tab_position = len(self.tab_order)-1
        else:
          self.tab_position += 1
          if self.tab_position >= len(self.tab_order):
            self.tab_position = 0

        self.speak(self.tab_order[self.tab_position].getLabel(), True)

        try:
          self.tab_order[self.tab_position].setFocus(True)
        except AttributeError:
          pass
  
      elif event.key == pl.K_LCTRL or pygame.key == pl.K_RCTRL:
        self.speak(self.tab_order[self.tab_position].getLabel(), True)
  
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

  def speak(self, text, interrupt=False):
    self.speaker.speak(text, interrupt)

  # will only be called once the view receives it's first update
  def first_update(self):
    if not self.display.accessibility:
      return

    if len(self.tab_order) == 0:
      return

    self.speak(self.tab_order[0].getLabel(), False)
    try:
      self.tab_order[0].setFocus(True)
    except AttributeError:
      pass
