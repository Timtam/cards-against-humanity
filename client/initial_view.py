from .view import View
import text_input

class InitialView(View):
  def __init__(self):
    self.textinput = text_input.TextInput()
  
  
  def handleEvent(self, event):
    self.textinput.update(event)
    
  def update(self):
    print self.textinput.get_text()
    
  def render(self):
    return self.textinput.surface