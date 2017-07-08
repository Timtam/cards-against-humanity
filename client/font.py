import os.path
import pygame.font

from shared.path import getScriptDirectory

# we need this class to properly encode all data shown on the screen
# only the fonts need this proper encoding,
# that's why we're doing this like so

class Font(pygame.font.Font):
  def __init__(self, display, size):
    self.display = display
    pygame.font.Font.__init__(self, os.path.join(getScriptDirectory(), 'assets', 'font', display.translator.getLanguageFont()+'.ttf'), size)


  def render(self, text, *args, **kwargs):

    encoding = self.display.translator.getLanguageEncoding()

    if encoding is not None:
      text = text.encode(encoding)

    return pygame.font.Font.render(self, text, *args, **kwargs)
