import os.path
from itertools import chain

import pygame

from shared.path import getScriptDirectory



class ScrolledTextPanel:
  def __init__(self, display, text, x, y, width, height):
    self.display = display
    self.text = text
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.font = pygame.font.Font(
      os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), 16)
    self.text_surfaces = []
    
    self.text_lines = self.wrap_multi_line(text, self.font, width)
    for line in self.text_lines:
      self.text_surfaces.append(self.font.render(line, 1, (0, 0, 0)))
  
  
  def truncline(self, text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = True
    # old = None
    while l > maxwidth:
      a = a + 1
      n = text.rsplit(None, a)[0]
      if stext == n:
        cut += 1
        stext = n[:-cut]
      else:
        stext = n
      l = font.size(stext)[0]
      real = len(stext)
      done = False
    return real, done, stext
  
  
  def wrapline(self, text, font, maxwidth):
    done = False
    wrapped = []
    
    while not done:
      nl, done, stext = self.truncline(text, font, maxwidth)
      wrapped.append(stext.strip())
      text = text[nl:]
    return wrapped
  
  
  def wrap_multi_line(self, text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(
      *(self.wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)
  
  
  def handleEvent(self, event):
    pass
  
  
  def update(self):
    pass
  
  
  def render(self):
    pos_y = self.y
    for text_line in self.text_surfaces:
      self.display.screen.blit(text_line, (self.x, pos_y))
      pos_y += text_line.get_height()
