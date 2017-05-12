import hashlib
import os.path

import pygame
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.task import LoopingCall

from .connection_view import ConnectionView
from .factory import ClientFactory
from .login_view import LoginView
from shared.path import getScriptDirectory



class Display(object):
  def __init__(self, width=1280, height=720, accessibility=False):
    
    self.accessibility = accessibility
    self.endpoint = None
    self.factory = ClientFactory(self)
    # initializing the loop caller
    self.loop = LoopingCall(self.process)
    self.reactor = None
    self.running = True
    self.login_name = ''
    self.login_password = ''
    
    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Cards Against Humanity Online')
    
    # global font (may be the original from Cards Against Humanity)
    self.font = pygame.font.Font(
      os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), 20)
    
    # setting the current view
    self.view = None
    # loading all sounds
    self.loadSounds()
  
  
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
    self.screen.fill((255, 255, 255))
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
    self.reactor.stop()
    self.running = False
  
  
  def init(self):
    self.loop.start(1.0 / 30.0)
    self.reactor = reactor
    self.reactor.run()

  def loadSounds(self):
    # the function which builds some sounds path for us
    def sound(name):
      return pygame.mixer.Sound(
        os.path.join(getScriptDirectory(), 'assets', 'sound', name + '.ogg'))
    
    self.button_down_sound = sound('button_down')
    self.button_up_sound = sound('button_up')
    self.connect_sound = sound('connect')
    self.cursor_sound = sound('cursor')
    self.error_sound = sound('error')
    self.login_sound = sound('login')
    self.start_sound = sound('start')
    self.tap_sound = sound('tap')
    self.tap_delete_sound = sound('tap_delete')
  
  
  def setView(self, view):
    self.view = eval(view)(self)


  # unhashed password is required here
  def connect(self, host, username, password):
    self.login_name = username
    self.login_password = hashlib.sha512(password).hexdigest()
    self.endpoint = TCP4ClientEndpoint(self.reactor, host, 11337)
    deferred = self.endpoint.connect(self.factory)
    deferred.addErrback(lambda err: err.printTraceback())


  def getLoginCredentials(self):
    return (self.login_name, self.login_password)
