import hashlib
import os.path

import pygame
import sys
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.error import ConnectionRefusedError, DNSLookupError
from twisted.internet.task import LoopingCall

from .events import *
from .factory import ClientFactory
from .login_view import LoginView
from .connection_view import ConnectionView
from .message_view import MessageView
from .game_view import GameView
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
    self.server_name = ''
    
    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Cards Against Humanity Online')
    
    # global font (may be the original from Cards Against Humanity)
    self.font = open(os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), 'rb')
    
    # setting the current view
    self.view = None
    # loading all sounds
    self.loadSounds()
  
  
  def getFont(self, size = 20):
    # the preferred way of loading the font from a file doesn't work properly on x64 systems
    if sys.maxsize>2**32:
      return pygame.font.Font(os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), size)
    else:
      self.font.seek(0)
      return pygame.font.Font(self.font, size)
  
  
  def getSize(self):
    return self.screen.get_width(), self.screen.get_height()
  
  
  def handleEvent(self, event):
    if event.type == pygame.QUIT:
      self.stop()
    elif event.type == EVENT_VIEWCHANGE:
      if not isinstance(self.view, eval(event.view)):
        self.view = eval(event.view)(self)
    elif event.type == EVENT_FUNCALL:
      eval(event.function)(*event.args, **event.kwargs)
    else:
      if self.view:
        self.view.handleEvent(event)
  
  
  def update(self):
    if self.view:
      self.view.update()
  
  
  def render(self):
    if self.view:
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
    self.start_sound.play()
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
    self.game_error_sound = sound('game_error')
    self.join_game_sound = sound('join_game')
    self.leave_game_sound = sound('leave_game')
    self.login_sound = sound('login')
    self.start_sound = sound('start')
    self.tap_sound = sound('tap')
    self.tap_delete_sound = sound('tap_delete')
  
  
  def setView(self, view):
    pygame.event.post(pygame.event.Event(EVENT_VIEWCHANGE, view=view))


  def callFunction(self, function, *args, **kwargs):
    pygame.event.post(pygame.event.Event(EVENT_FUNCALL, function=function, args=args, kwargs=kwargs))

  # unhashed password is required here
  def connect(self, host, username, password):
    def connectionRefusedErrback(failure):
      failure.trap(ConnectionRefusedError)
      self.view.errorMessage(failure.getErrorMessage())
    def dnsLookupErrback(failure):
      failure.trap(DNSLookupError)
      self.view.errorMessage('unable to lookup ip adress for servername: %s'%failure.getErrorMessage())
    self.login_name = username
    self.login_password = password
    self.server_name = host
    self.endpoint = TCP4ClientEndpoint(self.reactor, host, 11337)
    deferred = self.endpoint.connect(self.factory)
    deferred.addErrback(connectionRefusedErrback)
    deferred.addErrback(dnsLookupErrback)
    deferred.addErrback(lambda err: err.printTraceback())


  def getLoginCredentials(self):
    return (self.login_name, hashlib.sha512(self.login_password).hexdigest())
