import pygame

class View(object):
  def __init__(self, display):
    self.display = display

  def update(self):
    pass

  def render(self):
    pass

  def handleEvent(self, event):
    pass

  def loadImage(self, filename, colorkey = None):

    image = pygame.image.load(filename)

    if image.get_alpha() is None:
      image = image.convert()
    else:
      image = image.convert_alpha()

    if colorkey is not None:

      if colorkey == -1:
        colorkey = image.get_at((0, 0))

    image.set_colorkey(colorkey, pygame.RLEACCEL)

    return image
