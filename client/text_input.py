import pygame
import pygame.locals as pl

DEFAULT_LENGTH = 300



class TextInput:
  """
  This class lets the user input a piece of text, e.g. a name or a message.

  This class let's the user input a short, one-lines piece of text at a
  blinking cursor
  that can be moved using the arrow-keys. Delete, home and end work as well.
  """
  
  
  def __init__(self, display, font,
               antialias=True,
               text_color=(0, 0, 0),
               cursor_color=(0, 0, 1),
               max_width=DEFAULT_LENGTH,
               password = False):
    """
    Args:
        #font_family: Name or path of the font that should be used. Default is
        pygame-font
        #font_size: Size of the font in pixels
        antialias: (bool) Determines if antialias is used on fonts or not
        text_color: Color of the text
    """
    
    # Text related vars:
    self.display = display
    self.antialias = antialias
    self.text_color = text_color
    self.font_size = font.get_linesize()
    self.input_string = ""  # Inputted text
    self.font_object = font
    
    # max width of text input
    self.max_width = max_width
    self.password = password
    
    # focus
    self.focus = False
    
    # Text-surface will be created during the first update call:
    self.surface = pygame.Surface((1, 1))
    self.surface.set_alpha(0)
    
    # Things cursor:
    self.cursor_surface = pygame.Surface(
      (int(self.font_size / 20 + 1), self.font_size))
    self.cursor_surface.fill(cursor_color)
    self.cursor_position = 0  # Inside text
    self.cursor_visible = False  # Switches every self.cursor_switch_ms ms
    self.cursor_switch_ms = 500  # /|\
    self.cursor_ms_counter = 0
    
    self.clock = pygame.time.Clock()
  
  
  def setFocus(self, flag):
    self.focus = flag
  
  
  def handleEvent(self, event):
    if self.focus and event.type == pygame.KEYDOWN:
      self.cursor_visible = True  # So the user sees where he writes
      
      if event.key == pl.K_BACKSPACE:  # FIXME: Delete at beginning of line?
        try:
          self.display.view.speak(self.input_string[-1] if not self.password else '*', True)
        except IndexError:
          self.display.view.speak('', True)
        self.input_string = self.input_string[
                            :max(self.cursor_position - 1, 0)] + \
                            self.input_string[self.cursor_position:]
        # Subtract one from cursor_pos, but do not go below zero:
        self.cursor_position = max(self.cursor_position - 1, 0)
        self.display.tap_delete_sound.stop()
        self.display.tap_delete_sound.play()
      
      elif event.key == pl.K_DELETE:
        try:
          self.display.view.speak(self.input_string[self.cursor_position] if not self.password else '*', True)
        except IndexError:
          self.display.view.speak('', True)
        self.input_string = self.input_string[:self.cursor_position] + \
                            self.input_string[self.cursor_position + 1:]
        self.display.tap_delete_sound.stop()
        self.display.tap_delete_sound.play()
      
      elif event.key == pl.K_RETURN:
        return True
      
      elif event.key == pl.K_RIGHT:
        # Add one to cursor_pos, but do not exceed len(input_string)
        self.cursor_position = min(self.cursor_position + 1,
                                   len(self.input_string))
        try:
          self.display.view.speak(self.input_string[self.cursor_position] if not self.password else '*', True)
        except IndexError:
          self.display.view.speak('', True)
        self.display.cursor_sound.stop()
        self.display.cursor_sound.play()
      
      elif event.key == pl.K_LEFT:
        # Subtract one from cursor_pos, but do not go below zero:
        self.cursor_position = max(self.cursor_position - 1, 0)
        try:
          self.display.view.speak(self.input_string[self.cursor_position] if not self.password else '*', True)
        except IndexError:
          self.display.view.speak('', True)
        self.display.cursor_sound.stop()
        self.display.cursor_sound.play()
      
      elif event.key == pl.K_END:
        self.cursor_position = len(self.input_string)
        try:
          self.display.view.speak(self.input_string[self.cursor_position] if not self.password else '*', True)
        except IndexError:
          self.display.view.speak('', True)
        self.display.cursor_sound.stop()
        self.display.cursor_sound.play()
      
      elif event.key == pl.K_HOME:
        self.cursor_position = 0
        try:
          self.display.view.speak(self.input_string[self.cursor_position] if not self.password else '*', True)
        except IndexError:
          self.display.view.speak('', True)
        self.display.cursor_sound.stop()
        self.display.cursor_sound.play()
      
      elif event.key == pl.K_TAB or event.key == pl.K_LCTRL:
        # prevent usage here
        # those keys are used differently in our project
        pass
      
      else:
        # to avoid to input endless text, check the length of current text +
        # next character
        text_width = self.font_object.size(self.input_string + "W")[0]  # + "W",
        # because its the possibly widest letter ;)
        if text_width <= self.max_width:
          # If no special key is pressed, add unicode of key to input_string
          self.input_string = self.input_string[:self.cursor_position] + \
                              event.unicode + \
                              self.input_string[self.cursor_position:]
          self.cursor_position += len(
            event.unicode)  # Some are empty, e.g. K_UP
        self.display.view.speak(event.unicode if not self.password else '*', True)
        if len(event.unicode):
          self.display.tap_sound.stop()
          self.display.tap_sound.play()
    
    return False
  
  
  def render(self):
    
    # Rerender text surface:
    self.surface = self.font_object.render(self.input_string if not self.password else '*'*len(self.input_string), self.antialias,
                                           self.text_color)
    
    if self.cursor_visible:
      cursor_y_pos = \
        self.font_object.size(self.input_string[:self.cursor_position])[0]
      # Without this, the cursor is invisible when self.cursor_position > 0:
      if self.cursor_position > 0:
        cursor_y_pos -= self.cursor_surface.get_width()
      self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))
    
    return self.surface
  
  
  def get_text(self):
    return self.input_string
  
  
  def get_cursor_position(self):
    return self.cursor_position
  
  
  def set_text_color(self, color):
    self.text_color = color
  
  
  def set_cursor_color(self, color):
    self.cursor_surface.fill(color)
  
  
  def update(self):
    if self.focus:
      # Update self.cursor_visible
      self.cursor_ms_counter += self.clock.get_time()
      if self.cursor_ms_counter >= self.cursor_switch_ms:
        self.cursor_ms_counter %= self.cursor_switch_ms
        self.cursor_visible = not self.cursor_visible
      
      self.clock.tick()
    else:
      self.cursor_visible = False
