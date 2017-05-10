from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ClientProtocol(JSONReceiver):
  def __init__(self, factory):
    self.callbacks = {
                      MSG_SERVER_AUTHENTIFICATION: self.serverAuthentification
                     }
    self.factory = factory


  def messageReceived(self, code, data):
    if not code in self.callbacks:
      self.log.warn("received unsupported message {message} with code {code}", message=data, code=code)
    else:
      self.callbacks[code](**data)

  def connectionMade(self):
    self.sendMessage(MSG_CLIENT_AUTHENTIFICATION, major=version.MAJOR, minor=version.MINOR, revision=version.REVISION)


  def serverAuthentification(self, major, minor, revision):
    print 'server authenticated'