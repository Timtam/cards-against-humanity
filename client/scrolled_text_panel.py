import pygame
from itertools import chain
import pygame.locals as pl

BUTTON_SCROLL_WHEEL_UP = 4
BUTTON_SCROLL_WHEEL_DOWN = 5

SCROLLBAR_THICKNESS = 20
#TEXT_SCROLLBAR_SPACE = 10
SCROLL_SPEED = 20


class ScrolledTextPanel(pygame.Surface):
  def __init__(self, display, x, y, width, height, background_color=(255, 255, 255)):
    pygame.Surface.__init__(self,(width, height))

    self.focus = False
    self.label = ''

    self.display = display
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.font = self.display.getFont()
    self.background_color = background_color
    self.text_lines = []
    self.text_surfaces = []
    self.text_width = self.width
    self.text_height = self.height
    self.text_width = self.getTextWidth()
    self.text_height = self.getTextHeight()
    self.text_surface = pygame.Surface((self.text_width, self.text_height))

    self.line_cursor = 0
    self.speak_lines = True

    self.rect = self.get_rect()
    self.ratio = 1.0
    self.track = pygame.Rect(self.rect.right - SCROLLBAR_THICKNESS, self.rect.top, SCROLLBAR_THICKNESS, self.rect.height)
    self.knob = pygame.Rect(self.track)
    self.knob.height = self.track.height * self.ratio
    self.scrolling = False
    self.mouse_in_me = False
    

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


  def getTextWidth(self):
    text_width = self.width - SCROLLBAR_THICKNESS
    return text_width
    
    
  # def getTextHeight(self):
  #
  #   text_height = 0
  #   for text_line_surface in self.text_surfaces:
  #     text_height += text_line_surface.get_height()
  #   return text_height


  def getTextHeight(self):
    font_height = self.font.get_height()
    return len(self.text_lines) * font_height


  def getHeight(self):
    height = 0
    for text_line in self.text_surfaces:
      height += text_line.get_height()
  
    return height
  
    
  def buildScrollbar(self):
    self.rect = self.get_rect()
    if self.rect.height < self.text_surface.get_height():
      self.ratio = (1.0 * self.rect.height) / self.text_surface.get_height()
    self.track = pygame.Rect(self.rect.right - SCROLLBAR_THICKNESS,
                             self.rect.top, SCROLLBAR_THICKNESS,
                             self.rect.height)
    self.knob = pygame.Rect(self.track)
    self.knob.height = self.track.height * self.ratio


  def addText(self, text, color=(0, 0, 0)):
    self.text_width = self.getTextWidth()
    
    length = len(self.text_lines)
    self.text_lines += self.wrap_multi_line(text, self.font, self.text_width)
    for i in range(length, len(self.text_lines)):
      self.text_surfaces.append(self.font.render(self.text_lines[i], 1, color))
    self.line_cursor = len(self.text_lines) - 1
    
    self.text_width = self.getTextWidth()
    self.text_height = self.getTextHeight()
    self.height = self.getHeight()
    self.text_surface = pygame.Surface((self.text_width, self.text_height))

    self.buildScrollbar()


  def clearText(self):
    self.text_surfaces = []
    self.text_lines = []
    self.line_cursor = 0
    
    
  def getText(self):
    return '\n'.join(self.text_lines)
    
    
  def setFocus(self, value):
    self.focus = value


  def getFocus(self):
    return self.focus


  def setLabel(self, label):
    self.label = label


  def setSpeakLines(self, value):
    self.speak_lines = value


  def getLabel(self):
    label = ""
    if len(self.label)>0:
      label += self.label + " text: "
    if len(self.text_lines):
      label += self.text_lines[self.line_cursor]
      if self.speak_lines:
        label += ' (line %d of %d'%(self.line_cursor+1, len(self.text_lines))
    else:
      label += "empty"
    return label

    
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
  
    elif event.type == pygame.MOUSEBUTTONDOWN and self.knob.collidepoint(
         event.pos[0] - self.x, event.pos[1] - self.y):
      self.scrolling = True
  
    elif event.type == pygame.MOUSEBUTTONUP:
      self.scrolling = False
      
    
    if event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos[0] - self.x, event.pos[1] - self.y):
      self.mouse_in_me = True
    elif event.type == pygame.MOUSEMOTION and not self.rect.collidepoint(event.pos[0] - self.x, event.pos[1] - self.y):
      self.mouse_in_me = False
      
    if self.mouse_in_me and event.type == pygame.MOUSEBUTTONDOWN:
      move = 0
      if event.button == BUTTON_SCROLL_WHEEL_UP:
        #print("scrolled up")  # debug
        move = max(-1 * SCROLL_SPEED * self.ratio, self.track.top - self.knob.top)
      elif event.button == BUTTON_SCROLL_WHEEL_DOWN:
        #print("scolled down")  # debug
        move = max(SCROLL_SPEED * self.ratio, self.track.top - self.knob.top)
      move = min(move, self.track.bottom - self.knob.bottom)
      if move != 0:
        self.knob.move_ip(0, move)
    
    
  def update(self):
    pass
    
    
  def render(self):
    self.fill(self.background_color)
    self.text_surface.fill(self.background_color)

    text_pos_y = 0
    for text_line in self.text_surfaces:
      self.text_surface.blit(text_line, (0, text_pos_y))
      text_pos_y += text_line.get_height()
    self.blit(self.text_surface, (0, (self.knob.top / self.ratio) * -1))
    if self.ratio != 1.0:
      pygame.draw.rect(self, (192, 192, 192), self.track, 0)
      pygame.draw.rect(self, (0, 0, 0), self.knob.inflate(-4, -4), 3)