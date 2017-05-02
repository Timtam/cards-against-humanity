import pygame
import sys

class Display(object):
  def __init__(self, width = 1280, height = 720):

    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Cards Against Humanity Online')

  def handleEvent(self, event):
    pass

  def update(self):
    pass

  def render(self):
    self.screen.fill((0,0,0))
    pygame.display.flip()

  def process(self):
    for event in pygame.event.get():
      self.handleEvent(event)
    self.update()
    self.render()
