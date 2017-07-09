import os.path
import pygame.font
import types

from shared.path import getScriptDirectory

# we need this class to properly encode all data shown on the screen
# only the fonts need this proper encoding,
# that's why we're doing this like so

class Font(pygame.font.Font):
  def __init__(self, display, size):
    self.display = display
    self.encoding = None
    pygame.font.Font.__init__(self, os.path.join(getScriptDirectory(), 'assets', 'font', display.translator.getLanguageFont()+'.ttf'), size)


  def render(self, text, *args, **kwargs):

    if type(text) == types.UnicodeType:

      if self.encoding is None:

        self.encoding = self.display.translator.getLanguageEncoding()

      if self.encoding is not None:

        text = text.encode(self.encoding)

    return pygame.font.Font.render(self, text, *args, **kwargs)
