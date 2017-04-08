from twisted.internet.protocol import Factory
from .protocol import ServerProtocol

class ServerFactory(Factory):

  def buildProtocol(self, addr):
    return ServerProtocol()
