from scrolled_panel_surface import ScrolledPanelSurface


class LanguageEntry(ScrolledPanelSurface):
  def __init__(self, display, x, y, width, height, language=None):
    ScrolledPanelSurface.__init__(self, display, x, y, width, height)
    
    self.text = language
    self.rendered_text = self.display.getFont().render(self.text, 1, (0, 0, 0))
  

  def render(self):
    ScrolledPanelSurface.render(self)
    self.blit(self.rendered_text, ((self.width - self.rendered_text.get_width()) / 2, (self.height - self.rendered_text.get_height()) / 2))


  def getLabel(self):
    return self.text