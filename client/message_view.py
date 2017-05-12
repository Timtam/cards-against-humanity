from .scrolled_text_panel import ScrolledTextPanel
from .tools import *
from .view import View

PADDING_LEFT_RIGHT = 20
PADDING_TOP_BOTTOM = 20



class MessageView(View):
  def __init__(self, display, width=480, height=480):
    View.__init__(self, display)
    
    self.display = display
    self.width = width
    self.height = height
    self.old_screen = display.screen.copy()
    self.old_screen.set_alpha(86)
    self.old_screen = self.blurSurface(self.old_screen, 1.5)
    self.display_size = display.getSize()
    self.hmiddle = self.display_size[0] / 2
    self.vmiddle = self.display_size[1] / 2
    self.button = None
    
    self.text = ""
    dummy_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
                 "sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
                 "magna aliquyam erat, sed diam voluptua. At vero eos et " \
                 "accusam et justo duo dolores et ea rebum. Stet clita kasd " \
                 "gubergren, no sea takimata sanctus est Lorem ipsum dolor " \
                 "sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing " \
                 "" \
                 "" \
                 "elitr, sed diam nonumy eirmod tempor invidunt ut labore et " \
                 "dolore magna aliquyam erat, sed diam voluptua. At vero eos " \
                 "et accusam et justo duo dolores et ea rebum. Stet clita " \
                 "kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
                 "dolor sit amet."
    self.setText(dummy_text)
    
    self.message_box = pygame.Surface((width, height))
    self.message_border = pygame.Rect(0, 0, width, height)
    
    self.box_x = self.hmiddle - width / 2
    self.box_y = self.vmiddle - height / 2
    
    self.scrolled_text = ScrolledTextPanel(self.message_box, self.text,
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
  def setButton(self, text="", callback=None):
    if callback is not None:
      self.button = Button(self.message_box, text, self.display.getFont(),
                           (100, 100))
      self.button.setPosition((self.width - self.button.getWidth() -
                               PADDING_LEFT_RIGHT,
                               self.height - self.button.getHeight() -
                               PADDING_TOP_BOTTOM))
      self.button.setCallback(callback)
    else:
      self.button = None
  
  
  def render(self):
    self.display.screen.blit(self.old_screen, (0, 0))
    self.message_box.fill((255, 255, 255))
    pygame.draw.rect(self.message_box, (0, 0, 0), self.message_border, 3)
    self.scrolled_text.render()
    if self.button is not None:
      self.button.render()
    self.display.screen.blit(self.message_box, (self.box_x, self.box_y))
  
  
  def handleEvent(self, event):
    if self.button is not None:
      self.button.handleEvent(event)


  def blurSurface(self, surface, val=2.0):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value = 1 -> no blur.
    """
    if val < 1.0:
      raise ValueError(
        "Arg 'val' must be greater than 1.0, passed in value is %s" % val)
    scale = 1.0 / float(val)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

