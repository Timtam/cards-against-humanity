from .view import View
import text_input

class InitialView(View):
  def __init__(self, display):
    View.__init__(self, display)
    self.text_input = text_input.TextInput()
  
  def handleEvent(self, event):
    self.text_input.update(event)
    
  def render(self):
    surface = self.text_input.get_surface()
    self.display.screen.blit(surface, (100,100))
