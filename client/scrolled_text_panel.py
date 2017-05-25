import os.path
from itertools import chain

import pygame
import pygame.locals as pl

from shared.path import getScriptDirectory

SCROLLBAR_THICKNESS = 20


class ScrolledTextPanel:
  def __init__(self, screen, x, y, width, height):
    self.focus = False
    self.label = ''
    self.screen = screen
    self.x = x
    self.y = y
    self.width = width - SCROLLBAR_THICKNESS
    self.height = height
    self.font = pygame.font.Font(
      os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), 16)
    self.text_surfaces = []
    self.text_lines = []
    # for now only used to memorize the text the visually impaired user
    # is currently looking at
    self.line_cursor = 0
    self.speak_lines = True
    self.getHeight()
    self.surface = pygame.Surface((self.width, self.height))
    self.surface_rect = self.surface.get_rect()
    self.ratio = 1.0
    self.track = pygame.Rect(self.surface_rect.right - SCROLLBAR_THICKNESS + self.x, self.surface_rect.top + self.y,
                        SCROLLBAR_THICKNESS, self.surface_rect.height)
    self.knob = pygame.Rect(self.track)
    self.knob.height = self.track.height * self.ratio
    self.scrolling = False
    
  
  @staticmethod
  def truncline(text, font, maxwidth):
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
  
  
  def addText(self, text):
    length = len(self.text_lines)
    self.text_lines += self.wrap_multi_line(text, self.font, self.width)
    for i in range(length, len(self.text_lines)):
      self.text_surfaces.append(self.font.render(self.text_lines[i], 1, (0, 0, 0)))
    self.line_cursor = len(self.text_lines)-1

    self.getHeight()
    self.surface = pygame.Surface((self.width, self.height))
    self.surface_rect = self.surface.get_rect()
    self.ratio = (1.0 * self.surface_rect.height) / self.surface.get_height()
    self.track = pygame.Rect(self.surface_rect.right - SCROLLBAR_THICKNESS + self.x, self.surface_rect.top + self.y,
                        SCROLLBAR_THICKNESS, self.surface_rect.height)
    self.knob = pygame.Rect(self.track)
    self.knob.height = self.track.height * self.ratio
    self.scrolling = False


  def clearText(self):
    self.text_surfaces = []
    self.text_lines = []
    self.line_cursor = 0


  def getText(self):
    return '\n'.join(self.text_lines)


  def getHeight(self):
    self.height = 0
    for text_line in self.text_surfaces:
      self.height += text_line.get_height()
      
    return self.height
  
  
  def setNewScreen(self, surface):
    self.screen = surface
    
  
  # a bit different from usual
  # this class doesn't know the display yet, so we'll have to tell
  def handleEvent(self, event, display):
    if display.accessibility and self.focus:
      if event.type == pygame.KEYDOWN:
        speech = True
        if event.key == pl.K_UP:
          self.line_cursor = max(0, self.line_cursor-1)
        elif event.key == pl.K_DOWN:
          self.line_cursor = min(len(self.text_lines)-1, self.line_cursor+1)
        elif event.key == pl.K_HOME:
          self.line_cursor = 0
        elif event.key == pl.K_END:
          self.line_cursor = len(self.text_lines)-1
        else:
          speech = False
        if speech:
          display.view.speak(self.text_lines[self.line_cursor], True)

    if event.type == pygame.MOUSEMOTION and self.scrolling:
  
      if event.rel[1] != 0:
        move = max(event.rel[1], self.track.top - self.knob.top)
        move = min(move, self.track.bottom - self.knob.bottom)
    
        if move != 0:
          self.knob.move_ip(0, move)

    elif event.type == pygame.MOUSEBUTTONDOWN and self.knob.collidepoint(event.pos):
      self.scrolling = True

    elif event.type == pygame.MOUSEBUTTONUP:
      self.scrolling = False
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.surface.fill((255, 255, 255))
    pos_y = 0
    for text_line in self.text_surfaces:
      self.surface.blit(text_line, (0, pos_y))
      pos_y += text_line.get_height()
    #self.screen.blit(self.surface, (self.x, self.y))
    self.screen.blit(self.surface, (self.x, (self.knob.top / self.ratio - self.y) * -1 + self.y))
    pygame.draw.rect(self.screen, (192, 192, 192), self.track, 0)
    pygame.draw.rect(self.screen, (0, 0, 0), self.knob.inflate(-2, -6), 3)


  def setFocus(self, value):
    self.focus = value


  def getFocus(self):
    return self.focus


  def setLabel(self, label):
    self.label = label


  def setSpeakLines(self, value):
    self.speak_lines = value


  def getLabel(self):
    label = self.label+" text: "
    if len(self.text_lines):
      label += self.text_lines[self.line_cursor]
      if self.speak_lines:
        label += ' (line %d of %d'%(self.line_cursor+1, len(self.text_lines))
    else:
      label += "empty"
    return label
