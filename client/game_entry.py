from scrolled_panel_surface import ScrolledPanelSurface



class GameEntry(ScrolledPanelSurface):
  def __init__(self, display, x, y, width, height, game_id):
    ScrolledPanelSurface.__init__(self, display, x, y, width, height)
    
    self.id = game_id
    self.updateText()
  

  def getId(self):
    return self.id
    
  
  def getLabel(self):
    return self.text
  
  
  def render(self):
    ScrolledPanelSurface.render(self)
    self.blit(self.rendered_text, (10, (self.height - self.rendered_text.get_height()) / 2))
    

  def setText(self, text):
    self.text = text
    self.rendered_text = self.display.getFont().render(text, 1, (0, 0, 0))


  def updateText(self):

    game = self.display.factory.findGame(self.id)

    if game is None:
      return

    self.setText(game['name']+', '+self.display.translator.translate('{players} players').format(players = game['users'])+", "+self.display.translator.translate("{rounds} rounds remaining").format(rounds = game['rounds']))
