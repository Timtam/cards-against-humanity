from shared.card import CARD_PLACEHOLDER_LENGTH

import pygame
import pygame.locals as pl

from twisted.logger import Logger

class View(object):
  log = Logger()
  def __init__(self, display):
    self.display = display
    self.first_call = False
    self.tab_order = []
    self.tab_position = 0
    
    if self.display.accessibility:
      from .speech import Speaker
      self.speaker = Speaker()
  
  
  def update(self):
    if not self.first_call:
      self.firstUpdate()
      self.first_call = True
  
  
  def render(self):
    pass
  
  
  def handleEvent(self, event):
    
    if len(self.tab_order) == 0:
      return
    
    if event.type == pygame.KEYDOWN:
      if event.key == pl.K_TAB:
        try:
          self.tab_order[self.tab_position].setFocus(False)
        except AttributeError:
          pass
        # some weird problem here
        # after restoring the focus of the window by tabbing back into
        # it, the mod attribute won't be set correctly
        # that's why we will try to guess it here in a different way
        if pygame.key.get_mods() & pl.KMOD_LSHIFT == pl.KMOD_LSHIFT or \
                                pygame.key.get_mods() & pl.KMOD_RSHIFT == \
                        pl.KMOD_RSHIFT:
          self.tab_position -= 1
          if self.tab_position < 0:
            self.tab_position = len(self.tab_order) - 1
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
      
      elif event.key == pl.K_RETURN:
        
        try:
          if self.tab_order[self.tab_position].getEnable():
            self.tab_order[self.tab_position].getCallback()()
            sound = self.tab_order[self.tab_position].getClickSound()
            sound.stop()
            sound.play()
        except (AttributeError, TypeError):
          pass
  

  def speak(self, text, interrupt=False):
    if not self.display.accessibility:
      return
    self.speaker.output(text.replace('_'*CARD_PLACEHOLDER_LENGTH, "("+self.display.translator.translate("free space")+")"), interrupt)
  
  
  # will only be called once the view receives it's first update
  def firstUpdate(self):
    if len(self.tab_order) == 0:
      return
    
    self.speak(self.tab_order[0].getLabel(), False)
    try:
      self.tab_order[0].setFocus(True)
    except AttributeError:
      pass
