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
    self.font = self.display.getFont()
    
    self.next_surface_pos_y = PADDING
    
    self.surface_overview = pygame.Surface((self.screen_size[0], self.screen_size[1] * 0.5))
    self.overview_border = pygame.Rect(0, 0, self.surface_overview.get_width(), self.surface_overview.get_height())
    self.game_overview = ScrolledPanel(self.display, PADDING, PADDING, self.surface_overview.get_width() - 2 * PADDING, self.surface_overview.get_height() - 2 * PADDING)
    self.game_overview.setLabel('games to join')
    
    self.button_join = Button(self.display, "Join Game", self.font, (50, self.screen_size[1] * 0.8))
    self.button_create = Button(self.display, "Create Game", self.font, (250, self.screen_size[1] * 0.8))
    self.button_close = Button(self.display, "Close Game Client", self.font, (450, self.screen_size[1] * 0.8))
    self.tab_order = [self.game_overview, self.button_join, self.button_create, self.button_close]

    self.addGame(1)
    self.addGame(2)
    self.addGame(3)
    self.addGame(4)
    self.addGame(5)
    self.addGame(6)
    self.addGame(7)
    self.addGame(8)
    self.deleteGame(8)
    self.deleteGame(3)
    self.deleteGame(5)
    self.deleteGame(6)
    self.deleteGame(1)
    self.deleteGame(2)
  
  
  def addGame(self, game_id):
    game_entry = GameEntry(self.display, PADDING, self.next_surface_pos_y, self.game_overview.getAvailableWidth() - 20, 50, game_id)
    self.game_overview.addSurface(game_entry)
    self.next_surface_pos_y += game_entry.get_height() + self.game_overview.getVSpace()
  
  
  def clearGames(self):
    self.game_overview.clearSurfaces()
    self.next_surface_pos_y = PADDING
  
  
  def deleteGame(self, game_id):
    tmp_surfaces = self.game_overview.getSurfaces()
    self.clearGames()
    for surface in tmp_surfaces:
      if surface.getID() != game_id:
        self.addGame(surface.getID())
  
  
  def handleEvent(self, event):
    View.handleEvent(self, event)
    self.game_overview.handleEvent(event)
    self.button_join.handleEvent(event)
    self.button_create.handleEvent(event)
    self.button_close.handleEvent(event)
    
    
  def render(self):
    self.surface_overview.fill((255, 255, 255))
    pygame.draw.rect(self.surface_overview, (0, 0, 0), self.overview_border, 5)
    self.display.screen.blit(self.surface_overview, (0, 0))
    self.game_overview.render()
    self.display.screen.blit(self.game_overview, (PADDING, PADDING))
    self.button_join.render()
    self.button_create.render()
    self.button_close.render()
