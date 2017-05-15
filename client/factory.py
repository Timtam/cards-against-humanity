from twisted.internet.protocol import Factory
from twisted.logger import Logger

from .protocol import ClientProtocol

class ClientFactory(Factory):
  display = None
  log = Logger()

  def __init__(self, display):
    self.client = None
    self.display = display


  def buildProtocol(self, addr):
    self.client = ClientProtocol(self)
    return self.client

  def closeClient(self):
    if self.client:
      self.client.transport.loseConnection()
      self.client = None
