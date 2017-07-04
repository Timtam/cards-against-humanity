from scrolled_panel_surface import ScrolledPanelSurface



class GameEntry(ScrolledPanelSurface):
  def __init__(self, display, x, y, width, height, game_id):
    ScrolledPanelSurface.__init__(self, display, x, y, width, height)
    
    self.id = game_id
    self.text = self.display.factory.findGamename(game_id)
    self.rendered_text = self.display.getFont().render(self.text, 1, (0, 0, 0))
    
  
  def getId(self):
    return self.id
    
  
  def getLabel(self):
    return self.text
  
  
  def render(self):
    ScrolledPanelSurface.render(self)
    self.blit(self.rendered_text, (10, (self.height - self.rendered_text.get_height()) / 2))
    