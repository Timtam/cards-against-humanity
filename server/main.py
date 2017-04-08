from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from .factory import ServerFactory

def main():
  endpoint = TCP4ServerEndpoint(reactor, 11337)
  endpoint.listen(ServerFactory())
  reactor.run()
