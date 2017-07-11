from scrolled_panel_surface import ScrolledPanelSurface
import pygame.image
from shared.path import getScriptDirectory
import os.path


class GameEntry(ScrolledPanelSurface):
  def __init__(self, display, x, y, width, height, game_id):
    ScrolledPanelSurface.__init__(self, display, x, y, width, height)
    
    self.id = game_id
    self.lock = pygame.image.load(os.path.join(getScriptDirectory(), 'assets', 'images', 'lock.png'))
    self.game = self.display.factory.findGame(self.id)
    self.updateText()
  

  def getId(self):
    return self.id
    
  
  def getLabel(self):
    label = self.text
    if self.game['protected']:
      label += ' ('+self.display.translator.translate('password required')+')'
    return label
  
  
  def render(self):
    ScrolledPanelSurface.render(self)
    if self.game['protected']:
      self.blit(self.lock, (20, (self.height - self.lock.get_height()) / 2))
      self.blit(self.rendered_text, (self.lock.get_width() + 40, 5 + (self.height - self.rendered_text.get_height()) / 2))
    else:
      self.blit(self.rendered_text, (10, (self.height - self.rendered_text.get_height()) / 2))
    

  def setText(self, text):
    self.text = text
    self.rendered_text = self.display.getFont().render(text, 1, (0, 0, 0))


  def updateText(self):

    if self.game is None:
      return

    self.setText(self.game['name']+', '+self.display.translator.translate('{players} players').format(players = self.game['users'])+", "+self.display.translator.translate("{rounds} rounds remaining").format(rounds = self.game['rounds']))
