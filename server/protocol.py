from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):
  Callbacks = {
              }

  def connectionMade(self):
    self.log.info("Connection established from {connection}", connection=self.transport.getPeer())
    self.sendMessage(MSG_REQUEST_CLIENT_AUTHENTIFICATION)
