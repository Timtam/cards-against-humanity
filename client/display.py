from .initial_view import InitialView

import pygame
import sys

from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class Display(object):
  def __init__(self, width = 1280, height = 720):

    # initializing the loop caller
    self.loop = LoopingCall(self.process)
    self.running = True

    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Cards Against Humanity Online')

    # global font (may be the original from Cards Against Humanity)
    self.font = pygame.font.Font("assets/helvetica-bold.ttf", 20)

    # setting the current view
    self.view = InitialView(self)


  def getFont(self):
    return self.font


  def getSize(self):
    return self.screen.get_width(), self.screen.get_height()


  def handleEvent(self, event):
    if event.type == pygame.QUIT:
      self.stop()
      return
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
      if not self.running:
        return
    self.update()
    self.render()

  def stop(self):
    pygame.quit()
    reactor.stop()
    self.running = False

  def init(self):
    self.loop.start(1.0 / 30.0)
    reactor.run()
