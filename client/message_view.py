from .scrolled_text_panel import ScrolledTextPanel
from .tools import *
from .view import View

PADDING_LEFT_RIGHT = 20
PADDING_TOP_BOTTOM = 20



class MessageView(View):
  def __init__(self, display, width=480, height=480, maxheight=480):
    View.__init__(self, display)
    
    self.display = display
    self.width = width
    self.height = height
    self.maxheight = maxheight
    self.setHeight(height)
    self.old_screen = display.screen.copy()
    self.old_screen.set_alpha(86)
    self.old_screen = self.blurSurface(self.old_screen)
    self.display_size = display.getSize()
    self.hmiddle = self.display_size[0] / 2
    self.vmiddle = self.display_size[1] / 2
    self.button = None
    
    self.message_box = pygame.Surface((width, self.height))
    self.message_border = pygame.Rect(0, 0, width, self.height)
    
    self.box_x = self.hmiddle - width / 2
    self.box_y = self.vmiddle - height / 2
    
    # # long text for checking scrolled text panel
    # dummy_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
    #              "sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
    #              "magna aliquyam erat, sed diam voluptua. At vero eos et " \
    #              "accusam et justo duo dolores et ea rebum. Stet clita kasd " \
    #              "gubergren, no sea takimata sanctus est Lorem ipsum dolor " \
    #              "sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing " \
    #              "elitr, sed diam nonumy eirmod tempor invidunt ut labore et " \
    #              "dolore magna aliquyam erat, sed diam voluptua. At vero eos " \
    #              "et accusam et justo duo dolores et ea rebum. Stet clita " \
    #              "kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
    #              "dolor sit amet. \n" \
    #              "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
    #              "sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
    #              "magna aliquyam erat, sed diam voluptua. At vero eos et " \
    #              "accusam et justo duo dolores et ea rebum. Stet clita kasd " \
    #              "gubergren, no sea takimata sanctus est Lorem ipsum dolor " \
    #              "sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing " \
    #              "elitr, sed diam nonumy eirmod tempor invidunt ut labore et " \
    #              "dolore magna aliquyam erat, sed diam voluptua. At vero eos " \
    #              "et accusam et justo duo dolores et ea rebum. Stet clita " \
    #              "kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
    #              "dolor sit amet. \n" \
    #              "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
    #              "sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
    #              "magna aliquyam erat, sed diam voluptua. At vero eos et " \
    #              "accusam et justo duo dolores et ea rebum. Stet clita kasd " \
    #              "gubergren, no sea takimata sanctus est Lorem ipsum dolor " \
    #              "sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing " \
    #              "elitr, sed diam nonumy eirmod tempor invidunt ut labore et " \
    #              "dolore magna aliquyam erat, sed diam voluptua. At vero eos " \
    #              "et accusam et justo duo dolores et ea rebum. Stet clita " \
    #              "kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
    #              "dolor sit amet. \n" \
    #              "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
    #              "sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
    #              "magna aliquyam erat, sed diam voluptua. At vero eos et " \
    #              "accusam et justo duo dolores et ea rebum. Stet clita kasd " \
    #              "gubergren, no sea takimata sanctus est Lorem ipsum dolor " \
    #              "sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing " \
    #              "elitr, sed diam nonumy eirmod tempor invidunt ut labore et " \
    #              "dolore magna aliquyam erat, sed diam voluptua. At vero eos " \
    #              "et accusam et justo duo dolores et ea rebum. Stet clita " \
    #              "kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
    #              "dolor sit amet."
    
    dummy_text = "No text"
    self.setText(dummy_text)
  
  
  # setting some automatically formatted and rendered text onto the screen
  def setText(self, text):
    
    self.scrolled_text = ScrolledTextPanel(self.display, self.box_x + PADDING_LEFT_RIGHT, self.box_y + PADDING_TOP_BOTTOM,
                                              self.width - 2 * PADDING_LEFT_RIGHT,
                                              self.height - 2 * PADDING_TOP_BOTTOM)
    self.scrolled_text.setLabel('information')
    self.scrolled_text.addText(text)

    button_height = 0
    if self.button is not None:
      button_height = self.button.getHeight() + PADDING_TOP_BOTTOM
    # calculate new height through the text and adjust the message box
    self.setHeight(self.scrolled_text.getHeight() + button_height + 2 * \
                   PADDING_TOP_BOTTOM)
    self.message_box = pygame.Surface((self.width, self.height))
    self.message_border = pygame.Rect(0, 0, self.width, self.height)
    self.box_y = self.vmiddle - self.height / 2
    self.scrolled_text = ScrolledTextPanel(self.display, self.box_x + PADDING_LEFT_RIGHT, self.box_y + PADDING_TOP_BOTTOM,
                                              self.width - 2 *
                                              PADDING_LEFT_RIGHT,
                                              self.height - 2 *
                                              PADDING_TOP_BOTTOM - button_height)
    self.scrolled_text.setLabel('information')
    self.scrolled_text.addText(text)
    self.tab_position = 0
    self.tab_order = [self.scrolled_text]
    if self.display.accessibility:
      self.scrolled_text.setFocus(True)
      self.speak(text, False)
  
  
  # may display a button (not needed)
  # window may also exist without any button
  # if callback is None, the button will be removed
  # otherwise it will be created
  def setButton(self, text="", callback=None):
    if callback is not None:
      self.button = Button(self.display, text, self.display.getFont(),
                           (100, 100))
      self.button.setPosition(
        (self.hmiddle + self.width / 2 - self.button.getWidth() -
         PADDING_LEFT_RIGHT,
         self.vmiddle + self.height / 2 - self.button.getHeight() -
         PADDING_TOP_BOTTOM))
      self.button.setCallback(callback)
      # need to call setText as you can call setButton from external; after that
      # we got a new height, so we need to position the buton again
      self.setText(self.scrolled_text.getText())
      self.button.setPosition(
        (self.hmiddle + self.width / 2 - self.button.getWidth() -
         PADDING_LEFT_RIGHT,
         self.vmiddle + self.height / 2 - self.button.getHeight() -
         PADDING_TOP_BOTTOM))
      self.tab_order.append(self.button)
    else:
      self.button = None
      if len(self.tab_order)>1:
        del self.tab_order[1]
        if self.tab_position >0:
          self.tab_position = 0
  
  # handy mehtod to check maxheight befor setting height
  def setHeight(self, new_height):
    if new_height > self.maxheight:
      self.height = self.maxheight
    else:
      self.height = new_height
  
  
  def render(self):
    self.display.screen.blit(self.old_screen, (0, 0))
    self.message_box.fill((255, 255, 255))
    pygame.draw.rect(self.message_box, (0, 0, 0), self.message_border, 3)
    self.scrolled_text.render()
    self.display.screen.blit(self.message_box, (self.box_x, self.box_y))
    self.display.screen.blit(self.scrolled_text, (self.box_x + PADDING_LEFT_RIGHT, self.box_y + PADDING_TOP_BOTTOM))
    if self.button is not None:
      self.button.render()
  
  
  def handleEvent(self, event):
    View.handleEvent(self, event)
    self.scrolled_text.handleEvent(event)
    if self.button is not None:
      self.button.handleEvent(event)

  def firstUpdate(self):
    pass

  # function for blurring a surface through smoothscaling to lower resolution
  # and back to original
  @staticmethod
  def blurSurface(surface, val=2.0):
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

