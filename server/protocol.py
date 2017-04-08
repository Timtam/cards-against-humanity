from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):
  callbacks = {}

  def __init__(self):
    self.callbacks = {
                       MSG_CLIENT_AUTHENTIFICATION: self.clientAuthentification
                     }

  def connectionMade(self):
    self.log.info("Connection established from {connection}", connection=self.transport.getPeer())
    self.sendMessage(MSG_REQUEST_CLIENT_AUTHENTIFICATION)

  def messageReceived(self, code, data):
    if not code in self.callbacks:
      self.log.warn("Received unsupported message {message} with code {code} from {connection}", message=data, connection=self.transport.getPeer(), code=code)
    else:
      self.callbacks[code](**data)

  def clientAuthentification(self):
    pass