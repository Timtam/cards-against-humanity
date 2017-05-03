from .initial_view import InitialView

import pygame
import sys

class Display(object):
  def __init__(self, width = 1280, height = 720):

    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Cards Against Humanity Online')

    # setting the current view
    self.view = InitialView(self)

  def handleEvent(self, event):
    if event.type == pygame.QUIT:
      self.stop()
    self.view.handleEvent(event)

  def update(self):
    self.view.update()

  def render(self):
    self.screen.fill((255,255,255))
    self.view.render()
    pygame.display.flip()

  def process(self):
    for event in pygame.event.get():
      self.handleEvent(event)
    self.update()
    self.render()

  def stop(self):
    pygame.quit()
    sys.exit()