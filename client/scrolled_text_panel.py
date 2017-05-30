import os.path
from itertools import chain

import pygame
import pygame.locals as pl

from shared.path import getScriptDirectory

SCROLLBAR_THICKNESS = 20


class ScrolledTextPanel:
  def __init__(self, screen, display, x, y, width, height, text_color=(0, 0, 0), maxheight=480):
    self.focus = False
    self.label = ''
    self.display = display
    self.screen = screen
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.text_color = text_color
    self.maxheight = maxheight
    self.font = display.getFont(16)
    self.text_surfaces = []
    self.text_lines = []
    # for now only used to memorize the text the visually impaired user
    # is currently looking at
    self.line_cursor = 0
    self.speak_lines = True
    self.getHeight()
    if self.height > self.maxheight:
      surface_height = self.maxheight
    else:
      surface_height = self.height
    self.surface = pygame.Surface((self.width, surface_height))
    self.text_surface = pygame.Surface((self.width - SCROLLBAR_THICKNESS, surface_height))
    self.surface_rect = self.surface.get_rect()
    self.ratio = 1.0
    self.track = pygame.Rect(self.surface_rect.right - SCROLLBAR_THICKNESS, self.surface_rect.top,
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
  
  
  @classmethod
  def wrapline(cls, text, font, maxwidth):
    done = False
    wrapped = []
    
    while not done:
      nl, done, stext = cls.truncline(text, font, maxwidth)
      wrapped.append(stext.strip())
      text = text[nl:]
    return wrapped
  
  
  @classmethod
  def wrap_multi_line(cls, text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(
      *(cls.wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)
  
  
  def addText(self, text):
    length = len(self.text_lines)
    self.text_lines += self.wrap_multi_line(text, self.font, self.width - SCROLLBAR_THICKNESS)
    for i in range(length, len(self.text_lines)):
      self.text_surfaces.append(self.font.render(self.text_lines[i], 1, self.text_color))
    self.line_cursor = len(self.text_lines)-1

    self.getHeight()
    if self.height > self.maxheight:
      surface_height = self.maxheight
    else:
      surface_height = self.height
    self.surface = pygame.Surface((self.width, surface_height))
    self.text_surface = pygame.Surface((self.width - SCROLLBAR_THICKNESS, self.height))
    self.surface_rect = self.surface.get_rect()
    self.ratio = (1.0 * self.surface_rect.height) / self.text_surface.get_height()
    self.track = pygame.Rect(self.surface_rect.right - SCROLLBAR_THICKNESS
       , self.surface_rect.top,
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
    
  
  def handleEvent(self, event):
    if self.display.accessibility and self.focus:
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
          self.display.view.speak(self.text_lines[self.line_cursor], True)

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
    if self.text_color == (0, 0, 0):
      self.surface.fill((255, 255, 255))
      self.text_surface.fill((255, 255, 255))
    elif self.text_color == (255, 255, 255):
      self.surface.fill((0, 0, 0))
      self.text_surface.fill((0, 0, 0))
    pos_y = 0
    for text_line in self.text_surfaces:
      self.text_surface.blit(text_line, (0, pos_y))
      pos_y += text_line.get_height()
    self.surface.blit(self.text_surface, (0, (self.knob.top / self.ratio) * -1))
    if self.text_color == (0, 0, 0):
      pygame.draw.rect(self.surface, (192, 192, 192), self.track, 0)
      pygame.draw.rect(self.surface, (0, 0, 0), self.knob.inflate(-2, -2), 3)
    elif self.text_color == (255, 255, 255):
      pygame.draw.rect(self.surface, (64, 64, 64), self.track, 0)
      pygame.draw.rect(self.surface, (255, 255, 255), self.knob.inflate(-2, -2), 3)
    self.screen.blit(self.surface, (self.x, self.y))


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
