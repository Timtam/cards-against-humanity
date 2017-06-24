import hashlib

from .message_view import MessageView
from .tools import Button, TextInput
from .scrolled_panel import ScrolledPanel
from .game_entry import GameEntry

import pygame

PADDING = 20



class OverviewView(MessageView):
  def __init__(self, display):
    MessageView.__init__(self, display)
    
    self.screen_size = self.display.getSize()
    self.font = self.display.getFont()
    
    self.label_game_name = self.font.render(display.translator.translate("Game name")+':', 1, (0, 0, 0))
    self.input_game_name = TextInput(self.display, self.font, (20, 50), 300, self.display.translator.translate("Game name"))
    self.label_game_password = self.font.render(display.translator.translate("Game password (optional)")+':', 1, (0, 0, 0))
    self.input_game_password = TextInput(self.display, self.font, (20, 130), 300, self.display.translator.translate("Game password"), True)
    
    self.button_create = Button(self.display, display.translator.translate("Create game"), self.font, (20, 200))
    self.button_create.setCallback(self.onCreate)
    self.button_join = Button(self.display, display.translator.translate("Join game"), self.font, (20, 250))
    self.button_join.setCallback(self.onJoin)
    self.button_disconnect = Button(self.display, display.translator.translate("Disconnect"), self.font, (20, 350))
    self.button_disconnect.setCallback(self.onDisconnect)
    
    self.surface_overview = pygame.Surface((self.screen_size[0] - 340, self.screen_size[1]))
    self.overview_border = pygame.Rect(0, 0, self.surface_overview.get_width(), self.surface_overview.get_height())
    self.game_overview = ScrolledPanel(self.display, 340 + PADDING, PADDING, self.surface_overview.get_width() - 2 * PADDING, self.surface_overview.get_height() - 2 * PADDING)
    self.game_overview.setLabel(display.translator.translate('Games to join'))

    self.next_surface_pos_y = self.game_overview.getPos()[1]
    
    self.tab_order = [self.game_overview, self.input_game_name, self.input_game_password, self.button_create, self.button_join, self.button_disconnect]
    self.game_selected = False

    for game in self.display.factory.getAllGames():
      self.addGame(game['id'])

    if len(self.game_overview.getSurfaces()) == 0:
      self.button_join.setEnable(False)

  
  def addGame(self, game_id):
    old_len = len(self.game_overview.getSurfaces())

    game_entry = GameEntry(self.display, self.game_overview.getPos()[0], self.next_surface_pos_y, self.game_overview.getAvailableWidth() - 20, 50, game_id)
    self.game_overview.addSurface(game_entry)
    self.next_surface_pos_y += game_entry.get_height() + self.game_overview.getVSpace()

    if old_len == 0:
      game_entry.setClicked()
      self.button_join.setEnable(True)
      self.input_game_name.setText(game_entry.text)

  
  def clearGames(self):
    self.game_overview.clearSurfaces()
    self.next_surface_pos_y = self.game_overview.getPos()[1]
  
  
  def deleteGame(self, game_id):
    tmp_surfaces = self.game_overview.getSurfaces()
    self.clearGames()
    for surface in tmp_surfaces:
      if surface.getId() != game_id:
        self.addGame(surface.getId())

    if len(self.game_overview.getSurfaces()) == 0:
      self.button_join.setEnable(False) 

  
  def handleEventDefault(self, event):
    MessageView.handleEventDefault(self, event)
    
    self.game_selected = False
    self.input_game_name.handleEvent(event)
    self.input_game_password.handleEvent(event)
    
    self.button_create.handleEvent(event)
    self.button_join.handleEvent(event)
    self.button_disconnect.handleEvent(event)
    
    self.game_overview.handleEvent(event)
  
  
  def update(self):
    self.input_game_name.update()
    self.input_game_password.update()
  
  
  def renderDefault(self):
    self.display.screen.blit(self.label_game_name, (20, 20))
    self.input_game_name.render()
    self.display.screen.blit(self.label_game_password, (20, 100))
    self.input_game_password.render()
    
    self.button_create.render()
    self.button_join.render()
    self.button_disconnect.render()
    
    self.surface_overview.fill((255, 255, 255))
    pygame.draw.rect(self.surface_overview, (0, 0, 0), self.overview_border, 5)
    self.display.screen.blit(self.surface_overview, (340, 0))
    self.game_overview.render()
    self.display.screen.blit(self.game_overview, self.game_overview.getPos())

  def onDisconnect(self):
    self.display.callFunction('self.factory.closeClient')
    self.display.setView('LoginView')


  def onGameSelect(self, game):
    self.input_game_name.setText(game.text)
    self.input_game_password.setText('')
    self.button_join.setEnable(True)
    self.game_selected = True
    
  def onGameDeselect(self, game):
    # if self.game_selected == True, this loop another game was already selected
    # if we deselect now, we will end up with a cleared screen, but a
    # selected panel
    if not self.game_selected:
      self.input_game_name.setText('')
      self.input_game_password.setText('')
      self.button_join.setEnable(False)


  def errorMessage(self, message):
    self.default_mode = False
    MessageView.errorMessage(self, message, self.onOK)


  def onOK(self):
    self.default_mode = True


  def onCreate(self):
    if self.input_game_password.input.get_text() == '':
      password = None
    else:
      password = hashlib.sha512(self.input_game_password.input.get_text()).hexdigest()
    self.display.factory.client.sendCreateGame(self.input_game_name.input.get_text(), password)
    self.default_mode = False
    self.setText(self.display.translator.translate('Creating game...'))

  def onJoin(self):
    game = self.game_overview.getClickedSurface()
    if game is None:
      self.errorMessage(self.display.translator.translate('No game selected'))
      return

    if len(self.input_game_password.input.get_text()) == 0:
      password = None
    else:
      password = hashlib.sha512(self.input_game_password.input.get_text()).hexdigest()

    self.display.factory.client.sendJoinGame(game.id, password)
    self.default_mode = False
    self.setText(self.display.translator.translate('Joining game...'))

