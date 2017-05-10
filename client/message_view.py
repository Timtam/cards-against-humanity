from .scrolled_text_panel import ScrolledTextPanel
from .tools import *
from .view import View

PADDING_LEFT_RIGHT = 20
PADDING_TOP_BOTTOM = 20



class MessageView(View):
  def __init__(self, display, width=480, height=480):
    View.__init__(self, display)
    
    self.display = display
    self.display.screen = pygame.display.set_mode((width, height))
    self.width = width
    self.height = height
    
    self.text = ""
    dummy_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
                 "sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
                 "magna aliquyam erat, sed diam voluptua. At vero eos et " \
                 "accusam et justo duo dolores et ea rebum. Stet clita kasd " \
                 "gubergren, no sea takimata sanctus est Lorem ipsum dolor " \
                 "sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing " \
                 "elitr, sed diam nonumy eirmod tempor invidunt ut labore et " \
                 "dolore magna aliquyam erat, sed diam voluptua. At vero eos " \
                 "et accusam et justo duo dolores et ea rebum. Stet clita " \
                 "kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
                 "dolor sit amet."
    self.setText(dummy_text)
    
    self.scrolled_text = ScrolledTextPanel(self.display, self.text,
                                           PADDING_LEFT_RIGHT,
                                           PADDING_TOP_BOTTOM,
                                           width - 2 * PADDING_LEFT_RIGHT,
                                           height - 2 * PADDING_TOP_BOTTOM)
  
  
  # setting some automatically formatted and rendered text onto the screen
  def setText(self, text):
    self.text = text
  
  
  # may display a button (not needed)
  # window may also exist without any button
  # if callback is None, the button will be removed
  # otherwise it will be created
  def setButton(self, text='', callback=None):
    pass
  
  
  def render(self):
    self.scrolled_text.render()
  
  
  def handleEvent(self, event):
    pass
