from twisted.internet.protocol import Factory
from twisted.logger import Logger

from .protocol import ClientProtocol

class ClientFactory(Factory):
  display = None
  log = Logger()

  def __init__(self, display):
    self.display = display


  def buildProtocol(self, addr):
    return ClientProtocol(self)
