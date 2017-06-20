from .view import View
from .tools import Button
from .scrolled_panel import ScrolledPanel
from .game_entry import GameEntry

import pygame

PADDING = 20



class OverviewView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    self.display = display
    self.screen_size = self.display.getSize()
    
    self.surface_overview = pygame.Surface((self.screen_size[0], self.screen_size[1] * 0.5))
    self.overview_border = pygame.Rect(0, 0, self.surface_overview.get_width(), self.surface_overview.get_height())
    self.game_overview = ScrolledPanel(self.display, PADDING, PADDING, self.surface_overview.get_width() - 2 * PADDING, self.surface_overview.get_height() - 2 * PADDING)
    
    surface_pos_y = PADDING
    for i in range(10):
      dummy = GameEntry(self.display, PADDING, surface_pos_y, self.game_overview.getAvailableWidth() - 20, 50)
      surface_pos_y += dummy.get_height() + self.game_overview.getVSpace()
      self.game_overview.addSurface(dummy)
    
    self.button_join = Button(self.display, "Join Game", self.display.getFont(), (self.screen_size[0] / 2, self.screen_size[1] * 0.8))
    self.tab_order = [self.game_overview, self.button_join]
    
    
  def handleEvent(self, event):
    View.handleEvent(self, event)
    self.game_overview.handleEvent(event)
    self.button_join.handleEvent(event)
    
    
  def render(self):
    self.surface_overview.fill((255, 255, 255))
    pygame.draw.rect(self.surface_overview, (0, 0, 0), self.overview_border, 5)
    self.display.screen.blit(self.surface_overview, (0, 0))
    self.game_overview.render()
    self.display.screen.blit(self.game_overview, (PADDING, PADDING))
    self.button_join.render()