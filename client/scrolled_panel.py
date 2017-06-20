import pygame

SCROLLBAR_THICKNESS = 20
BUTTON_SCROLL_WHEEL_UP = 4
BUTTON_SCROLL_WHEEL_DOWN = 5
SCROLL_SPEED = 20

VSPACE = 20



class ScrolledPanel(pygame.Surface):
  def __init__(self, display, x, y, width, height, vspace=VSPACE, background_color=(255, 255, 255)):
    pygame.Surface.__init__(self, (width, height))

    self.focus = False
    self.label = ''

    self.display = display
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.vspace = vspace
    self.background_color = background_color
    
    self.available_width = self.width - SCROLLBAR_THICKNESS
    self.virtual_height = 0
    self.content_surface = pygame.Surface((self.available_width, self.virtual_height))
    
    self.surfaces = []

    self.rect = self.get_rect()
    self.ratio = 1.0
    self.track = pygame.Rect(self.rect.right - SCROLLBAR_THICKNESS,
                             self.rect.top, SCROLLBAR_THICKNESS,
                             self.rect.height)
    self.knob = pygame.Rect(self.track)
    self.knob.height = self.track.height * self.ratio
    self.scrolling = False
    self.mouse_in_me = False
    
    
  def buildScrollbar(self):
    self.rect = self.get_rect()
    if self.rect.height < self.content_surface.get_height():
      self.ratio = (1.0 * self.rect.height) / self.content_surface.get_height()
    self.track = pygame.Rect(self.rect.right - SCROLLBAR_THICKNESS,
                             self.rect.top, SCROLLBAR_THICKNESS,
                             self.rect.height)
    self.knob = pygame.Rect(self.track)
    self.knob.height = self.track.height * self.ratio
    
    
  def getAvailableWidth(self):
    return self.available_width
  
    
  def getVirtualHeight(self):
    height = 0
    last = len(self.surfaces) - 1
    for i, surface in enumerate(self.surfaces):
      height += surface.get_height()
      if i is not last:
        height += self.vspace
      
    return height
    
    
  def addSurface(self, surface):
    
    self.surfaces.append(surface)
    self.virtual_height = self.getVirtualHeight()
    self.content_surface = pygame.Surface((self.available_width, self.virtual_height))
    
    self.buildScrollbar()
    
    
  def clearSurfaces(self):
    self.surfaces = []
    self.ratio = 1.0
  
  
  def deleteSurface(self, id):
    for surface in self.surfaces:
      if surface.id == id:
        self.surfaces.remove(surface)
    tmp_surfaces = self.surfaces
    self.clearSurfaces()
    for surface in tmp_surfaces:
      self.surfaces.append(surface)
  
  
  def getSurface(self, surface_id):
    for surface in self.surfaces:
      if surface.id == surface_id:
        return surface
  
  
  def getSurfaces(self):
    return self.surfaces
  
    
  def setFocus(self, value):
    self.focus = value
    
  
  def getFocus(self):
    return self.focus


  def setLabel(self, label):
    self.label = label
    
    
  def getLabel(self):
    return self.label
  
  
  def getVSpace(self):
    return self.vspace
  
  
  def handleEvent(self, event):
    for surface in self.surfaces:
      surface.handleEvent(event)
    
    if event.type == pygame.MOUSEMOTION and self.scrolling:
      if event.rel[1] != 0:
        move = max(event.rel[1], self.track.top - self.knob.top)
        move = min(move, self.track.bottom - self.knob.bottom)
        
        if move != 0:
          self.knob.move_ip(0, move)
          new_y = self.knob.top / self.ratio
          for surface in self.surfaces:
            surface.setNewYPos(surface.getYPos() - new_y)
  
    elif event.type == pygame.MOUSEBUTTONDOWN and self.knob.collidepoint(
                    event.pos[0] - self.x, event.pos[1] - self.y):
      self.scrolling = True
  
    elif event.type == pygame.MOUSEBUTTONUP:
      self.scrolling = False
  
    if event.type == pygame.MOUSEMOTION and self.rect.collidepoint(
                    event.pos[0] - self.x, event.pos[1] - self.y):
      self.mouse_in_me = True
    elif event.type == pygame.MOUSEMOTION and not self.rect.collidepoint(
                    event.pos[0] - self.x, event.pos[1] - self.y):
      self.mouse_in_me = False
  
    if self.mouse_in_me and event.type == pygame.MOUSEBUTTONDOWN:
      move = 0
      if event.button == BUTTON_SCROLL_WHEEL_UP:
        # print("scrolled up")  # debug
        move = max(-1 * SCROLL_SPEED * self.ratio,
                   self.track.top - self.knob.top)
      elif event.button == BUTTON_SCROLL_WHEEL_DOWN:
        # print("scolled down")  # debug
        move = max(SCROLL_SPEED * self.ratio, self.track.top - self.knob.top)
      move = min(move, self.track.bottom - self.knob.bottom)
      
      if move != 0:
        self.knob.move_ip(0, move)
        new_y = self.knob.top / self.ratio
        for surface in self.surfaces:
          surface.setNewYPos(surface.getYPos() - new_y)
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.fill(self.background_color)
    self.content_surface.fill(self.background_color)
    
    surface_pos_y = 0
    for surface in self.surfaces:
      surface.render()
      self.content_surface.blit(surface, (0, surface_pos_y))
      surface_pos_y += surface.get_height() + self.vspace

    self.blit(self.content_surface, (0, (self.knob.top / self.ratio) * -1))
    if self.ratio != 1.0:
      pygame.draw.rect(self, (192, 192, 192), self.track, 0)
      pygame.draw.rect(self, (0, 0, 0), self.knob.inflate(-4, -4), 3)