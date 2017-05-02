from twisted.internet.protocol import Factory
from twisted.logger import Logger

from .protocol import ClientProtocol

class ClientFactory(Factory):
  log = Logger()

  def buildProtocol(self, addr):
    return ClientProtocol(self)
